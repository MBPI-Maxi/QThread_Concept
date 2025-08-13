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


# Without QThread (blocking main thread):
## [UI Thread] ---- run heavy task ---- UI updates
#            ↑ UI frozen during task ↑ 

# With QThread (non-blocking main thread):
# [UI Thread] ---- still responsive ---- receives signals → UI updates
# [Worker Thread] ---- runs heavy task ---- emits signals

class WorkerScript(QObject):
    print_statement = pyqtSignal(str)
    finished_thread = pyqtSignal()

    @pyqtSlot()
    def run_slot(self):
        self.run_print_statement()
        self.finished_thread.emit()

    def run_print_statement(self):
        self.print_statement.emit(
            "This is triggered in the worker class"
        )


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        
        self.thread = QThread()
        self.worker = WorkerScript()
        self.button = QPushButton("Click me")

        # ------------------------------------------------
        self.set_initial_config()
        self.connect_signals()
        self.set_widget_layout()

    def connect_signals(self):
        self.button.clicked.connect(self.thread.start)

        # Thread start triggers work (built-in signal .started)
        self.thread.started.connect(self.worker.run_slot)

        # Worker signals
        self.worker.print_statement.connect(lambda msg: print(msg)) # print_statement automatically returns a string value if it is a pyqtSignal(str)
        self.worker.finished_thread.connect(self.thread.quit)
        self.worker.finished_thread.connect(self.worker.deleteLater)

        # Thread cleanup (thread .finished built-in signal)
        self.thread.finished.connect(self.thread.deleteLater)
        
    def set_widget_layout(self):
        self.main_layout.addWidget(self.button)
        self.setLayout(self.main_layout)

    def set_initial_config(self):
        self.resize(800, 600)

    # def trigger_event(self):
    #     print("Clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = Main()
    main_app.show()
    sys.exit(app.exec())