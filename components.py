"""
База данных компонентов для конструктора консоли
"""

from typing import List, Dict, Optional


class Component:
    """Базовый класс для всех компонентов"""

    def __init__(self, name: str, price: float, power: int, release_year: int):
        self.name = name
        self.price = price
        self.power = power  # Мощность в условных единицах
        self.release_year = release_year

    def __str__(self):
        return f"{self.name} (${self.price:,.0f}, {self.power} ед., {self.release_year})"

    def get_info(self) -> Dict:
        """Вернуть информацию о компоненте в виде словаря"""
        return {
            'name': self.name,
            'price': self.price,
            'power': self.power,
            'release_year': self.release_year
        }


class CPU(Component):
    """Класс процессора"""

    def __init__(self, name: str, price: float, power: int, release_year: int, cores: int, frequency: float):
        super().__init__(name, price, power, release_year)
        self.cores = cores
        self.frequency = frequency  # Частота в ГГц

    def __str__(self):
        return f"CPU: {self.name} | {self.cores} ядер | {self.frequency} ГГц | Мощность: {self.power} | Цена: ${self.price:,.0f} | Год: {self.release_year}"

    def get_info(self) -> Dict:
        info = super().get_info()
        info.update({
            'cores': self.cores,
            'frequency': self.frequency,
            'type': 'CPU'
        })
        return info


class RAM(Component):
    """Класс модуля памяти"""

    def __init__(self, name: str, price: float, power: int, release_year: int, size: int, ram_type: str):
        super().__init__(name, price, power, release_year)
        self.size = size  # Размер в МБ
        self.ram_type = ram_type  # Тип памяти (DDR1, DDR2 и т.д.)

    def __str__(self):
        return f"RAM: {self.name} | {self.size} МБ | {self.ram_type} | Мощность: {self.power} | Цена: ${self.price:,.0f} | Год: {self.release_year}"

    def get_info(self) -> Dict:
        info = super().get_info()
        info.update({
            'size': self.size,
            'ram_type': self.ram_type,
            'type': 'RAM'
        })
        return info


class ComponentDatabase:
    """База данных всех доступных компонентов"""

    def __init__(self):
        self.cpus: List[CPU] = []
        self.rams: List[RAM] = []
        self._init_default_components()

    def _init_default_components(self):
        """Инициализация стандартных компонентов (исторические данные 1970-1980)"""

        # Процессоры (1970-е годы)
        self.cpus = [
            CPU("Intel 4004", 60.00, 8, 1971, 1, 0.74),
            CPU("Intel 8008", 120.00, 15, 1972, 1, 0.80),
            CPU("Intel 8080", 360.00, 40, 1974, 1, 2.00),
            CPU("MOS 6502", 25.00, 35, 1975, 1, 1.00),
            CPU("Zilog Z80", 150.00, 45, 1976, 1, 2.50),
            CPU("Intel 8086", 360.00, 60, 1978, 1, 5.00),
            CPU("Intel 8088", 450.00, 55, 1979, 1, 5.00),
            CPU("Motorola 68000", 500.00, 80, 1979, 1, 8.00),
        ]

        # Модули памяти (1970-е годы)
        self.rams = [
            RAM("Intel 1103", 50.00, 5, 1970, 1, "DRAM"),
            RAM("Mostek MK4096", 80.00, 8, 1973, 4, "DRAM"),
            RAM("TI TMS4060", 120.00, 12, 1975, 16, "DRAM"),
            RAM("Intel 2116", 180.00, 15, 1976, 16, "DRAM"),
            RAM("Mostek MK4116", 200.00, 18, 1977, 16, "DRAM"),
            RAM("Hitachi HM6148", 350.00, 25, 1979, 64, "SRAM"),
            RAM("Intel P2114", 400.00, 30, 1980, 64, "SRAM"),
        ]

    def get_available_cpus_by_year(self, year: int) -> List[CPU]:
        """Получить процессоры, доступные в указанном году"""
        return [cpu for cpu in self.cpus if cpu.release_year <= year]

    def get_available_rams_by_year(self, year: int) -> List[RAM]:
        """Получить модули памяти, доступные в указанном году"""
        return [ram for ram in self.rams if ram.release_year <= year]

    def display_component_list(self, components: List[Component], title: str):
        """Отобразить список компонентов в виде меню"""
        print(f"\n{title}")
        print("-" * 60)
        for idx, component in enumerate(components, 1):
            print(f"{idx}. {component}")
        print("0. Отмена")
        print("-" * 60)

    def select_component(self, components: List[Component], prompt: str) -> Optional[Component]:
        """Интерактивный выбор компонента из списка"""
        if not components:
            print("Нет доступных компонентов для этого года!")
            return None

        while True:
            try:
                choice = input(f"\n{prompt} (введите номер): ")
                if choice == "0":
                    return None

                choice_num = int(choice)
                if 1 <= choice_num <= len(components):
                    return components[choice_num - 1]
                else:
                    print(f"Пожалуйста, введите число от 0 до {len(components)}")
            except ValueError:
                print("Пожалуйста, введите корректное число")