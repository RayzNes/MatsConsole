"""Стили и темы для Dear ImGui"""
import imgui


def apply_style():
    """Применить современный стиль для окна игры"""
    style = imgui.get_style()

    # Цветовая схема (тёмная тема с акцентами)
    colors = style.colors

    # Основные цвета
    colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.08, 0.08, 0.10, 1.0)
    colors[imgui.COLOR_FRAME_BACKGROUND] = (0.15, 0.15, 0.18, 1.0)
    colors[imgui.COLOR_FRAME_BACKGROUND_HOVERED] = (0.20, 0.20, 0.25, 1.0)
    colors[imgui.COLOR_FRAME_BACKGROUND_ACTIVE] = (0.25, 0.25, 0.30, 1.0)

    # Акцентный цвет (сине-зелёный)
    accent = (0.20, 0.70, 0.70, 1.0)
    colors[imgui.COLOR_BUTTON] = accent
    colors[imgui.COLOR_BUTTON_HOVERED] = (0.30, 0.80, 0.80, 1.0)
    colors[imgui.COLOR_BUTTON_ACTIVE] = (0.15, 0.60, 0.60, 1.0)

    colors[imgui.COLOR_CHECK_MARK] = accent
    colors[imgui.COLOR_SLIDER_GRAB] = accent
    colors[imgui.COLOR_SLIDER_GRAB_ACTIVE] = (0.30, 0.80, 0.80, 1.0)

    # Заголовки окон
    colors[imgui.COLOR_TITLE_BACKGROUND] = (0.12, 0.12, 0.14, 1.0)
    colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE] = (0.15, 0.15, 0.18, 1.0)

    # Текст
    colors[imgui.COLOR_TEXT] = (0.95, 0.95, 0.97, 1.0)

    # Разделители
    colors[imgui.COLOR_BORDER] = (0.30, 0.30, 0.35, 1.0)

    # Настройки округления углов
    style.window_rounding = 5.0
    style.frame_rounding = 4.0
    style.popup_rounding = 4.0
    style.scrollbar_rounding = 4.0
    style.grab_rounding = 4.0

    # Отступы
    style.window_padding = (10, 10)
    style.frame_padding = (8, 6)
    style.item_spacing = (8, 6)