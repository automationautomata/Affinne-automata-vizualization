from PyQt6.QtWidgets import QApplication
from widgets.mainwindow import MainWindow
from sys import exit, argv

app = QApplication(argv)

# Создаём виджет Qt — окно.
window = MainWindow()
window.show()
# Запускаем цикл событий.
exit(app.exec())
