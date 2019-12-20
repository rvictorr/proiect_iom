from PyQt5.QtWidgets import QApplication
from CoolWindow import CoolWindow


# Function to run App
def run():
    app = QApplication([])
    mainWindow = CoolWindow()
    mainWindow.show()
    app.exec()


if __name__ == "__main__":
    run()



