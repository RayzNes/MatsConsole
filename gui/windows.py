"""GUI окна для игры"""
import imgui
from typing import Optional, List
from ..components import CPU, RAM
from ..constructor import ConsoleBuild, ConstructorMenu
from ..market import SalesManager, Market


class GUIManager:
    """Менеджер GUI окон"""

    def __init__(self, time_engine):
        self.engine = time_engine
        self.active_window = "main"  # main, constructor, sales, history
        self.show_constructor = False
        self.show_sales = False
        self.show_history = False
        self.show_market = False

        # Временные данные для конструктора
        self.selected_cpu = None
        self.selected_ram = None
        self.available_cpus = []
        self.available_rams = []

        # Сообщения для пользователя
        self.message = ""
        self.message_timer = 0

    def update(self):
        """Обновление GUI (вызывается каждый кадр)"""
        self._draw_main_menu_bar()

        if self.show_constructor:
            self._draw_constructor_window()
        if self.show_sales:
            self._draw_sales_window()
        if self.show_history:
            self._draw_history_window()
        if self.show_market:
            self._draw_market_window()

        self._draw_main_dashboard()
        self._draw_messages()

    def _draw_main_menu_bar(self):
        """Отрисовать главное меню"""
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("Игра", True):
                _, self.show_constructor = imgui.menu_item(
                    "Конструктор консоли", None, self.show_constructor
                )
                _, self.show_sales = imgui.menu_item(
                    "Управление продажами", None, self.show_sales
                )
                _, self.show_market = imgui.menu_item(
                    "Анализ рынка", None, self.show_market
                )
                _, self.show_history = imgui.menu_item(
                    "Исторические события", None, self.show_history
                )
                imgui.separator()
                if imgui.menu_item("Выход", "Esc")[0]:
                    return False
                imgui.end_menu()

            if imgui.begin_menu("Помощь", True):
                imgui.text("Управление:")
                imgui.bullet_text("Enter - пропустить неделю")
                imgui.bullet_text("Используйте меню для доступа к функциям")
                imgui.end_menu()

            imgui.end_main_menu_bar()

    def _draw_main_dashboard(self):
        """Отрисовать главную панель с информацией о игре"""
        imgui.set_next_window_position(10, 40)
        imgui.set_next_window_collapsed(False)

        imgui.begin("Игровая панель", flags=imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_ALWAYS_AUTO_RESIZE)

        # Дата и баланс
        imgui.text_colored(self.engine.get_date_string(), 0.3, 0.8, 0.8, 1.0)
        balance_color = (0.2, 1.0, 0.2, 1.0) if self.engine.balance > 10000 else (1.0, 0.8, 0.2, 1.0)
        imgui.text_colored(f"Баланс: {self.engine.format_balance()}", *balance_color)

        imgui.separator()

        # Информация о консоли
        if self.engine.console_build and self.engine.console_build.is_complete():
            imgui.text_colored("Собранная консоль:", 0.5, 0.5, 0.5, 1.0)
            imgui.text(f"  CPU: {self.engine.console_build.cpu.name}")
            imgui.text(f"  RAM: {self.engine.console_build.ram.name}")
            imgui.text(f"  Мощность: {self.engine.console_build.calculate_total_power()} ед.")
            imgui.text(f"  Себестоимость: ${self.engine.console_build.calculate_total_cost():,.0f}")
        else:
            imgui.text_colored("Консоль не собрана", 0.8, 0.3, 0.3, 1.0)
            if imgui.button("Собрать консоль"):
                self.show_constructor = True

        imgui.separator()

        # Статус продаж
        if self.engine.sales_manager.is_selling:
            imgui.text_colored("Продажи: АКТИВНЫ", 0.2, 0.8, 0.2, 1.0)
            imgui.text(f"  Цена: ${self.engine.sales_manager.current_price:.0f}")
        else:
            imgui.text_colored("Продажи: ОСТАНОВЛЕНЫ", 0.8, 0.3, 0.3, 1.0)

        # Прогресс времени
        week_progress = self.engine.week / 4.0
        imgui.text(f"Неделя {self.engine.week}/4")
        imgui.progress_bar(week_progress, 150)

        imgui.end()

        # Кнопка следующей недели
        imgui.set_next_window_position(10, 300)
        imgui.begin("Действия", flags=imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_ALWAYS_AUTO_RESIZE)

        if imgui.button("Следующая неделя (Enter)", 200, 40):
            self.engine.next_week()

        imgui.end()

    def _draw_constructor_window(self):
        """Отрисовать окно конструктора консоли"""
        imgui.set_next_window_size(600, 500, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(400, 100)

        imgui.begin("Конструктор консоли", True, flags=imgui.WINDOW_NO_DOCKING)

        if imgui.button("Обновить компоненты"):
            self._refresh_components()

        imgui.separator()

        # Выбор CPU
        imgui.text_colored("Процессор (CPU)", 0.3, 0.8, 0.8, 1.0)
        if self.available_cpus:
            items = [f"{cpu.name} - ${cpu.price:,.0f} ({cpu.power} ед.)" for cpu in self.available_cpus]
            current = self.selected_cpu if self.selected_cpu else 0
            _, selected = imgui.listbox("##cpu_list", items, current, 5)
            if selected != current:
                self.selected_cpu = self.available_cpus[selected] if self.available_cpus else None
        else:
            imgui.text_colored("Нет доступных процессоров", 0.8, 0.3, 0.3, 1.0)

        imgui.separator()

        # Выбор RAM
        imgui.text_colored("Оперативная память (RAM)", 0.3, 0.8, 0.8, 1.0)
        if self.available_rams:
            items = [f"{ram.name} - ${ram.price:,.0f} ({ram.power} ед.)" for ram in self.available_rams]
            current = self.selected_ram if self.selected_ram else 0
            _, selected = imgui.listbox("##ram_list", items, current, 5)
            if selected != current:
                self.selected_ram = self.available_rams[selected] if self.available_rams else None
        else:
            imgui.text_colored("Нет доступных модулей памяти", 0.8, 0.3, 0.3, 1.0)

        imgui.separator()

        # Итоговая информация
        total_cost = 0
        if self.selected_cpu:
            total_cost += self.selected_cpu.price
        if self.selected_ram:
            total_cost += self.selected_ram.price

        imgui.text(f"Итоговая стоимость: ${total_cost:,.0f}")

        if total_cost > self.engine.balance:
            imgui.text_colored("Недостаточно средств!", 1.0, 0.3, 0.3, 1.0)

        imgui.separator()

        # Кнопки управления
        if imgui.button("Собрать консоль", 150, 30):
            if self.selected_cpu and self.selected_ram:
                if total_cost <= self.engine.balance:
                    build = ConsoleBuild(self.engine.year)
                    build.cpu = self.selected_cpu
                    build.ram = self.selected_ram
                    self.engine.console_build = build
                    self.engine.balance -= total_cost
                    self.message = f"Консоль успешно собрана! Стоимость: ${total_cost:,.0f}"
                    self.message_timer = 5
                    self.show_constructor = False
                else:
                    self.message = f"Недостаточно средств! Требуется: ${total_cost:,.0f}"
                    self.message_timer = 3
            else:
                self.message = "Выберите все компоненты!"
                self.message_timer = 2

        imgui.same_line()
        if imgui.button("Отмена", 100, 30):
            self.show_constructor = False

        imgui.end()

    def _draw_sales_window(self):
        """Отрисовать окно управления продажами"""
        imgui.set_next_window_size(500, 400, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(300, 100)

        imgui.begin("Управление продажами", True)

        # Статус продаж
        if self.engine.sales_manager.is_selling:
            imgui.text_colored("Статус: АКТИВНЫ", 0.2, 0.8, 0.2, 1.0)
            if imgui.button("Остановить продажи", 200, 30):
                self.engine.sales_manager.is_selling = False
        else:
            imgui.text_colored("Статус: ОСТАНОВЛЕНЫ", 0.8, 0.3, 0.3, 1.0)
            if imgui.button("Начать продажи", 200, 30):
                if self.engine.console_build and self.engine.console_build.is_complete():
                    self.engine.sales_manager.is_selling = True
                else:
                    self.message = "Сначала соберите консоль!"
                    self.message_timer = 2

        imgui.separator()

        # Настройка цены
        imgui.text("Цена:")
        _, price = imgui.slider_float(
            "##price_slider",
            self.engine.sales_manager.current_price,
            10, 500, "%.0f"
        )
        if price != self.engine.sales_manager.current_price:
            self.engine.sales_manager.current_price = price

        # Бюджет маркетинга
        imgui.text("Бюджет маркетинга:")
        _, budget = imgui.slider_float(
            "##budget_slider",
            self.engine.sales_manager.marketing_budget,
            0, 1000, "%.0f"
        )
        if budget != self.engine.sales_manager.marketing_budget:
            if budget <= self.engine.balance:
                self.engine.sales_manager.marketing_budget = budget
            else:
                self.message = "Недостаточно средств для такого бюджета!"
                self.message_timer = 2

        # Предполагаемая выручка
        if self.engine.console_build:
            sales = self.engine.market.calculate_sales(
                self.engine.console_build,
                self.engine.sales_manager.current_price,
                self.engine.sales_manager.marketing_budget
            )
            imgui.text_colored(f"Прогноз продаж: ~{sales} шт.", 0.5, 0.8, 0.5, 1.0)

        imgui.end()

    def _draw_history_window(self):
        """Отрисовать окно исторических событий"""
        imgui.set_next_window_size(500, 400, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(350, 100)

        imgui.begin("Исторические события", True)

        # Активные эффекты
        imgui.text_colored("Активные эффекты:", 0.3, 0.8, 0.8, 1.0)
        effects = self.engine.event_manager.game_state

        if effects.get("ram_cost_multiplier", 1.0) != 1.0:
            imgui.bullet_text(f"Стоимость памяти: {effects['ram_cost_multiplier'] * 100:.0f}% от базовой")
        if effects.get("market_size_multiplier", 1.0) != 1.0:
            imgui.bullet_text(f"Размер рынка: {effects['market_size_multiplier'] * 100:.0f}% от базового")
        if effects.get("production_cost_multiplier", 1.0) != 1.0:
            imgui.bullet_text(f"Стоимость производства: {effects['production_cost_multiplier'] * 100:.0f}% от базовой")
        if effects.get("crash_active"):
            imgui.bullet_text_colored("КРИЗИС 1983 АКТИВЕН!", 1.0, 0.3, 0.3, 1.0)

        imgui.separator()

        # Список произошедших событий
        imgui.text_colored("Произошедшие события:", 0.3, 0.8, 0.8, 1.0)
        if self.engine.event_manager.calendar.triggered_events:
            for event in self.engine.event_manager.calendar.triggered_events[-10:]:
                imgui.bullet_text(f"{event.month}.{event.year} - {event.title}")
                if imgui.is_item_hovered():
                    imgui.set_tooltip(event.description)
        else:
            imgui.text("Пока не произошло ни одного события")

        imgui.end()

    def _draw_market_window(self):
        """Отрисовать окно анализа рынка"""
        imgui.set_next_window_size(500, 400, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(400, 120)

        imgui.begin("Анализ рынка", True)

        if self.engine.console_build and self.engine.console_build.is_complete():
            demand_score = self.engine.market.calculate_demand_score(
                self.engine.console_build,
                self.engine.sales_manager.current_price
            )

            # Градусник спроса
            imgui.text(f"Спрос: {demand_score:.1f}/100")
            imgui.progress_bar(demand_score / 100.0, 300)

            # Репутация
            imgui.text(f"Репутация: {self.engine.market.reputation * 100:.1f}%")
            imgui.progress_bar(self.engine.market.reputation, 300)

            # Доля рынка
            imgui.text(f"Доля рынка: {self.engine.market.market_share * 100:.1f}%")
            imgui.progress_bar(self.engine.market.market_share, 300)

            # Всего продано
            imgui.text(f"Всего продано: {self.engine.market.total_sold} шт.")

            # Прогноз на следующую неделю
            sales = self.engine.market.calculate_sales(
                self.engine.console_build,
                self.engine.sales_manager.current_price,
                self.engine.sales_manager.marketing_budget
            )
            imgui.text_colored(f"Прогноз продаж: {sales} шт.", 0.5, 0.8, 0.5, 1.0)
        else:
            imgui.text_colored("Консоль не собрана. Нет данных для анализа.", 0.8, 0.5, 0.5, 1.0)

        imgui.end()

    def _draw_messages(self):
        """Отрисовать всплывающие сообщения"""
        if self.message_timer > 0:
            imgui.set_next_window_position(400, 500)
            imgui.begin("Сообщение", flags=imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_ALWAYS_AUTO_RESIZE)
            imgui.text_colored(self.message, 0.3, 0.8, 0.8, 1.0)
            imgui.end()
            self.message_timer -= 0.05

    def _refresh_components(self):
        """Обновить список доступных компонентов"""
        self.available_cpus = self.engine.db.get_available_cpus_by_year(self.engine.year)
        self.available_rams = self.engine.db.get_available_rams_by_year(self.engine.year)