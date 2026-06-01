"""
Конструктор игровой консоли
"""

from typing import Optional, Dict, Tuple
from components import ComponentDatabase, CPU, RAM


class ConsoleBuild:
    """Класс для сборки консоли"""

    def __init__(self, current_year: int = 1973):
        self.current_year = current_year
        self.cpu: Optional[CPU] = None
        self.ram: Optional[RAM] = None
        self.db = ComponentDatabase()

    def select_cpu(self) -> bool:
        """Выбрать процессор"""
        available_cpus = self.db.get_available_cpus_by_year(self.current_year)

        if not available_cpus:
            print(f"\n❌ В {self.current_year} году нет доступных процессоров!")
            return False

        self.db.display_component_list(available_cpus, f"ДОСТУПНЫЕ ПРОЦЕССОРЫ ({self.current_year} год)")
        selected_cpu = self.db.select_component(available_cpus, "Выберите процессор")

        if selected_cpu:
            self.cpu = selected_cpu
            print(f"\n✅ Выбран процессор: {self.cpu.name}")
            return True
        else:
            print("\n❌ Выбор процессора отменён")
            return False

    def select_ram(self) -> bool:
        """Выбрать оперативную память"""
        available_rams = self.db.get_available_rams_by_year(self.current_year)

        if not available_rams:
            print(f"\n❌ В {self.current_year} году нет доступных модулей памяти!")
            return False

        self.db.display_component_list(available_rams, f"ДОСТУПНЫЕ МОДУЛИ ПАМЯТИ ({self.current_year} год)")
        selected_ram = self.db.select_component(available_rams, "Выберите модуль памяти")

        if selected_ram:
            self.ram = selected_ram
            print(f"\n✅ Выбрана память: {self.ram.name}")
            return True
        else:
            print("\n❌ Выбор памяти отменён")
            return False

    def calculate_total_cost(self) -> float:
        """Рассчитать итоговую стоимость сборки"""
        total = 0.0
        if self.cpu:
            total += self.cpu.price
        if self.ram:
            total += self.ram.price
        return total

    def calculate_total_power(self) -> int:
        """Рассчитать общую мощность системы"""
        total = 0
        if self.cpu:
            total += self.cpu.power
        if self.ram:
            total += self.ram.power
        return total

    def display_build_info(self):
        """Отобразить информацию о текущей сборке"""
        print("\n" + "=" * 60)
        print("ТЕКУЩАЯ КОНФИГУРАЦИЯ КОНСОЛИ")
        print("=" * 60)

        if self.cpu:
            print(f"\n📦 ПРОЦЕССОР:")
            print(f"   {self.cpu}")
        else:
            print(f"\n📦 ПРОЦЕССОР: не выбран")

        if self.ram:
            print(f"\n💾 ПАМЯТЬ:")
            print(f"   {self.ram}")
        else:
            print(f"\n💾 ПАМЯТЬ: не выбрана")

        print(f"\n💰 ИТОГОВАЯ СЕБЕСТОИМОСТЬ: ${self.calculate_total_cost():,.0f}")
        print(f"⚡ ОБЩАЯ МОЩНОСТЬ: {self.calculate_total_power()} ед.")
        print("=" * 60)

    def is_complete(self) -> bool:
        """Проверить, полностью ли собрана консоль"""
        return self.cpu is not None and self.ram is not None

    def get_build_summary(self) -> Dict:
        """Получить сводку о сборке в виде словаря"""
        summary = {
            'total_cost': self.calculate_total_cost(),
            'total_power': self.calculate_total_power(),
            'complete': self.is_complete()
        }

        if self.cpu:
            summary['cpu'] = self.cpu.get_info()
        if self.ram:
            summary['ram'] = self.ram.get_info()

        return summary


class ConstructorMenu:
    """Меню конструктора консоли"""

    def __init__(self, current_year: int = 1973):
        self.build = ConsoleBuild(current_year)

    def display_menu(self):
        """Отобразить главное меню конструктора"""
        print("\n" + "=" * 60)
        print("КОНСТРУКТОР КОНСОЛИ")
        print("=" * 60)
        print("1. Выбрать процессор (CPU)")
        print("2. Выбрать оперативную память (RAM)")
        print("3. Показать текущую сборку")
        print("4. Завершить сборку и продолжить")
        print("0. Выход в главное меню")
        print("=" * 60)

    def run(self) -> Optional[ConsoleBuild]:
        """Запустить конструктор. Возвращает сборку или None если выход"""
        print(f"\n🔧 ДОБРО ПОЖАЛОВАТЬ В КОНСТРУКТОР КОНСОЛИ!")
        print(f"📅 Доступные технологии: {self.build.current_year} год")
        print(f"💡 Выберите компоненты для вашей консоли")

        while True:
            self.display_menu()

            choice = input("\nВаш выбор: ")

            if choice == "1":
                self.build.select_cpu()
            elif choice == "2":
                self.build.select_ram()
            elif choice == "3":
                self.build.display_build_info()
            elif choice == "4":
                if self.build.is_complete():
                    print("\n✅ Сборка завершена успешно!")
                    self.build.display_build_info()
                    return self.build
                else:
                    print("\n⚠️ Вы не выбрали все необходимые компоненты!")
                    missing = []
                    if not self.build.cpu:
                        missing.append("процессор")
                    if not self.build.ram:
                        missing.append("память")
                    print(f"Отсутствует: {', '.join(missing)}")
                    print("Пожалуйста, завершите сборку.")
            elif choice == "0":
                print("\n🚪 Выход из конструктора...")
                return None
            else:
                print("\n❌ Неверный выбор. Попробуйте снова.")