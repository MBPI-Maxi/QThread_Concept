# PyQt6 Worker Thread Example

This is a simple PyQt6 application demonstrating how to run a long task in a separate thread using `QThread` and `QObject`.

## Features

- Runs a background worker in a separate thread to keep the UI responsive.
- Uses signals (`pyqtSignal`) to communicate progress, results, and completion back to the main thread.
- Safely cleans up thread and worker objects after finishing work.
- Updates a simple GUI with progress percentage and task results.

## How it works

- `Worker` class (inherits `QObject`) performs two sequential tasks inside the `run` method.
- `MainWindow` creates a `QThread` and moves the `Worker` instance into it.
- Signals from `Worker` update the GUI labels asynchronously.
- The start button is disabled during the work and re-enabled once finished.

## Running the app

Run the script with Python 3 and PyQt6 installed:

```bash
python main.py
