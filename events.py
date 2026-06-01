"""
Исторический календарь событий
Система триггеров, привязанных к датам
"""

from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GameEvent:
    """Класс исторического события"""
    year: int
    month: int
    title: str
    description: str
    effects: Dict[str, Any]
    triggered: bool = False


class EventCalendar:
    """Календарь исторических событий"""

    def __init__(self):
        self.events: List[GameEvent] = []
        self.triggered_events: List[GameEvent] = []
        self._init_historical_events()

    def _init_historical_events(self):
        """Инициализация исторических событий 1973-1983"""

        # 1973 год
        self.events.append(GameEvent(
            year=1973, month=1,
            title="💡 ЭРА ПОЛУПРОВОДНИКОВ",
            description="Старт массового производства микросхем RAM емкостью 4 Кбит.",
            effects={"ram_cost_reduction": 0.85, "message": "Себестоимость памяти снижена на 15%!"}
        ))

        self.events.append(GameEvent(
            year=1973, month=2,
            title="🕹️ РОЖДЕНИЕ АРКАД",
            description="Игра Pong от Atari захватывает бары и торговые центры США.",
            effects={"market_growth": 1.2, "message": "Потенциальных покупателей стало на 20% больше!"}
        ))

        self.events.append(GameEvent(
            year=1973, month=10,
            title="📉 НЕФТЯНОЙ КРИЗИС",
            description="Глобальный нефтяной кризис. Стагфляция в США и Европе.",
            effects={"price_sensitivity": 1.5, "inflation_boost": 0.5,
                     "message": "Покупательская способность упала! Цена стала критически важна."}
        ))

        # 1974 год
        self.events.append(GameEvent(
            year=1974, month=4,
            title="💡 INTEL 8080",
            description="Intel выпускает легендарный 8-битный процессор Intel 8080.",
            effects={"new_cpu_available": "Intel 8080", "message": "В базе компонентов появился мощный процессор!"}
        ))

        self.events.append(GameEvent(
            year=1974, month=6,
            title="🕹️ ПЕРВЫЙ КОНКУРЕНТ",
            description="Magnavox выпускает обновленную домашнюю консоль Odyssey 100/200.",
            effects={"competitor_strength": 0.3, "message": "Появился первый слабый конкурент!"}
        ))

        self.events.append(GameEvent(
            year=1974, month=11,
            title="🌍 DUNGEONS & DRAGONS",
            description="Всплеск популярности настольной игры Dungeons & Dragons.",
            effects={"niche_segment": "hardcore", "message": "Сформировался сегмент 'гиков', требующих сложные игры!"}
        ))

        # 1975 год
        self.events.append(GameEvent(
            year=1975, month=3,
            title="💡 MOS 6502 - РЕВОЛЮЦИЯ",
            description="MOS Technology выпускает дешевый процессор MOS 6502 за $25!",
            effects={"new_cpu_available": "MOS 6502", "message": "Доступен дешевый и мощный процессор MOS 6502!"}
        ))

        self.events.append(GameEvent(
            year=1975, month=9,
            title="🕹️ HOME PONG",
            description="Выходит домашняя версия Home Pong от Atari.",
            effects={"christmas_boost": 2.0, "message": "Рождественский сезон принесет удвоение продаж!"}
        ))

        self.events.append(GameEvent(
            year=1975, month=12,
            title="🌍 ОСНОВАНИЕ MICROSOFT",
            description="Основана корпорация Microsoft. Начинается коммерческая эпоха ПО.",
            effects={"developer_cost": 1.2, "message": "Стоимость найма программистов выросла на 20%!"}
        ))

        # 1976 год
        self.events.append(GameEvent(
            year=1976, month=5,
            title="💡 ZILOG Z80",
            description="Появление процессора Zilog Z80.",
            effects={"new_cpu_available": "Zilog Z80", "message": "Доступен гибкий процессор Zilog Z80!"}
        ))

        self.events.append(GameEvent(
            year=1976, month=8,
            title="🕹️ ПЕРВЫЕ КАРТРИДЖИ",
            description="Fairchild Channel F - первая консоль на сменных картриджах.",
            effects={"unlock_cartridges": True, "message": "Технология картриджей открыта! Игры стали сменными."}
        ))

        self.events.append(GameEvent(
            year=1976, month=10,
            title="📉 ВСПЛЕСК ИНФЛЯЦИИ",
            description="Инфляция в США достигает 5.8%.",
            effects={"production_cost": 1.15, "message": "Стоимость производства выросла на 15%!"}
        ))

        # 1977 год
        self.events.append(GameEvent(
            year=1977, month=1,
            title="💡 ЦВЕТНОЕ ТВ",
            description="Падение цен на цветные телевизоры в США.",
            effects={"color_demand": True, "message": "Черно-белые игры теперь не привлекают покупателей!"}
        ))

        self.events.append(GameEvent(
            year=1977, month=6,
            title="🕹️ ATARI 2600",
            description="Выход легендарной Atari 2600 (Atari VCS).",
            effects={"competitor_strength": 1.0, "main_competitor": "Atari 2600",
                     "message": "⚠️ Atari 2600 вышла на рынок! Сильный конкурент!"}
        ))

        self.events.append(GameEvent(
            year=1977, month=7,
            title="🌍 ЗВЕЗДНЫЕ ВОЙНЫ",
            description="Премьера фильма 'Звездные войны: Новая надежда'.",
            effects={"space_bonus": 1.5,
                     "message": "Бум на космическую тематику! Космические игры получают +50% к привлекательности."}
        ))

        # 1978 год
        self.events.append(GameEvent(
            year=1978, month=6,
            title="💡 SPACE INVADERS",
            description="Релиз аркадного автомата Space Invaders.",
            effects={"market_doubling": True, "message": "Игровой бум! Аудитория рынка удваивается!"}
        ))

        self.events.append(GameEvent(
            year=1978, month=9,
            title="🕹️ MAGNAVOX ODYSSEY²",
            description="Выходит консоль Magnavox Odyssey² с клавиатурой.",
            effects={"competitor_strength": 0.5, "message": "Конкуренты начинают использовать необычные фичи."}
        ))

        self.events.append(GameEvent(
            year=1978, month=12,
            title="🌍 ОТКРЫТИЕ CES",
            description="Выставка CES в Лас-Вегасе становится главной игровой площадкой.",
            effects={"expo_available": True, "message": "Доступно участие в выставках для хайпа!"}
        ))

        # 1979 год
        self.events.append(GameEvent(
            year=1979, month=3,
            title="💡 MOTOROLA 68000",
            description="Motorola выпускает 16/32-битный процессор.",
            effects={"new_cpu_available": "Motorola 68000", "message": "Доступен мощный, но дорогой Motorola 68000!"}
        ))

        self.events.append(GameEvent(
            year=1979, month=8,
            title="🕹️ РОЖДЕНИЕ ЖАНРОВ",
            description="На Atari 2600 выходит игра Adventure.",
            effects={"gameplay_demand": True, "message": "Игроки теперь ценят глубину геймплея, а не только графику!"}
        ))

        self.events.append(GameEvent(
            year=1979, month=12,
            title="📉 ВТОРОЙ НЕФТЯНОЙ КРИЗИС",
            description="Иранская революция вызвала новый виток инфляции.",
            effects={"production_cost": 1.2, "message": "Заводы повысили стоимость производства!"}
        ))

        # 1980 год
        self.events.append(GameEvent(
            year=1980, month=4,
            title="💡 PAC-MAN",
            description="Namco выпускает аркадный автомат Pac-Man.",
            effects={"casual_segment": True, "message": "Рынок казуальных игроков (женщины и дети) резко вырос!"}
        ))

        self.events.append(GameEvent(
            year=1980, month=10,
            title="🕹️ INTELLIVISION",
            description="Mattel выпускает консоль Intellivision с 16-битной графикой.",
            effects={"competitor_strength": 0.8, "graphics_wars": True,
                     "message": "Начало маркетинговых 'войн графики'!"}
        ))

        self.events.append(GameEvent(
            year=1980, month=12,
            title="🌍 ОСНОВАНИЕ ACTIVISION",
            description="Первый независимый сторонний издатель.",
            effects={"third_party_available": True, "message": "Теперь игры могут писать сторонние студии!"}
        ))

        # 1981 год
        self.events.append(GameEvent(
            year=1981, month=8,
            title="💡 ЭРА ПК",
            description="Появление IBM PC. ПК входят в дома.",
            effects={"pc_competition": 0.7, "message": "Появился скрытый конкурент - персональные компьютеры!"}
        ))

        self.events.append(GameEvent(
            year=1981, month=12,
            title="🕹️ DONKEY KONG",
            description="Nintendo выпускает Donkey Kong.",
            effects={"system_seller_concept": True,
                     "message": "Родилось понятие 'систем-селлер' (игра, ради которой покупают консоль)!"}
        ))

        # 1982 год
        self.events.append(GameEvent(
            year=1982, month=3,
            title="💡 ЭРА ЗВУКА",
            description="Внедрение микросхем звуковых генераторов (SID).",
            effects={"sound_importance": True, "message": "Звук стал критически важен для привлекательности консоли!"}
        ))

        self.events.append(GameEvent(
            year=1982, month=6,
            title="🕹️ COLECOVISION",
            description="Выходит мощная консоль ColecoVision.",
            effects={"competitor_strength": 0.9, "message": "Технологическая планка поднята до предела!"}
        ))

        self.events.append(GameEvent(
            year=1982, month=9,
            title="📉 КРИЗИС ДОВЕРИЯ",
            description="Рынок перенасыщен низкокачественными играми.",
            effects={"retailer_trust": 0.5, "message": "Магазины неохотно берут новые консоли!"}
        ))

        # 1983 год - ВЕЛИКИЙ КРАХ
        self.events.append(GameEvent(
            year=1983, month=5,
            title="💡 ДИСКЕТЫ",
            description="Падение цен на дискеты и дисководы.",
            effects={"alternative_media": True, "message": "Появился дешевый носитель данных вместо картриджей!"}
        ))

        self.events.append(GameEvent(
            year=1983, month=7,
            title="🕹️ NINTENDO FAMICOM",
            description="В Японии выходит Nintendo Famicom (будущая NES).",
            effects={"future_monopoly": True, "message": "В Азии родился будущий монополист!"}
        ))

        self.events.append(GameEvent(
            year=1983, month=12,
            title="💥 ВЕЛИКИЙ КРАХ ВИДЕОИГР",
            description="Крах индустрии в США. Atari банкротится. Рынок падает на 85%!",
            effects={"market_crash": 0.15, "crash_active": True,
                     "message": "⚠️⚠️⚠️ КРИЗИС! Спрос в США упал на 85%! Срочно ищите новые рынки!"}
        ))

    def check_events(self, year: int, month: int) -> List[GameEvent]:
        """Проверить и вернуть события для указанной даты"""
        triggered = []

        for event in self.events:
            if not event.triggered and event.year == year and event.month == month:
                event.triggered = True
                self.triggered_events.append(event)
                triggered.append(event)

        return triggered

    def apply_event_effects(self, event: GameEvent, game_state: Dict) -> Dict:
        """Применить эффекты события к игровому состоянию"""
        effects = event.effects.copy()

        # Специальные эффекты для разных типов событий
        if "ram_cost_reduction" in effects:
            game_state["ram_cost_multiplier"] = game_state.get("ram_cost_multiplier", 1.0) * effects[
                "ram_cost_reduction"]

        if "market_growth" in effects:
            game_state["market_size_multiplier"] = game_state.get("market_size_multiplier", 1.0) * effects[
                "market_growth"]

        if "price_sensitivity" in effects:
            game_state["price_sensitivity"] = effects["price_sensitivity"]

        if "production_cost" in effects:
            game_state["production_cost_multiplier"] = game_state.get("production_cost_multiplier", 1.0) * effects[
                "production_cost"]

        # Исправляем - передаём month через параметр
        # В этом методе нет month, поэтому нужно передавать его отдельно

        return game_state


class EventManager:
    """Менеджер событий для интеграции с игрой"""

    def __init__(self):
        self.calendar = EventCalendar()
        self.game_state = {
            "ram_cost_multiplier": 1.0,
            "market_size_multiplier": 1.0,
            "production_cost_multiplier": 1.0,
            "price_sensitivity": 1.0,
            "crash_active": False,
            "space_bonus_active": False,
            "space_bonus_multiplier": 1.0,
            "temporary_boost": 1.0
        }
        self.active_crisis = False
        self.crisis_end_year = 0

    def update(self, year: int, month: int) -> List[GameEvent]:
        """Обновить состояние событий для текущей даты"""
        triggered_events = self.calendar.check_events(year, month)

        for event in triggered_events:
            print("\n" + "=" * 60)
            print(f"📜 ИСТОРИЧЕСКОЕ СОБЫТИЕ: {event.title}")
            print("=" * 60)
            print(f"📅 {event.month}.{event.year}")
            print(f"📖 {event.description}")
            print(f"✨ Эффект: {event.effects.get('message', '---')}")
            print("=" * 60)

            # Применяем эффекты - убираем month, которого нет в параметрах метода
            self.game_state = self.calendar.apply_event_effects(event, self.game_state)

            # Специальная обработка кризиса 1983
            if event.effects.get("crash_active"):
                self.active_crisis = True
                self.crisis_end_year = 1985
                print("\n💀 ВНИМАНИЕ! РЫНОК В США РУХНУЛ!")
                print("Рекомендация: ищите рынки в Европе или заморозьте производство!")

        # Проверяем окончание кризиса
        if self.active_crisis and year >= self.crisis_end_year:
            self.active_crisis = False
            print("\n" + "=" * 60)
            print("📈 РЫНОК НАЧИНАЕТ ВОССТАНАВЛИВАТЬСЯ")
            print("=" * 60)
            print("Кризис видеоигр постепенно уходит в прошлое.")
            print("Спрос начинает возвращаться к нормальным значениям.")
            print("=" * 60)
            self.game_state["crash_active"] = False
            self.game_state["market_crash_multiplier"] = 1.0

        return triggered_events

    def get_market_multiplier(self) -> float:
        """Получить текущий множитель рынка (с учётом кризиса и событий)"""
        multiplier = self.game_state.get("market_size_multiplier", 1.0)

        if self.game_state.get("crash_active"):
            multiplier *= self.game_state.get("market_crash_multiplier", 0.15)

        return multiplier

    def get_price_sensitivity(self) -> float:
        """Получить чувствительность рынка к цене"""
        return self.game_state.get("price_sensitivity", 1.0)

    def display_active_effects(self):
        """Отобразить активные эффекты"""
        print("\n" + "=" * 60)
        print("АКТИВНЫЕ ИСТОРИЧЕСКИЕ ЭФФЕКТЫ")
        print("=" * 60)

        if self.game_state["ram_cost_multiplier"] != 1.0:
            print(f"💰 Стоимость памяти: {self.game_state['ram_cost_multiplier'] * 100:.0f}% от базовой")

        if self.game_state["market_size_multiplier"] != 1.0:
            print(f"📊 Размер рынка: {self.game_state['market_size_multiplier'] * 100:.0f}% от базового")

        if self.game_state["production_cost_multiplier"] != 1.0:
            print(f"🏭 Стоимость производства: {self.game_state['production_cost_multiplier'] * 100:.0f}% от базовой")

        if self.game_state["price_sensitivity"] != 1.0:
            print(f"🎯 Чувствительность к цене: {self.game_state['price_sensitivity']:.1f}x")

        if self.game_state.get("space_bonus_active"):
            print(
                f"🚀 Космический бонус: +{(self.game_state['space_bonus_multiplier'] - 1) * 100:.0f}% к продажам космических игр")

        if self.game_state.get("crash_active"):
            print(f"💀 КРИЗИС АКТИВЕН: продажи упали на 85%")

        print("=" * 60)