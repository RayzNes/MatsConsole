"""
Модуль рынка - модель спроса и продаж
"""

import random
from typing import Optional
from constructor import ConsoleBuild


class Market:
    """Класс, моделирующий рыночный спрос"""

    def __init__(self, total_buyers: int = 10000, event_manager=None):
        self.total_buyers = total_buyers  # Общее количество потенциальных покупателей
        self.market_share = 0.0  # Доля рынка, которую заняла консоль
        self.total_sold = 0  # Всего продано консолей за всё время
        self.reputation = 0.5  # Репутация компании (0-1), влияет на продажи
        self.market_trend = 0.0  # Тренд рынка (-0.2 до +0.2)
        self.event_manager = event_manager  # Ссылка на менеджер событий

    def calculate_demand_score(self, console: ConsoleBuild, price: float) -> float:
        """
        Рассчитать индекс привлекательности консоли (0-100)
        Формула учитывает: цену, мощность, год выпуска, репутацию, исторические события
        """
        if not console or not console.is_complete():
            return 0.0

        # Получаем чувствительность к цене из исторических событий
        price_sensitivity = 1.0
        if self.event_manager:
            price_sensitivity = self.event_manager.get_price_sensitivity()

        # Идеальная цена для расчёта (чем ниже, тем лучше)
        # Чем ниже цена, тем выше ценовой фактор
        price_factor = max(0, 1.0 - (price / 500.0) * price_sensitivity)

        # Фактор мощности (чем мощнее, тем лучше)
        power = console.calculate_total_power()
        power_factor = min(1.0, power / 100.0)

        # Фактор репутации (влияет на доверие покупателей)
        reputation_factor = self.reputation

        # Фактор времени - новые консоли привлекательнее
        time_factor = 1.0

        # Тренд рынка - общий интерес к играм
        market_trend_factor = 1.0 + self.market_trend

        # Исторический множитель размера рынка
        market_multiplier = 1.0
        if self.event_manager:
            market_multiplier = self.event_manager.get_market_multiplier()

        # Итоговый индекс привлекательности (0-100)
        demand_score = (
                               price_factor * 40 +  # Цена даёт до 40 баллов
                               power_factor * 35 +  # Мощность даёт до 35 баллов
                               reputation_factor * 15 +  # Репутация даёт до 15 баллов
                               time_factor * 10  # Время даёт до 10 баллов
                       ) * market_trend_factor * market_multiplier

        # Ограничиваем от 0 до 100
        return max(0.0, min(100.0, demand_score))

    def calculate_sales(self, console: ConsoleBuild, price: float,
                        marketing_budget: float = 0) -> int:
        """
        Рассчитать количество продаж за неделю

        Аргументы:
            console: собранная консоль
            price: установленная цена
            marketing_budget: бюджет на маркетинг в эту неделю

        Возвращает:
            количество проданных консолей
        """
        if not console or not console.is_complete():
            return 0

        # Базовая привлекательность
        demand_score = self.calculate_demand_score(console, price)

        # Маркетинг увеличивает продажи (до +50%)
        marketing_factor = 1.0 + (marketing_budget / 1000.0) * 0.5
        marketing_factor = min(1.5, marketing_factor)

        # Случайные колебания рынка
        random_factor = random.uniform(0.8, 1.2)

        # Исторический множитель размера рынка
        market_size = self.total_buyers
        if self.event_manager:
            market_size = int(self.total_buyers * self.event_manager.get_market_multiplier())

        # Процент рынка, который мы займём (от 0% до 15%)
        market_penetration = (demand_score / 100.0) * 0.15 * marketing_factor * random_factor

        # Количество продаж
        sales = int(market_size * market_penetration)

        # Небольшой эффект "сарафанного радио" - больше продаж = больше репутация
        if sales > 0:
            self.update_reputation(sales)

        # Обновляем общее количество проданных
        self.total_sold += sales

        # Обновляем долю рынка (с учётом исторического множителя)
        max_potential = market_size * 0.5
        if max_potential > 0:
            self.market_share = min(0.5, self.total_sold / max_potential)

        return sales

    def update_reputation(self, weekly_sales: int):
        """Обновить репутацию на основе продаж"""
        # Продажи увеличивают репутацию
        reputation_gain = (weekly_sales / self.total_buyers) * 0.1
        self.reputation = min(1.0, self.reputation + reputation_gain)

        # Со временем репутация немного падает, если нет продаж
        if weekly_sales == 0:
            self.reputation = max(0.0, self.reputation - 0.01)

    def update_market_trend(self):
        """Обновить тренд рынка (случайные колебания)"""
        # Рынок может расти или падать
        change = random.uniform(-0.05, 0.05)
        self.market_trend += change
        self.market_trend = max(-0.2, min(0.2, self.market_trend))

    def get_reputation_history(self):
        """Вернуть историю репутации (для графика)"""
        # Здесь можно хранить историю, но для простоты возвращаем текущее значение
        return self.reputation

    def display_market_info(self, console: ConsoleBuild, price: float):
        """Отобразить информацию о рынке"""
        print("\n" + "=" * 60)
        print("ИНФОРМАЦИЯ О РЫНКЕ")
        print("=" * 60)

        if console and console.is_complete():
            demand_score = self.calculate_demand_score(console, price)
            print(f"📊 Индекс привлекательности: {demand_score:.1f}/100")
            print(f"⭐ Репутация компании: {self.reputation * 100:.1f}%")
            print(f"📈 Тренд рынка: {self.market_trend * 100:+.1f}%")
            print(f"📦 Всего продано: {self.total_sold} шт.")
            print(f"🏆 Доля рынка: {self.market_share * 100:.1f}%")

            if self.event_manager:
                multiplier = self.event_manager.get_market_multiplier()
                if multiplier != 1.0:
                    print(f"📉 Исторический множитель рынка: {multiplier * 100:.0f}%")
        else:
            print("❌ Консоль не собрана. Невозможно выйти на рынок.")

        print("=" * 60)


class SalesManager:
    """Управление продажами и ценообразованием"""

    def __init__(self, market: Market):
        self.market = market
        self.current_price = 150.0  # Цена по умолчанию $150
        self.marketing_budget = 0.0
        self.is_selling = False  # Идут ли продажи

    def set_price(self):
        """Интерактивная установка цены"""
        print(f"\n💰 ТЕКУЩАЯ ЦЕНА: ${self.current_price:.0f}")

        while True:
            try:
                new_price = input("Введите новую цену (или Enter для отмены): $")
                if new_price == "":
                    return

                new_price = float(new_price)
                if new_price < 10:
                    print("❌ Цена не может быть ниже $10 (себестоимость)")
                elif new_price > 1000:
                    print("❌ Цена не может быть выше $1000 (рынок не выдержит)")
                else:
                    self.current_price = new_price
                    print(f"✅ Цена установлена: ${self.current_price:.0f}")
                    return
            except ValueError:
                print("❌ Пожалуйста, введите число")

    def set_marketing_budget(self, current_balance: float):
        """Установить бюджет на маркетинг"""
        print(f"\n📢 ТЕКУЩИЙ БЮДЖЕТ МАРКЕТИНГА: ${self.marketing_budget:.0f}")
        print(f"💰 Доступно средств: ${current_balance:,.0f}")

        while True:
            try:
                budget = input("Введите бюджет на маркетинг в эту неделю (0-1000): $")
                if budget == "":
                    return

                budget = float(budget)
                if budget < 0:
                    print("❌ Бюджет не может быть отрицательным")
                elif budget > 1000:
                    print("❌ Слишком большой бюджет (максимум $1000 в неделю)")
                elif budget > current_balance:
                    print(f"❌ Недостаточно средств! Доступно: ${current_balance:,.0f}")
                else:
                    self.marketing_budget = budget
                    print(f"✅ Бюджет маркетинга установлен: ${self.marketing_budget:.0f}")
                    return
            except ValueError:
                print("❌ Пожалуйста, введите число")

    def process_weekly_sales(self, console: Optional[ConsoleBuild]) -> tuple:
        """
        Обработать продажи за неделю

        Возвращает:
            (количество продаж, доход от продаж)
        """
        if not self.is_selling:
            return 0, 0.0

        if not console or not console.is_complete():
            print("⚠️ Нельзя продавать - консоль не собрана!")
            self.is_selling = False
            return 0, 0.0

        # Рассчитываем продажи
        sales = self.market.calculate_sales(console, self.current_price, self.marketing_budget)

        # Доход от продаж
        revenue = sales * self.current_price

        # Затраты на маркетинг
        marketing_cost = self.marketing_budget

        # Обновляем тренд рынка
        self.market.update_market_trend()

        # Сброс маркетингового бюджета на следующую неделю
        self.marketing_budget = 0

        return sales, revenue - marketing_cost

    def display_sales_menu(self):
        """Отобразить меню управления продажами"""
        print("\n" + "=" * 60)
        print("УПРАВЛЕНИЕ ПРОДАЖАМИ")
        print("=" * 60)
        print(f"Статус: {'🟢 ПРОДАЖИ АКТИВНЫ' if self.is_selling else '🔴 ПРОДАЖИ ОСТАНОВЛЕНЫ'}")
        print(f"Цена: ${self.current_price:.0f}")
        print(f"Бюджет маркетинга: ${self.marketing_budget:.0f}")
        print("-" * 60)
        print("1. Включить/выключить продажи")
        print("2. Изменить цену")
        print("3. Установить бюджет маркетинга")
        print("4. Показать анализ рынка")
        print("0. Вернуться в главное меню")
        print("=" * 60)

    def run_sales_menu(self, console: Optional[ConsoleBuild], current_balance: float) -> bool:
        """
        Запустить меню управления продажами

        Возвращает:
            True если нужно обновить баланс, False если нет
        """
        while True:
            self.display_sales_menu()
            choice = input("\nВаш выбор: ")

            if choice == "1":
                self.is_selling = not self.is_selling
                status = "ВКЛЮЧЕНЫ" if self.is_selling else "ВЫКЛЮЧЕНЫ"
                print(f"\n✅ Продажи {status}")
                return False

            elif choice == "2":
                self.set_price()
                return False

            elif choice == "3":
                self.set_marketing_budget(current_balance)
                return False

            elif choice == "4":
                self.market.display_market_info(console, self.current_price)
                return False

            elif choice == "0":
                return False

            else:
                print("\n❌ Неверный выбор")