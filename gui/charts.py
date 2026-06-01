"""Компоненты для отображения графиков"""
import imgui
import numpy as np
from typing import List, Tuple


class SalesChart:
    """График продаж"""

    def __init__(self, max_data_points: int = 50):
        self.data_points = []
        self.max_points = max_data_points
        self.hovered_value = None

    def add_data_point(self, value: float):
        """Добавить точку данных"""
        self.data_points.append(value)
        if len(self.data_points) > self.max_points:
            self.data_points.pop(0)

    def draw(self, title: str, width: float = 0, height: float = 150):
        """Отрисовать график"""
        if len(self.data_points) < 2:
            imgui.text("Нет данных для отображения")
            return

        # Подготовка данных
        values = np.array(self.data_points)
        if values.max() == values.min():
            values = np.ones_like(values) * values.max()

        # Отрисовка графика
        draw_list = imgui.get_window_draw_list()
        cursor_pos = imgui.get_cursor_screen_pos()

        # Заголовок
        imgui.text(title)

        # График будет отрисован внутри области
        available = imgui.get_content_region_available()
        if width == 0:
            width = available.x
        if height == 0:
            height = min(available.y, 200)

        # Рамка
        imgui.dummy(width, height)

        # Отрисовка линий (простой вариант - через text, для реального графика нужен plot)
        # Используем встроенный plot lines из imgui
        imgui.plot_lines(
            f"##{title}",
            values.tolist(),
            graph_size=(width, height),
            overlay_text=f"Max: {values.max():.0f}"
        )

    def clear(self):
        """Очистить данные"""
        self.data_points.clear()


class PerformanceChart:
    """График производительности (мощность vs цена)"""

    def draw_comparison(self, cpu_power: int, ram_power: int, cpu_price: float, ram_price: float):
        """Отрисовать сравнение компонентов"""
        imgui.text("Анализ эффективности:")

        total_power = cpu_power + ram_power
        total_price = cpu_price + ram_price

        if total_price > 0:
            efficiency = total_power / total_price
            imgui.text(f"  Эффективность: {efficiency:.2f} ед./$")

        # Прогресс-бары для мощности
        imgui.text("  Распределение мощности:")
        progress_width = 200

        if total_power > 0:
            cpu_percent = cpu_power / total_power
            imgui.text(f"    CPU: {cpu_power} ед.")
            imgui.same_line()
            progress = imgui.progress_bar(cpu_percent, progress_width)

            imgui.text(f"    RAM: {ram_power} ед.")
            imgui.same_line()
            progress = imgui.progress_bar(ram_power / total_power, progress_width)

        imgui.separator()


class MarketMetricsChart:
    """График рыночных метрик"""

    def __init__(self):
        self.sales_history = []
        self.price_history = []
        self.reputation_history = []
        self.max_history = 20

    def update(self, sales: int, price: float, reputation: float):
        """Обновить исторические данные"""
        self.sales_history.append(sales)
        self.price_history.append(price)
        self.reputation_history.append(reputation)

        if len(self.sales_history) > self.max_history:
            self.sales_history.pop(0)
            self.price_history.pop(0)
            self.reputation_history.pop(0)

    def draw(self):
        """Отрисовать рыночные графики"""
        imgui.text("Рыночные метрики:")

        # График продаж
        if len(self.sales_history) > 1:
            imgui.plot_lines(
                "Продажи по неделям",
                self.sales_history,
                graph_size=(0, 80),
                scale_min=0
            )

        # График цены
        if len(self.price_history) > 1:
            imgui.plot_lines(
                "Цена по неделям",
                self.price_history,
                graph_size=(0, 80)
            )

        # График репутации
        if len(self.reputation_history) > 1:
            imgui.plot_lines(
                "Репутация по неделям",
                self.reputation_history,
                graph_size=(0, 80),
                scale_min=0,
                scale_max=1
            )