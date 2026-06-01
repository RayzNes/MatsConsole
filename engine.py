"""
Движок времени для игры
"""

from typing import Optional
from constructor import ConsoleBuild, ConstructorMenu


class TimeEngine:
    """Движок времени, управляющий игровым циклом"""

    def __init__(self, start_year: int = 1973):
        self.year = start_year
        self.month = 1
        self.week = 1
        self.balance = 100_000
        self.console_build: Optional[ConsoleBuild] = None

        self.months = [
            "января", "февраля", "марта", "апреля", "мая", "июня",
            "июля", "августа", "сентября", "октября", "ноября", "декабря"
        ]

    def next_week(self):
        """Пропустить одну неделю вперёд"""
        self.week += 1

        if self.week > 4:
            self.week = 1
            self.month += 1

            if self.month > 12:
                self.month = 1
                self.year += 1

        self.update_balance()

    def update_balance(self):
        """Обновить баланс (математическая модель)"""
        import random

        weekly_expenses = 1200
        market_fluctuation = random.randint(-500, 800)

        inflation_impact = 0
        if self.month % 3 == 0 and self.week == 1:
            inflation_impact = -int(self.balance * 0.02)

        delta = -weekly_expenses + market_fluctuation + inflation_impact
        self.balance += delta

        if self.balance < 0:
            self.balance = 0

    def get_date_string(self) -> str:
        """Получить строку с датой"""
        month_name = self.months[self.month - 1]
        week_num = self.week
        return f"{week_num}-я неделя {month_name} {self.year} года"

    def format_balance(self) -> str:
        """Отформатировать баланс"""
        return f"${self.balance:,.0f}".replace(",", " ")

    def display_status(self):
        """Отобразить текущий статус"""
        print(f"\n📅 {self.get_date_string()}")
        print(f"💰 Баланс: {self.format_balance()}")

        if self.console_build:
            print(f"🕹️  Консоль: {self.console_build.cpu.name if self.console_build.cpu else 'Нет'} + "
                  f"{self.console_build.ram.name if self.console_build.ram else 'Нет'}")

    def is_game_over(self) -> bool:
        """Проверить окончание игры"""
        if self.balance <= 0:
            print("\n💀 ИГРА ОКОНЧЕНА 💀")
            print("Вы обанкротились!")
            return True
        return False

    def run_constructor(self):
        """Запустить конструктор консоли"""
        print("\n🔨 ЗАПУСК КОНСТРУКТОРА КОНСОЛИ")
        print(f"📅 Текущий год: {self.year}")
        print(f"💰 Доступный бюджет: {self.format_balance()}")

        # Создаём конструктор с текущим годом
        menu = ConstructorMenu(self.year)
        build = menu.run()

        if build:
            self.console_build = build

            # Списываем стоимость сборки с баланса
            if self.balance >= build.calculate_total_cost():
                self.balance -= build.calculate_total_cost()
                print(f"\n💰 Стоимость сборки: ${build.calculate_total_cost():,.0f}")
                print(f"💰 Остаток на счету: {self.format_balance()}")
                print("🎮 Консоль успешно собрана и готова к использованию!")
            else:
                print(f"\n❌ НЕДОСТАТОЧНО СРЕДСТВ!")
                print(f"Требуется: ${build.calculate_total_cost():,.0f}")
                print(f"Доступно: {self.format_balance()}")
                print("Сборка отменена. Накопите больше денег и попробуйте снова.")
                self.console_build = None
        else:
            print("\n🚫 Сборка консоли отменена")

    def run(self):
        """Главный игровой цикл"""
        print("=" * 60)
        print("ЭКОНОМИЧЕСКИЙ СИМУЛЯТОР - РАЗРАБОТКА КОНСОЛИ")
        print("=" * 60)
        print(f"Старт: {self.get_date_string()}")
        print(f"Начальный баланс: {self.format_balance()}")
        print("-" * 60)
        print("Управление:")
        print("  Enter - пропустить неделю")
        print("  c - войти в конструктор консоли")
        print("  s - показать текущую сборку")
        print("  q - выйти из игры")
        print("=" * 60)

        self.display_status()

        while True:
            user_input = input("\n➤ Действие (Enter/c/s/q): ").lower()

            if user_input == 'q':
                print("\nИгра завершена.")
                print(f"Финальный баланс: {self.format_balance()}")
                break

            elif user_input == 'c':
                self.run_constructor()
                self.display_status()

            elif user_input == 's':
                if self.console_build:
                    self.console_build.display_build_info()
                else:
                    print("\n⚠️ Консоль ещё не собрана! Используйте 'c' для входа в конструктор.")
                self.display_status()

            else:  # Enter или любая другая клавиша
                self.next_week()
                self.display_status()

                if self.is_game_over():
                    break

        print("\n" + "=" * 60)
        print("Спасибо за игру!")
        print("=" * 60)