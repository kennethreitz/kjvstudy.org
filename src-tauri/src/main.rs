// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Child, Command};
use std::sync::Mutex;
use std::time::Duration;
use tauri::{AppHandle, Manager, RunEvent};

struct ServerProcess(Mutex<Option<Child>>);

fn find_python_executable(app: &AppHandle) -> Option<String> {
    // In development, use system Python
    if cfg!(debug_assertions) {
        return Some("python3".to_string());
    }

    // In production, look for bundled Python sidecar
    let resource_path = app.path().resource_dir().ok()?;

    #[cfg(target_os = "macos")]
    {
        let sidecar_path = resource_path.join("sidecar").join("kjvstudy-server");
        if sidecar_path.exists() {
            return Some(sidecar_path.to_string_lossy().to_string());
        }
    }

    #[cfg(target_os = "windows")]
    {
        let sidecar_path = resource_path.join("sidecar").join("kjvstudy-server.exe");
        if sidecar_path.exists() {
            return Some(sidecar_path.to_string_lossy().to_string());
        }
    }

    // Fallback to system Python
    Some("python3".to_string())
}

fn start_server(app: &AppHandle) -> Option<Child> {
    let python = find_python_executable(app)?;

    // Get the resource directory for data files
    let resource_dir = app.path().resource_dir().ok()?;

    // For development, use the project directory
    let working_dir = if cfg!(debug_assertions) {
        std::env::current_dir().ok()?
    } else {
        resource_dir.clone()
    };

    println!("Starting KJV Study server...");
    println!("Python executable: {}", python);
    println!("Working directory: {:?}", working_dir);

    let child = if python.ends_with("kjvstudy-server") || python.ends_with("kjvstudy-server.exe") {
        // Running bundled executable
        Command::new(&python)
            .current_dir(&working_dir)
            .env("KJVSTUDY_PORT", "31102")
            .spawn()
            .ok()?
    } else {
        // Running with Python interpreter (development)
        Command::new(&python)
            .args([
                "-m", "uvicorn",
                "kjvstudy_org.server:app",
                "--host", "127.0.0.1",
                "--port", "31102",
                "--log-level", "warning"
            ])
            .current_dir(&working_dir)
            .spawn()
            .ok()?
    };

    Some(child)
}

fn wait_for_server(max_attempts: u32) -> bool {
    let client = reqwest::blocking::Client::builder()
        .timeout(Duration::from_secs(1))
        .build()
        .unwrap();

    for attempt in 1..=max_attempts {
        println!("Waiting for server... (attempt {}/{})", attempt, max_attempts);

        match client.get("http://127.0.0.1:31102/api/health").send() {
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

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(ServerProcess(Mutex::new(None)))
        .setup(|app| {
            // Start the Python server
            let handle = app.handle().clone();

            if let Some(child) = start_server(&handle) {
                let state = app.state::<ServerProcess>();
                *state.0.lock().unwrap() = Some(child);

                // Wait for server to be ready
                if !wait_for_server(30) {
                    eprintln!("Warning: Server may not be fully ready");
                }
            } else {
                eprintln!("Failed to start server process");
            }

            // Navigate to the local server
            if let Some(window) = app.get_webview_window("main") {
                let _ = window.eval("window.location.href = 'http://127.0.0.1:31102'");
            }

            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("error while building tauri application")
        .run(|app_handle, event| {
            if let RunEvent::Exit = event {
                // Clean up: kill the server process
                let state = app_handle.state::<ServerProcess>();
                if let Some(mut child) = state.0.lock().unwrap().take() {
                    println!("Shutting down server...");
                    let _ = child.kill();
                    let _ = child.wait();
                };
            }
        });
}
