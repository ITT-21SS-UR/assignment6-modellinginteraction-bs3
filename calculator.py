import sys
from PyQt5 import QtGui, uic, QtWidgets
from datetime import datetime
import pandas as pd

FIELDS = ["timestamp", "event"]

class Calculator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.expression = ""
        self.df = pd.DataFrame(columns=FIELDS)
        self.delete = "delete"
        self.clear = "clear"
        self.err = "Syntax Error"
        self.initUI()
        self.connectButtons()
        print("timestamp,event")

    def initUI(self):
        self.ui = uic.loadUi("calculator.ui", self)
        self.ui.closeEvent = self.closeEvent
        self.ui.mouseReleaseEvent = self.mouseReleaseEvent
        self.ui.mouseMoveEvent = self.mouseMoveEvent
        self.setMouseTracking(True)
        self.show()

    def connectButtons(self):
        self.connectButton(self.ui.btn_0, "0")
        self.connectButton(self.ui.btn_1, "1")
        self.connectButton(self.ui.btn_2, "2")
        self.connectButton(self.ui.btn_3, "3")
        self.connectButton(self.ui.btn_4, "4")
        self.connectButton(self.ui.btn_5, "5")
        self.connectButton(self.ui.btn_6, "6")
        self.connectButton(self.ui.btn_7, "7")
        self.connectButton(self.ui.btn_8, "8")
        self.connectButton(self.ui.btn_9, "9")
        self.connectButton(self.ui.btn_multiply, "*")
        self.connectButton(self.ui.btn_divide, "/")
        self.connectButton(self.ui.btn_plus, "+")
        self.connectButton(self.ui.btn_minus, "-")
        self.connectButton(self.ui.btn_equal, "=")
        self.connectButton(self.ui.btn_dot, ".")
        self.connectButton(self.ui.btn_delete, self.delete)
        self.connectButton(self.ui.btn_clear, self.clear)

    def closeEvent(self, event):
        self.df = self.df.to_csv("./data.csv", index=False)
        
    
    def connectButton(self, btn, text):
        btn.clicked.connect(lambda x: self.onClick(text, False))

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.logKLM("keyRelease")
        return super().keyReleaseEvent(a0)

    def keyPressEvent(self, e):
        if e.key() == 16777220:
            self.onClick("=", True)
        elif e.key() == 16777219:
            self.onClick(self.clear, True)
        else:
            self.onClick(e.text(), True)

    def onClick(self, input, isKeyPress):
        if isKeyPress:
            self.logKLM("keyPress")
        else:
            self.logKLM("mouseClick")
        textField = self.ui.text_result
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        operators = [".", "*", "/", "+", "-"]
        inputs = numbers + operators

        if textField.text() == self.err:
            textField.setText("")

        if input in inputs:
            textField.setText(textField.text() + input)

        if input == "=":
            try:
                result = eval(textField.text())
                textField.setText(str(result))
            except SyntaxError:
                textField.setText(self.err)
        if input == self.clear:
            textField.setText("")

        if input == self.delete:
            textField.setText(textField.text()[:-1])

    def logKLM(self, eventType):
        timestamp = datetime.now()
        print(f'{timestamp},{eventType}')
        self.df = self.df.append({
            "timestamp": timestamp,
            "event": eventType
        }, ignore_index=True)


def main():
    app = QtWidgets.QApplication(sys.argv)
    calculator = Calculator()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
