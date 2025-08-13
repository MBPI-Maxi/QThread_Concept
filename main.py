from PyQt6.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
import sys
import time

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    error = pyqtSignal(str)
    resultReady = pyqtSignal(object)

    @pyqtSlot()
    def run(self):
        self.do_first_task()
        self.do_second_task()
        self.finished.emit()

    def do_first_task(self):
        # Simulate work and emit progress
        for i in range(1, 6):
            time.sleep(0.5)  # Simulate a time-consuming task
            self.progress.emit(i * 20)  # 20%, 40%, ...
    
    def do_second_task(self):
        # Simulate final task and emit result
        time.sleep(1)
        self.resultReady.emit("Task completed successfully!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Worker Thread Example")

        # UI setup
        self.button = QPushButton("Start Work")
        self.status_label = QLabel("Press start to begin.")
        self.progress_label = QLabel("Progress: 0%")
        self.result_label = QLabel("Result: N/A")

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect button to start worker thread
        self.button.clicked.connect(self.start_worker)

    def start_worker(self):
        self.button.setEnabled(False)
        self.status_label.setText("Working...")

        self.thread = QThread() # Create a new thread (QThread) where the worker will run separately from the main (UI) thread.
        self.worker = Worker() # Create a worker instance (Worker) that contains the actual work logic.
        self.worker.moveToThread(self.thread) # Move the worker object to the new thread, so its slots/signals execute in that thread instead of the main thread.

        self.thread.started.connect(self.worker.run) # When the thread starts, call the worker's run() method inside that thread. This triggers the worker to begin its tasks asynchronously.
        self.worker.finished.connect(self.thread.quit) # Stop the thread's event loop (thread.quit()) so the thread can clean up.
        self.worker.finished.connect(self.worker.deleteLater) # Schedule the worker object to be deleted safely (deleteLater()) to free resources.
        self.thread.finished.connect(self.thread.deleteLater) # Same with the thread

        self.worker.progress.connect(self.update_progress) # Update the progress display as the worker emits progress values.
        self.worker.resultReady.connect(self.show_result) # Show the final result when the worker finishes a task.
        self.worker.finished.connect(self.work_finished) # Handle cleanup or UI changes after work finishes.

        self.thread.start() # Start the thread’s event loop. This triggers the started signal, which calls worker.run() and kicks off the background work.

    def update_progress(self, val):
        self.progress_label.setText(f"Progress: {val}%")

    def show_result(self, result):
        self.result_label.setText(f"Result: {result}")

    def work_finished(self):
        self.status_label.setText("Work finished.")
        self.button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
