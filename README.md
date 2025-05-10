# PyWeb

A FastAPI-based web application that provides real-time command execution with WebSocket feedback. PyWeb allows running and monitoring system commands like network scanning (nmap) and connectivity testing (ping) through a web interface.

## Features

- WebSocket-based real-time communication
- Asyncio-powered command execution
- Stream command output directly to connected clients
- Ability to start and stop long-running processes
- Support for multiple concurrent tasks

## Requirements

- Python 3.12+
- FastAPI
- Socket-Pro (included as a wheel file)
- Uvicorn

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pyweb
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage

### Starting the Server

Run the application:

```bash
python main.py
```

The server will start on `http://0.0.0.0:8000` with automatic reload enabled.

### WebSocket Connection

Connect to the WebSocket endpoint at `/ws/122` to interact with the application.

### Available Commands

The application accepts JSON messages with the following formats:

#### Network Scanning

- Start an nmap scan:
  ```json
  {"data_type": "nmap-start"}
  ```

- Stop the running nmap scan:
  ```json
  {"data_type": "nmap-stop"}
  ```

#### Connectivity Testing

- Start pinging Google:
  ```json
  {"data_type": "ping-start"}
  ```

- Stop the running ping:
  ```json
  {"data_type": "ping-stop"}
  ```

## Project Structure

- main.py - FastAPI application and WebSocket handler
- __init__.py - Task management class for executing commands
- socket_pro-0.1.0-py3-none-any.whl - Custom WebSocket management library

## Security Considerations

This application runs system commands including those with `sudo`. Ensure proper permissions and security controls are in place before deploying in a production environment.




