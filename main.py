from PyQt6.QtWidgets import QApplication
from mainwindow import MainWindow
from sys import exit, argv

# Только для доступа к аргументам командной строки
# Приложению нужен один (и только один) экземпляр QApplication.
# Передаём sys.argv, чтобы разрешить 
# аргументы командной строки для приложения.
# Если не будете использовать аргументы командной строки, 
# QApplication([]) тоже работает
app = QApplication(argv)

# Создаём виджет Qt — окно.
window = MainWindow()
window.show()
# Запускаем цикл событий.
exit(app.exec())
