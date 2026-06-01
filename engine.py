"""
Движок времени для игры
"""

from typing import Optional
from constructor import ConsoleBuild, ConstructorMenu
from market import Market, SalesManager


class TimeEngine:
    """Движок времени, управляющий игровым циклом"""

    def __init__(self, start_year: int = 1973):
        self.year = start_year
        self.month = 1
        self.week = 1
        self.balance = 100_000
        self.console_build: Optional[ConsoleBuild] = None

        # Добавляем рыночные механизмы
        self.market = Market(total_buyers=10000)
        self.sales_manager = SalesManager(self.market)

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
        """Обновить баланс (математическая модель с учётом продаж)"""
        import random

        # Базовые еженедельные расходы (аренда, зарплаты и т.д.)
        weekly_expenses = 1200

        # Расходы на производство консолей (если продажи активны)
        production_costs = 0
        if self.sales_manager.is_selling and self.console_build and self.console_build.is_complete():
            # Получаем продажи за неделю
            sales, net_revenue = self.sales_manager.process_weekly_sales(self.console_build)

            # Добавляем доход от продаж
            weekly_expenses -= net_revenue

            if sales > 0:
                print(f"\n📈 ПРОДАЖИ ЗА НЕДЕЛЮ:")
                print(f"   Продано: {sales} шт.")
                print(f"   Выручка: ${net_revenue + self.sales_manager.marketing_budget:,.0f}")
                print(f"   Маркетинг: ${self.sales_manager.marketing_budget:,.0f}")
                print(f"   Чистый доход: ${net_revenue:,.0f}")

        # Рыночные колебания
        market_fluctuation = random.randint(-500, 800)

        # Инфляция
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
        print(f"\n{'=' * 60}")
        print(f"📅 {self.get_date_string()}")
        print(f"💰 Баланс: {self.format_balance()}")

        if self.console_build and self.console_build.is_complete():
            print(f"🕹️  Консоль: {self.console_build.cpu.name} + {self.console_build.ram.name}")
            print(f"⚡ Мощность: {self.console_build.calculate_total_power()} ед.")

        # Статус продаж
        if self.sales_manager.is_selling and self.console_build and self.console_build.is_complete():
            print(f"🟢 ПРОДАЖИ АКТИВНЫ (Цена: ${self.sales_manager.current_price:.0f})")
        elif self.console_build and self.console_build.is_complete():
            print(f"🔴 ПРОДАЖИ ОСТАНОВЛЕНЫ")

        print(f"{'=' * 60}")

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

        # Проверяем, есть ли уже собранная консоль
        if self.console_build and self.console_build.is_complete():
            print("\n⚠️ У вас уже есть собранная консоль!")
            overwrite = input("Хотите собрать новую (старая будет утеряна)? (y/n): ")
            if overwrite.lower() != 'y':
                print("Сборка отменена")
                return

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

                # Автоматически предлагаем начать продажи
                start_sales = input("\nХотите начать продажи сейчас? (y/n): ")
                if start_sales.lower() == 'y':
                    self.sales_manager.is_selling = True
                    print("✅ Продажи активированы!")
                    self.run_sales_menu()
            else:
                print(f"\n❌ НЕДОСТАТОЧНО СРЕДСТВ!")
                print(f"Требуется: ${build.calculate_total_cost():,.0f}")
                print(f"Доступно: {self.format_balance()}")
                print("Сборка отменена. Накопите больше денег и попробуйте снова.")
                self.console_build = None
        else:
            print("\n🚫 Сборка консоли отменена")

    def run_sales_menu(self):
        """Запустить меню управления продажами"""
        self.sales_manager.run_sales_menu(self.console_build, self.balance)

    def run(self):
        """Главный игровой цикл"""
        print("=" * 60)
        print("ЭКОНОМИЧЕСКИЙ СИМУЛЯТОР - РАЗРАБОТКА КОНСОЛИ")
        print("=" * 60)
        print(f"Старт: {self.get_date_string()}")
        print(f"Начальный баланс: {self.format_balance()}")
        print("-" * 60)
        print("УПРАВЛЕНИЕ:")
        print("  Enter - пропустить неделю (автоматические продажи)")
        print("  c - войти в конструктор консоли")
        print("  s - показать текущую сборку")
        print("  m - управление продажами и ценой")
        print("  i - информация о рынке")
        print("  q - выйти из игры")
        print("=" * 60)

        self.display_status()

        while True:
            user_input = input("\n➤ Действие (Enter/c/s/m/i/q): ").lower()

            if user_input == 'q':
                print("\nИгра завершена.")
                print(f"Финальный баланс: {self.format_balance()}")
                if self.market.total_sold > 0:
                    print(f"Всего продано консолей: {self.market.total_sold}")
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

            elif user_input == 'm':
                if self.console_build and self.console_build.is_complete():
                    self.run_sales_menu()
                    self.display_status()
                else:
                    print("\n⚠️ Сначала соберите консоль ('c')!")
                    self.display_status()

            elif user_input == 'i':
                self.market.display_market_info(self.console_build,
                                                self.sales_manager.current_price)
                self.display_status()

            else:  # Enter или любая другая клавиша - пропуск недели
                self.next_week()
                self.display_status()

                if self.is_game_over():
                    break

        print("\n" + "=" * 60)
        print("Спасибо за игру!")
        print("=" * 60)