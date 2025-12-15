// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use std::time::Duration;
use tauri::{Manager, RunEvent, WebviewUrl, WebviewWindowBuilder};

struct ServerProcess(Mutex<Option<Child>>);

const SERVER_URL: &str = "http://127.0.0.1:31102";

fn start_server() -> Option<Child> {
    // Get the current working directory (project root in dev)
    let working_dir = std::env::current_dir().ok()?;

    println!("Starting KJV Study server...");
    println!("Working directory: {:?}", working_dir);

    // Try uv first (preferred), then fall back to python3
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
            Ok(response) => {
                println!("Server responded with status: {}", response.status());
            }
            Err(e) => {
                println!("Connection error: {}", e);
            }
        }
        std::thread::sleep(Duration::from_millis(500));
    }

    println!("Server failed to start after {} attempts", max_attempts);
    false
}

fn main() {
    // Start server BEFORE Tauri
    let server_child = start_server();

    if server_child.is_none() {
        eprintln!("ERROR: Failed to start server process!");
        eprintln!("Make sure you're running from the project directory with uv or python3 available.");
        std::process::exit(1);
    }

    // Wait for server to be ready
    if !wait_for_server(30) {
        eprintln!("ERROR: Server failed to become ready!");
        std::process::exit(1);
    }

    // Now start Tauri
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(ServerProcess(Mutex::new(server_child)))
        .setup(|app| {
            // Create window pointing to our server
            let _window = WebviewWindowBuilder::new(
                app,
                "main",
                WebviewUrl::External(SERVER_URL.parse().unwrap())
            )
            .title("KJV Study")
            .inner_size(1200.0, 800.0)
            .min_inner_size(800.0, 600.0)
            .center()
            .build()?;

            println!("Window created, loading {}", SERVER_URL);
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
                    println!("Server stopped.");
                };
            }
        });
}
