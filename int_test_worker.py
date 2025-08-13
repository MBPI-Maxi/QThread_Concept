from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QPushButton,
    QVBoxLayout
)
   
from PyQt6.QtCore import (
    QThread,
    QObject,
    pyqtSignal,
    pyqtSlot
)  
import sys
import time

class Worker(QObject):
    argument_string = pyqtSignal(str)
    data_ready = pyqtSignal(object)

    @pyqtSlot()
    def process_thread(self):
        self.argument_string.emit(
            "Fetching data in the database"
        )

        # simulate database fetching (replace with real DB Query)
        time.sleep(2)
        
        # example data in the database
        fetched_data = {"name": "Alice", "age": 30, "email": "alice@example.com"}

        self.data_ready.emit(fetched_data)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.click_btn = QPushButton("Click Me")

        self.thread = None
        self.worker = Worker()

        # connect the function to the button
        self.click_btn.clicked.connect(self.connect_thread)
        
        self.main_layout.addWidget(self.click_btn)
        self.setLayout(self.main_layout)

    def connect_thread(self):
        # create thread and Worker instance here
        if not self.thread:
            self.thread = QThread()
        
            # always move the worker instance to the thread
            self.worker.moveToThread(self.thread)

            # Connect the thread started signal to worker process
            self.thread.started.connect(self.worker.process_thread)

            # Connect a callback function to the worker signal to slot argument_string(signal) in MainWindow
            self.worker.argument_string.connect(lambda msg: print({
                "Argument_string": msg
            }))

            # Connect a callback function to the worker signal to slot data_ready(signal) in MainWindow
            self.worker.data_ready.connect(lambda received_data: print({
                "Data_Ready": received_data
            }))

            # cleanup the thread
            self.thread.finished.connect(self.worker.deleteLater)
        
        # check if the thread is running
        if not self.thread.isRunning():
            self.thread.start()
        else:
            print("Thread is currently running")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_window = MainWindow()
    app_window.show()
    sys.exit(app.exec())
