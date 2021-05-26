# this script was written by Erik Blank

import sys
from PyQt5 import QtGui, uic, QtWidgets
from datetime import datetime
import pandas as pd

# start program with python3 <scriptname> <userid> <tasknum>

FIELDS = ["timestamp", "user_id", "task", "event", "input"]


class Calculator(QtWidgets.QMainWindow):
    def __init__(self, userId, taskNum):
        super().__init__()
        self.userId = userId
        self.taskNum = taskNum
        self.expression = ""
        self.df = pd.DataFrame(columns=FIELDS)
        self.delete = "delete"
        self.clear = "clear"
        self.err = "Syntax Error"
        self.initUI()
        self.connectButtons()
        print("timestamp, user_id, task, event, input")

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
        self.df = self.df.to_csv(
            f"./data_{self.userId}_{self.taskNum}.csv", index=False)

    def connectButton(self, btn, text):
        btn.clicked.connect(lambda x: self.onClick(text, False))

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.logKLM("keyRelease", a0.text())
        return super().keyReleaseEvent(a0)

    def keyPressEvent(self, e):
        if e.key() == 16777220:
            self.onClick("=", True)
        elif e.key() == 16777219:
            self.onClick(self.delete, True)
        else:
            self.onClick(e.text(), True)

    def onClick(self, input, isKeyPress):
        if isKeyPress:
            self.logKLM("keyPress", input)
        else:
            self.logKLM("mouseClick", input)
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

    def logKLM(self, eventType, input):
        timestamp = datetime.now()
        print(f'{timestamp},{self.userId},{self.taskNum},{eventType},{input}')
        self.df = self.df.append({
            "timestamp": timestamp,
            "user_id": self.userId,
            "task": self.taskNum,
            "event": eventType,
            "input": input
        }, ignore_index=True)


def main():
    app = QtWidgets.QApplication(sys.argv)
    if len(sys.argv) != 3:
        print("usage: python3 <scriptname> <userID> <taskNum>")
    else:
        userId = str(sys.argv[1])
        taskNum = str(sys.argv[2])
    calculator = Calculator(userId, taskNum)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
