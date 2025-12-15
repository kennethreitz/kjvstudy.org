// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use std::time::Duration;
use tauri::{
    Manager, RunEvent, WebviewUrl, WebviewWindowBuilder,
    menu::{Menu, MenuItem, PredefinedMenuItem, Submenu},
    Emitter,
};

struct ServerProcess(Mutex<Option<Child>>);

const SERVER_URL: &str = "http://127.0.0.1:31102";
const APP_VERSION: &str = "0.1.0";

// Loading screen HTML
const LOADING_HTML: &str = r#"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #f5f5dc 0%, #e8e4d4 100%);
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #333;
        }
        .logo {
            font-size: 48px;
            margin-bottom: 8px;
        }
        h1 {
            font-size: 28px;
            font-weight: 300;
            letter-spacing: 2px;
            margin-bottom: 40px;
            color: #4a4a4a;
        }
        .spinner {
            width: 40px;
            height: 40px;
            border: 3px solid #ddd;
            border-top-color: #8b7355;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .status {
            margin-top: 20px;
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="logo">📖</div>
    <h1>KJV STUDY</h1>
    <div class="spinner"></div>
    <p class="status">Starting server...</p>
</body>
</html>
"#;

fn start_server() -> Option<Child> {
    println!("Starting KJV Study server...");

    // Try to find bundled server executable first (for standalone build)
    let exe_dir = std::env::current_exe().ok()?.parent()?.to_path_buf();

    // On macOS, resources are in ../Resources relative to the executable
    // Tauri preserves path structure, so ../dist/kjvstudy-server becomes _up_/dist/kjvstudy-server
    let resources_dir = exe_dir.parent()?.join("Resources");
    let bundled_server = resources_dir
        .join("_up_")
        .join("dist")
        .join("kjvstudy-server")
        .join("kjvstudy-server");

    println!("Looking for bundled server at: {:?}", bundled_server);

    if bundled_server.exists() {
        println!("Found bundled server, starting...");
        let child = Command::new(&bundled_server)
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .ok()?;

        println!("Server process started with PID: {}", child.id());
        return Some(child);
    }

    // Fall back to development mode (uv or python3)
    println!("Bundled server not found, trying development mode...");
    let working_dir = std::env::current_dir().ok()?;
    println!("Working directory: {:?}", working_dir);

    let child = Command::new("uv")
        .args([
            "run", "uvicorn",
            "kjvstudy_org.server:app",
            "--host", "127.0.0.1",
            "--port", "31102",
            "--log-level", "warning"
        ])
        .current_dir(&working_dir)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .or_else(|_| {
            println!("uv not found, trying python3...");
            Command::new("python3")
                .args([
                    "-m", "uvicorn",
                    "kjvstudy_org.server:app",
                    "--host", "127.0.0.1",
                    "--port", "31102",
                    "--log-level", "warning"
                ])
                .current_dir(&working_dir)
                .stdout(Stdio::piped())
                .stderr(Stdio::piped())
                .spawn()
        })
        .ok()?;

    println!("Server process started with PID: {}", child.id());
    Some(child)
}

fn wait_for_server(max_attempts: u32) -> bool {
    let client = reqwest::blocking::Client::builder()
        .timeout(Duration::from_secs(2))
        .build()
        .unwrap();

    for attempt in 1..=max_attempts {
        println!("Waiting for server... (attempt {}/{})", attempt, max_attempts);

        match client.get(format!("{}/api/health", SERVER_URL)).send() {
            Ok(response) if response.status().is_success() => {
                println!("Server is ready!");
                return true;
            }
            _ => {
                std::thread::sleep(Duration::from_millis(500));
            }
        }
    }

    println!("Server failed to start after {} attempts", max_attempts);
    false
}

fn create_menu(app: &tauri::AppHandle) -> tauri::Result<Menu<tauri::Wry>> {
    // App menu (macOS)
    let about = MenuItem::with_id(app, "about", "About KJV Study", true, None::<&str>)?;
    let quit = PredefinedMenuItem::quit(app, Some("Quit KJV Study"))?;
    let app_menu = Submenu::with_items(
        app,
        "KJV Study",
        true,
        &[&about, &PredefinedMenuItem::separator(app)?, &quit],
    )?;

    // File menu
    let close = PredefinedMenuItem::close_window(app, Some("Close Window"))?;
    let file_menu = Submenu::with_items(app, "File", true, &[&close])?;

    // Edit menu
    let edit_menu = Submenu::with_items(
        app,
        "Edit",
        true,
        &[
            &PredefinedMenuItem::undo(app, None)?,
            &PredefinedMenuItem::redo(app, None)?,
            &PredefinedMenuItem::separator(app)?,
            &PredefinedMenuItem::cut(app, None)?,
            &PredefinedMenuItem::copy(app, None)?,
            &PredefinedMenuItem::paste(app, None)?,
            &PredefinedMenuItem::select_all(app, None)?,
        ],
    )?;

    // Navigate menu
    let nav_home = MenuItem::with_id(app, "nav_home", "Home", true, Some("CmdOrCtrl+Shift+H"))?;
    let nav_books = MenuItem::with_id(app, "nav_books", "Books", true, Some("CmdOrCtrl+B"))?;
    let nav_search = MenuItem::with_id(app, "nav_search", "Search", true, Some("CmdOrCtrl+K"))?;
    let nav_votd = MenuItem::with_id(app, "nav_votd", "Verse of the Day", true, Some("CmdOrCtrl+D"))?;
    let nav_random = MenuItem::with_id(app, "nav_random", "Random Verse", true, Some("CmdOrCtrl+R"))?;

    let navigate_menu = Submenu::with_items(
        app,
        "Navigate",
        true,
        &[
            &nav_home,
            &nav_books,
            &PredefinedMenuItem::separator(app)?,
            &nav_search,
            &nav_votd,
            &nav_random,
        ],
    )?;

    // Study menu
    let study_guides = MenuItem::with_id(app, "study_guides", "Study Guides", true, None::<&str>)?;
    let topics = MenuItem::with_id(app, "topics", "Topics", true, None::<&str>)?;
    let stories = MenuItem::with_id(app, "stories", "Bible Stories", true, None::<&str>)?;
    let strongs = MenuItem::with_id(app, "strongs", "Strong's Concordance", true, None::<&str>)?;
    let interlinear = MenuItem::with_id(app, "interlinear", "Interlinear", true, None::<&str>)?;
    let reading_plans = MenuItem::with_id(app, "reading_plans", "Reading Plans", true, None::<&str>)?;

    let study_menu = Submenu::with_items(
        app,
        "Study",
        true,
        &[
            &study_guides,
            &topics,
            &stories,
            &PredefinedMenuItem::separator(app)?,
            &strongs,
            &interlinear,
            &PredefinedMenuItem::separator(app)?,
            &reading_plans,
        ],
    )?;

    // View menu
    let reload = MenuItem::with_id(app, "reload", "Reload", true, Some("CmdOrCtrl+Shift+R"))?;
    let back = MenuItem::with_id(app, "back", "Back", true, Some("CmdOrCtrl+["))?;
    let forward = MenuItem::with_id(app, "forward", "Forward", true, Some("CmdOrCtrl+]"))?;
    let fullscreen = PredefinedMenuItem::fullscreen(app, None)?;

    let view_menu = Submenu::with_items(
        app,
        "View",
        true,
        &[
            &back,
            &forward,
            &reload,
            &PredefinedMenuItem::separator(app)?,
            &fullscreen,
        ],
    )?;

    // Window menu
    let minimize = PredefinedMenuItem::minimize(app, None)?;
    let zoom = PredefinedMenuItem::maximize(app, Some("Zoom"))?;

    let window_menu = Submenu::with_items(
        app,
        "Window",
        true,
        &[&minimize, &zoom],
    )?;

    // Help menu
    let website = MenuItem::with_id(app, "website", "Visit kjvstudy.org", true, None::<&str>)?;
    let help_menu = Submenu::with_items(app, "Help", true, &[&website])?;

    Menu::with_items(
        app,
        &[&app_menu, &file_menu, &edit_menu, &navigate_menu, &study_menu, &view_menu, &window_menu, &help_menu],
    )
}

fn show_about_dialog(app: &tauri::AppHandle) {
    let about_html = format!(r#"
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                    padding: 30px;
                    text-align: center;
                    background: #fafafa;
                    color: #333;
                }}
                .logo {{ font-size: 64px; margin-bottom: 10px; }}
                h1 {{ font-size: 24px; font-weight: 500; margin: 0; }}
                .version {{ color: #666; margin: 8px 0 20px; }}
                .desc {{ font-size: 13px; color: #555; line-height: 1.6; max-width: 280px; margin: 0 auto; }}
                .footer {{ margin-top: 20px; font-size: 11px; color: #999; }}
            </style>
        </head>
        <body>
            <div class="logo">📖</div>
            <h1>KJV Study</h1>
            <p class="version">Version {}</p>
            <p class="desc">
                A comprehensive offline Bible study application featuring the 1769 Cambridge King James Version
                with commentary, cross-references, and original language tools.
            </p>
            <p class="footer">© 2024 Kenneth Reitz</p>
        </body>
        </html>
    "#, APP_VERSION);

    let about_url = format!("data:text/html,{}", urlencoding::encode(&about_html));

    if let Ok(_) = WebviewWindowBuilder::new(
        app,
        "about",
        WebviewUrl::External(about_url.parse().unwrap())
    )
    .title("About KJV Study")
    .inner_size(350.0, 320.0)
    .resizable(false)
    .minimizable(false)
    .maximizable(false)
    .center()
    .build() {
        println!("About dialog opened");
    }
}

fn main() {
    // Start server BEFORE Tauri
    let server_child = start_server();

    if server_child.is_none() {
        eprintln!("ERROR: Failed to start server process!");
        eprintln!("Make sure you're running from the project directory with uv or python3 available.");
        std::process::exit(1);
    }

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(ServerProcess(Mutex::new(server_child)))
        .setup(|app| {
            // Create menu
            let menu = create_menu(app.handle())?;
            app.set_menu(menu)?;

            // Create loading window first
            let loading_url = format!("data:text/html,{}", urlencoding::encode(LOADING_HTML));
            let window = WebviewWindowBuilder::new(
                app,
                "main",
                WebviewUrl::External(loading_url.parse().unwrap())
            )
            .title("KJV Study")
            .inner_size(1200.0, 800.0)
            .min_inner_size(800.0, 600.0)
            .center()
            .title_bar_style(tauri::TitleBarStyle::Transparent)
            .build()?;

            // Wait for server in background, then navigate
            let window_clone = window.clone();
            std::thread::spawn(move || {
                if wait_for_server(30) {
                    let _ = window_clone.eval(&format!("window.location.href = '{}'", SERVER_URL));
                    println!("Navigated to server");
                } else {
                    let _ = window_clone.eval(
                        "document.body.innerHTML = '<h1 style=\"color:red;text-align:center;margin-top:100px\">Failed to start server</h1>'"
                    );
                }
            });

            Ok(())
        })
        .on_menu_event(|app, event| {
            let window = app.get_webview_window("main");

            match event.id().as_ref() {
                "about" => show_about_dialog(app),
                "website" => {
                    let _ = tauri_plugin_shell::ShellExt::shell(app).open("https://kjvstudy.org", None);
                }
                // Navigation
                "nav_home" => {
                    if let Some(w) = window { let _ = w.eval(&format!("window.location.href = '{}'", SERVER_URL)); }
                }
                "nav_books" => {
                    if let Some(w) = window { let _ = w.eval(&format!("window.location.href = '{}/books'", SERVER_URL)); }
                }
                "nav_search" => {
                    if let Some(w) = window { let _ = w.eval("document.querySelector('input[type=search]')?.focus()"); }
                }
                "nav_votd" => {
                    if let Some(w) = window { let _ = w.eval(&format!("window.location.href = '{}/verse-of-the-day'", SERVER_URL)); }
                }
                "nav_random" => {
                    if let Some(w) = window { let _ = w.eval(&format!("window.location.href = '{}/random'", SERVER_URL)); }
                }
                // Study
                "study_guides" => {
                    if let Some(w) = window { let _ = w.eval(&format!("window.location.href = '{}/study-guides'", SERVER_URL)); }
                }
                "topics" => {
                    if let Some(w) = window { let _ = w.eval(&format!("window.location.href = '{}/topics'", SERVER_URL)); }
                }
                "stories" => {
                    if let Some(w) = window { let _ = w.eval(&format!("window.location.href = '{}/stories'", SERVER_URL)); }
                }
                "strongs" => {
                    if let Some(w) = window { let _ = w.eval(&format!("window.location.href = '{}/strongs'", SERVER_URL)); }
                }
                "interlinear" => {
                    if let Some(w) = window { let _ = w.eval(&format!("window.location.href = '{}/interlinear'", SERVER_URL)); }
                }
                "reading_plans" => {
                    if let Some(w) = window { let _ = w.eval(&format!("window.location.href = '{}/reading-plans'", SERVER_URL)); }
                }
                // View
                "reload" => {
                    if let Some(w) = window { let _ = w.eval("window.location.reload()"); }
                }
                "back" => {
                    if let Some(w) = window { let _ = w.eval("window.history.back()"); }
                }
                "forward" => {
                    if let Some(w) = window { let _ = w.eval("window.history.forward()"); }
                }
                _ => {}
            }
        })
        .build(tauri::generate_context!())
        .expect("error while building tauri application")
        .run(|app_handle, event| {
            if let RunEvent::Exit = event {
                let state = app_handle.state::<ServerProcess>();
                if let Some(mut child) = state.0.lock().unwrap().take() {
                    println!("Shutting down server...");
                    let _ = child.kill();
                    let _ = child.wait();
                    println!("Server stopped.");
                };
            }
        });
}
