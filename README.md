# KJV Study

A web application for studying the King James Bible with AI-powered commentary and insights.

## Features

- Browse and search King James Bible verses
- AI-powered biblical commentary and insights
- Clean, responsive web interface
- Fast verse lookup and navigation

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```

## Usage

Run the development server:
```bash
uv run kjvstudy-org
```

The application will be available at http://localhost:8000

## Docker

Build and run with Docker:
```bash
docker build -t kjvstudy .
docker run -p 8000:8000 kjvstudy
```

## Requirements

- Python 3.13+
- FastAPI
- biblepy

## License

See LICENSE file for details.