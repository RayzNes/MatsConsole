"""
Главный файл игры
Запускает экономический симулятор с конструктором консоли
"""

from engine import TimeEngine

def main():
    """Главная функция игры"""
    try:
        # Создаём и запускаем игровой движок
        game = TimeEngine(start_year=1973)
        game.run()
    except KeyboardInterrupt:
        print("\n\n👋 Игра прервана пользователем")
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
        print("Пожалуйста, перезапустите игру")

if __name__ == "__main__":
    main()