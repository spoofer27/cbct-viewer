from PySide6.QtCore import QObject, Signal, Slot
import traceback

class Worker(QObject):
    finished = Signal(object)      # result
    progress = Signal(int)         # 0–100
    error = Signal(str)

    def __init__(self, fn, *args):
        super().__init__()
        self.fn = fn
        self.args = args

    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, self.progress)
            self.finished.emit(result)
        except Exception:
            self.error.emit(traceback.format_exc())
