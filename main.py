"""Главный файл игры - запуск веб-интерфейса"""
from web_gui import GameWebGUI

if __name__ == "__main__":
    gui = GameWebGUI()
    gui.run()