"""Веб-интерфейс для игры с использованием Flask"""
from flask import Flask, render_template_string, jsonify, request
import json
import threading
import webbrowser
from engine import TimeEngine

app = Flask(__name__)
game_engine = None

# HTML шаблон с CSS и JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Console Constructor - Economic Simulator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3a 100%);
            color: #e0e0e0;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        /* Вкладки */
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .tab {
            background: #2a2a3a;
            padding: 12px 24px;
            cursor: pointer;
            border-radius: 8px;
            transition: all 0.3s;
            font-weight: bold;
        }

        .tab:hover {
            background: #3a3a4a;
            transform: translateY(-2px);
        }

        .tab.active {
            background: #4a90e2;
            color: white;
        }

        /* Панели */
        .panel {
            background: #252535;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            display: none;
            animation: fadeIn 0.3s;
        }

        .panel.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Карточки */
        .card {
            background: #1e1e2e;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #4a90e2;
        }

        .card-warning {
            border-left-color: #e2a04a;
        }

        .card-danger {
            border-left-color: #e24a4a;
        }

        .card-success {
            border-left-color: #4ae27a;
        }

        /* Заголовки */
        h1 {
            font-size: 28px;
            margin-bottom: 20px;
            color: #4a90e2;
        }

        h2 {
            font-size: 20px;
            margin-bottom: 15px;
            color: #e0e0e0;
        }

        h3 {
            font-size: 16px;
            margin-bottom: 10px;
            color: #aaa;
        }

        /* Статистика */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .stat-box {
            background: #1e1e2e;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-value {
            font-size: 32px;
            font-weight: bold;
            color: #4a90e2;
            margin-top: 10px;
        }

        .stat-label {
            font-size: 14px;
            color: #aaa;
        }

        /* Прогресс-бары */
        .progress-bar {
            background: #2a2a3a;
            height: 30px;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }

        .progress-fill {
            height: 100%;
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 12px;
            font-weight: bold;
        }

        /* Кнопки */
        .btn {
            background: #4a90e2;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: all 0.3s;
            margin: 5px;
        }

        .btn:hover {
            background: #357abd;
            transform: translateY(-2px);
        }

        .btn-danger {
            background: #e24a4a;
        }

        .btn-danger:hover {
            background: #c13a3a;
        }

        .btn-success {
            background: #4ae27a;
        }

        .btn-success:hover {
            background: #3ac863;
        }

        .btn-warning {
            background: #e2a04a;
        }

        /* Списки компонентов */
        .component-list {
            max-height: 300px;
            overflow-y: auto;
        }

        .component-item {
            background: #2a2a3a;
            padding: 10px;
            margin: 5px 0;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .component-item:hover {
            background: #3a3a4a;
            transform: translateX(5px);
        }

        .component-item.selected {
            background: #4a90e2;
            color: white;
        }

        /* График */
        .chart-container {
            background: #1e1e2e;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }

        canvas {
            max-width: 100%;
            height: auto;
        }

        /* Адаптивность */
        @media (max-width: 768px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }

            .tabs {
                flex-direction: column;
            }
        }

        /* Ползунки */
        .slider-container {
            margin: 15px 0;
        }

        input[type="range"] {
            width: 100%;
            margin: 10px 0;
        }

        /* Сообщения */
        .message {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #4a90e2;
            padding: 12px 20px;
            border-radius: 8px;
            animation: slideIn 0.3s;
            z-index: 1000;
        }

        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <h1>🎮 Console Constructor - Economic Simulator</h1>

        <div class="tabs">
            <div class="tab active" onclick="switchTab('main')">📊 Главная</div>
            <div class="tab" onclick="switchTab('constructor')">🔧 Конструктор</div>
            <div class="tab" onclick="switchTab('sales')">💰 Продажи</div>
            <div class="tab" onclick="switchTab('market')">📈 Анализ рынка</div>
            <div class="tab" onclick="switchTab('history')">📜 История</div>
        </div>

        <div id="mainPanel" class="panel active">
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-label">📅 Дата</div>
                    <div class="stat-value" id="date"></div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">💰 Баланс</div>
                    <div class="stat-value" id="balance"></div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">🕹️ Консоль</div>
                    <div class="stat-value" id="consoleStatus">Не собрана</div>
                </div>
            </div>

            <div class="card" id="consoleInfo">
                <h2>Текущая консоль</h2>
                <div id="consoleDetails"></div>
            </div>

            <div class="card card-success">
                <h2>Продажи</h2>
                <div id="salesInfo"></div>
            </div>

            <button class="btn" onclick="nextWeek()" style="width: 100%; margin-top: 20px;">
                ⏩ Следующая неделя (Enter)
            </button>
        </div>

        <div id="constructorPanel" class="panel">
            <h2>Конструктор консоли</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h3>Процессоры (CPU)</h3>
                    <div class="component-list" id="cpuList"></div>
                </div>
                <div>
                    <h3>Память (RAM)</h3>
                    <div class="component-list" id="ramList"></div>
                </div>
            </div>
            <div class="card">
                <h3>Выбранные компоненты</h3>
                <div id="selectedComponents"></div>
                <button class="btn btn-success" onclick="assembleConsole()" style="width: 100%; margin-top: 15px;">
                    🔨 Собрать консоль
                </button>
            </div>
        </div>

        <div id="salesPanel" class="panel">
            <h2>Управление продажами</h2>
            <div class="card">
                <h3>Статус продаж</h3>
                <div id="salesStatus"></div>
                <button class="btn" onclick="toggleSales()" id="toggleSalesBtn"></button>
            </div>

            <div class="card">
                <h3>Цена</h3>
                <div class="slider-container">
                    <input type="range" id="priceSlider" min="10" max="500" step="10" value="150">
                    <div>💰 Цена: $<span id="priceValue">150</span></div>
                </div>
            </div>

            <div class="card">
                <h3>Маркетинг</h3>
                <div class="slider-container">
                    <input type="range" id="marketingSlider" min="0" max="1000" step="50" value="0">
                    <div>📢 Бюджет: $<span id="marketingValue">0</span> / неделя</div>
                </div>
            </div>

            <div class="card">
                <h3>Прогноз продаж</h3>
                <div id="forecast"></div>
            </div>
        </div>

        <div id="marketPanel" class="panel">
            <h2>Анализ рынка</h2>
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-label">Спрос</div>
                    <div class="stat-value" id="demand">0%</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Репутация</div>
                    <div class="stat-value" id="reputation">0%</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Доля рынка</div>
                    <div class="stat-value" id="marketShare">0%</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Всего продано</div>
                    <div class="stat-value" id="totalSold">0</div>
                </div>
            </div>

            <div class="chart-container">
                <canvas id="salesChart"></canvas>
            </div>
        </div>

        <div id="historyPanel" class="panel">
            <h2>Исторические события</h2>
            <div class="card">
                <h3>Активные эффекты</h3>
                <div id="activeEffects"></div>
            </div>
            <div class="card">
                <h3>Произошедшие события</h3>
                <div id="pastEvents"></div>
            </div>
        </div>
    </div>

    <div id="messageContainer"></div>

    <script>
        let salesChart = null;
        let currentData = {};

        function switchTab(tabName) {
            document.querySelectorAll('.panel').forEach(panel => {
                panel.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });

            document.getElementById(tabName + 'Panel').classList.add('active');
            event.target.classList.add('active');

            if (tabName === 'market') {
                updateMarketData();
            }
        }

        async function fetchGameState() {
            const response = await fetch('/api/game_state');
            currentData = await response.json();
            updateUI();
        }

        async function nextWeek() {
            const response = await fetch('/api/next_week', { method: 'POST' });
            await fetchGameState();
        }

        async function assembleConsole() {
            const selectedCPU = document.querySelector('.component-item.selected[data-type="cpu"]');
            const selectedRAM = document.querySelector('.component-item.selected[data-type="ram"]');

            if (!selectedCPU || !selectedRAM) {
                showMessage('Выберите процессор и память!', 'warning');
                return;
            }

            const response = await fetch('/api/assemble', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    cpu_name: selectedCPU.dataset.name,
                    ram_name: selectedRAM.dataset.name
                })
            });

            const result = await response.json();
            showMessage(result.message, result.success ? 'success' : 'error');
            await fetchGameState();
        }

        async function toggleSales() {
            const response = await fetch('/api/toggle_sales', { method: 'POST' });
            await fetchGameState();
        }

        async function updatePrice() {
            const price = document.getElementById('priceSlider').value;
            document.getElementById('priceValue').innerText = price;
            await fetch('/api/set_price', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ price: parseFloat(price) })
            });
            await fetchGameState();
        }

        async function updateMarketing() {
            const budget = document.getElementById('marketingSlider').value;
            document.getElementById('marketingValue').innerText = budget;
            await fetch('/api/set_marketing', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ budget: parseFloat(budget) })
            });
            await fetchGameState();
        }

        function updateUI() {
            // Основная информация
            document.getElementById('date').innerText = currentData.date || '1973-01';
            document.getElementById('balance').innerText = '$' + (currentData.balance || 0).toLocaleString();

            // Информация о консоли
            if (currentData.has_console) {
                document.getElementById('consoleStatus').innerText = 'Собрана';
                document.getElementById('consoleDetails').innerHTML = `
                    <div>CPU: ${currentData.cpu_name || 'Нет'}</div>
                    <div>RAM: ${currentData.ram_name || 'Нет'}</div>
                    <div>Мощность: ${currentData.total_power || 0} ед.</div>
                    <div>Себестоимость: $${(currentData.total_cost || 0).toLocaleString()}</div>
                `;
            } else {
                document.getElementById('consoleStatus').innerText = 'Не собрана';
                document.getElementById('consoleDetails').innerHTML = '<div style="color: #e24a4a;">Консоль не собрана. Используйте конструктор!</div>';
            }

            // Информация о продажах
            const salesStatus = currentData.is_selling ? '🟢 АКТИВНЫ' : '🔴 ОСТАНОВЛЕНЫ';
            document.getElementById('salesInfo').innerHTML = `
                <div>Статус: ${salesStatus}</div>
                <div>Цена: $${currentData.current_price || 0}</div>
                <div>Маркетинг: $${currentData.marketing_budget || 0}</div>
                <div>Прогноз: ~${currentData.forecast_sales || 0} шт./неделю</div>
            `;

            // Конструктор
            if (currentData.available_cpus) {
                const cpuList = document.getElementById('cpuList');
                cpuList.innerHTML = currentData.available_cpus.map(cpu => `
                    <div class="component-item" data-type="cpu" data-name="${cpu.name}" onclick="selectComponent(this)">
                        <strong>${cpu.name}</strong><br>
                        Цена: $${cpu.price.toLocaleString()} | Мощность: ${cpu.power} ед. | Год: ${cpu.release_year}
                    </div>
                `).join('');
            }

            if (currentData.available_rams) {
                const ramList = document.getElementById('ramList');
                ramList.innerHTML = currentData.available_rams.map(ram => `
                    <div class="component-item" data-type="ram" data-name="${ram.name}" onclick="selectComponent(this)">
                        <strong>${ram.name}</strong><br>
                        Цена: $${ram.price.toLocaleString()} | Мощность: ${ram.power} ед. | Размер: ${ram.size}MB
                    </div>
                `).join('');
            }

            // Выбранные компоненты
            document.getElementById('selectedComponents').innerHTML = `
                <div>CPU: ${currentData.selected_cpu || 'Не выбран'}</div>
                <div>RAM: ${currentData.selected_ram || 'Не выбрана'}</div>
                <div>Итоговая стоимость: $${(currentData.selected_cost || 0).toLocaleString()}</div>
            `;

            // Меню продаж
            document.getElementById('salesStatus').innerHTML = `
                <div>Статус: ${currentData.is_selling ? '🟢 Активны' : '🔴 Остановлены'}</div>
            `;
            const toggleBtn = document.getElementById('toggleSalesBtn');
            toggleBtn.innerText = currentData.is_selling ? 'Остановить продажи' : 'Начать продажи';
            toggleBtn.className = currentData.is_selling ? 'btn btn-danger' : 'btn btn-success';

            document.getElementById('priceSlider').value = currentData.current_price || 150;
            document.getElementById('priceValue').innerText = currentData.current_price || 150;
            document.getElementById('marketingSlider').value = currentData.marketing_budget || 0;
            document.getElementById('marketingValue').innerText = currentData.marketing_budget || 0;

            // Прогноз
            document.getElementById('forecast').innerHTML = `
                <div style="font-size: 24px; font-weight: bold;">~${currentData.forecast_sales || 0} шт.</div>
                <div>Ожидаемый доход: ~$${((currentData.forecast_sales || 0) * (currentData.current_price || 0)).toLocaleString()}</div>
            `;
        }

        function updateMarketData() {
            if (!currentData.market_data) return;

            document.getElementById('demand').innerText = Math.round(currentData.market_data.demand || 0) + '%';
            document.getElementById('reputation').innerText = Math.round((currentData.market_data.reputation || 0) * 100) + '%';
            document.getElementById('marketShare').innerText = Math.round((currentData.market_data.market_share || 0) * 100) + '%';
            document.getElementById('totalSold').innerText = currentData.market_data.total_sold || 0;

            // Обновляем график
            if (salesChart && currentData.market_data.sales_history) {
                salesChart.data.datasets[0].data = currentData.market_data.sales_history;
                salesChart.update();
            }
        }

        function updateHistory() {
            if (!currentData.history_data) return;

            // Активные эффекты
            const effectsDiv = document.getElementById('activeEffects');
            if (currentData.history_data.active_effects && currentData.history_data.active_effects.length > 0) {
                effectsDiv.innerHTML = currentData.history_data.active_effects.map(effect => `
                    <div class="card card-warning">${effect}</div>
                `).join('');
            } else {
                effectsDiv.innerHTML = '<div>Нет активных эффектов</div>';
            }

            // Произошедшие события
            const eventsDiv = document.getElementById('pastEvents');
            if (currentData.history_data.past_events && currentData.history_data.past_events.length > 0) {
                eventsDiv.innerHTML = currentData.history_data.past_events.map(event => `
                    <div class="card">
                        <strong>${event.date} - ${event.title}</strong>
                        <div style="font-size: 12px; margin-top: 5px;">${event.description}</div>
                    </div>
                `).join('');
            } else {
                eventsDiv.innerHTML = '<div>Пока не произошло ни одного события</div>';
            }
        }

        function selectComponent(element) {
            const type = element.dataset.type;
            document.querySelectorAll(`.component-item[data-type="${type}"]`).forEach(el => {
                el.classList.remove('selected');
            });
            element.classList.add('selected');
        }

        function showMessage(text, type = 'info') {
            const container = document.getElementById('messageContainer');
            const message = document.createElement('div');
            message.className = 'message';
            message.style.background = type === 'error' ? '#e24a4a' : type === 'warning' ? '#e2a04a' : '#4a90e2';
            message.innerText = text;
            container.appendChild(message);
            setTimeout(() => message.remove(), 3000);
        }

        // Инициализация графика
        function initChart() {
            const ctx = document.getElementById('salesChart').getContext('2d');
            salesChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Продажи по неделям',
                        data: [],
                        borderColor: '#4a90e2',
                        backgroundColor: 'rgba(74, 144, 226, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            labels: { color: '#e0e0e0' }
                        }
                    }
                }
            });
        }

        // События
        document.getElementById('priceSlider').addEventListener('input', updatePrice);
        document.getElementById('marketingSlider').addEventListener('input', updateMarketing);

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                nextWeek();
            }
        });

        // Запуск
        initChart();
        fetchGameState();
        setInterval(fetchGameState, 2000);
    </script>
</body>
</html>
"""


class GameWebGUI:
    def __init__(self):
        global game_engine
        self.engine = TimeEngine(start_year=1973)
        game_engine = self.engine
        self.selected_cpu = None
        self.selected_ram = None

    def setup_routes(self):
        @app.route('/')
        def index():
            return render_template_string(HTML_TEMPLATE)

        @app.route('/api/game_state')
        def game_state():
            # Получаем доступные компоненты
            available_cpus = self.engine.db.get_available_cpus_by_year(self.engine.year)
            available_rams = self.engine.db.get_available_rams_by_year(self.engine.year)

            # Прогноз продаж
            forecast_sales = 0
            if self.engine.console_build and self.engine.console_build.is_complete():
                forecast_sales = self.engine.market.calculate_sales(
                    self.engine.console_build,
                    self.engine.sales_manager.current_price,
                    self.engine.sales_manager.marketing_budget
                )

            # Данные о рынке
            market_data = {
                'demand': 0,
                'reputation': self.engine.market.reputation,
                'market_share': self.engine.market.market_share,
                'total_sold': self.engine.market.total_sold,
                'sales_history': list(self.engine.market.sales_history) if hasattr(self.engine.market,
                                                                                   'sales_history') else []
            }

            if self.engine.console_build and self.engine.console_build.is_complete():
                market_data['demand'] = self.engine.market.calculate_demand_score(
                    self.engine.console_build,
                    self.engine.sales_manager.current_price
                )

            # Данные истории
            history_data = {
                'active_effects': [],
                'past_events': []
            }

            # Активные эффекты
            effects = self.engine.event_manager.game_state
            if effects.get('ram_cost_multiplier', 1.0) != 1.0:
                history_data['active_effects'].append(
                    f"Стоимость памяти: {effects['ram_cost_multiplier'] * 100:.0f}% от базовой")
            if effects.get('market_size_multiplier', 1.0) != 1.0:
                history_data['active_effects'].append(
                    f"Размер рынка: {effects['market_size_multiplier'] * 100:.0f}% от базового")
            if effects.get('crash_active'):
                history_data['active_effects'].append("КРИЗИС 1983 АКТИВЕН! Спрос упал на 85%")

            # Произошедшие события
            for event in self.engine.event_manager.calendar.triggered_events[-10:]:
                history_data['past_events'].append({
                    'date': f"{event.month}.{event.year}",
                    'title': event.title,
                    'description': event.description
                })

            return jsonify({
                'date': self.engine.get_date_string(),
                'balance': self.engine.balance,
                'has_console': self.engine.console_build is not None and self.engine.console_build.is_complete(),
                'cpu_name': self.engine.console_build.cpu.name if self.engine.console_build else None,
                'ram_name': self.engine.console_build.ram.name if self.engine.console_build else None,
                'total_power': self.engine.console_build.calculate_total_power() if self.engine.console_build else 0,
                'total_cost': self.engine.console_build.calculate_total_cost() if self.engine.console_build else 0,
                'is_selling': self.engine.sales_manager.is_selling,
                'current_price': self.engine.sales_manager.current_price,
                'marketing_budget': self.engine.sales_manager.marketing_budget,
                'forecast_sales': forecast_sales,
                'available_cpus': [
                    {'name': cpu.name, 'price': cpu.price, 'power': cpu.power, 'release_year': cpu.release_year} for cpu
                    in available_cpus],
                'available_rams': [{'name': ram.name, 'price': ram.price, 'power': ram.power, 'size': ram.size} for ram
                                   in available_rams],
                'selected_cpu': self.selected_cpu.name if self.selected_cpu else None,
                'selected_ram': self.selected_ram.name if self.selected_ram else None,
                'selected_cost': (self.selected_cpu.price if self.selected_cpu else 0) + (
                    self.selected_ram.price if self.selected_ram else 0),
                'market_data': market_data,
                'history_data': history_data
            })

        @app.route('/api/next_week', methods=['POST'])
        def next_week():
            self.engine.next_week()
            return jsonify({'success': True})

        @app.route('/api/assemble', methods=['POST'])
        def assemble():
            data = request.json
            cpu_name = data.get('cpu_name')
            ram_name = data.get('ram_name')

            # Находим компоненты
            cpu = None
            ram = None

            for c in self.engine.db.cpus:
                if c.name == cpu_name:
                    cpu = c
                    break

            for r in self.engine.db.rams:
                if r.name == ram_name:
                    ram = r
                    break

            if not cpu or not ram:
                return jsonify({'success': False, 'message': 'Компоненты не найдены'})

            total_cost = cpu.price + ram.price
            if total_cost > self.engine.balance:
                return jsonify({'success': False, 'message': f'Недостаточно средств! Нужно ${total_cost:,.0f}'})

            from constructor import ConsoleBuild
            build = ConsoleBuild(self.engine.year)
            build.cpu = cpu
            build.ram = ram
            self.engine.console_build = build
            self.engine.balance -= total_cost

            return jsonify({'success': True, 'message': f'Консоль собрана! Стоимость: ${total_cost:,.0f}'})

        @app.route('/api/toggle_sales', methods=['POST'])
        def toggle_sales():
            self.engine.sales_manager.is_selling = not self.engine.sales_manager.is_selling
            return jsonify({'success': True})

        @app.route('/api/set_price', methods=['POST'])
        def set_price():
            data = request.json
            self.engine.sales_manager.current_price = data.get('price', 150)
            return jsonify({'success': True})

        @app.route('/api/set_marketing', methods=['POST'])
        def set_marketing():
            data = request.json
            budget = data.get('budget', 0)
            if budget <= self.engine.balance:
                self.engine.sales_manager.marketing_budget = budget
            return jsonify({'success': True})

    def run(self):
        self.setup_routes()
        webbrowser.open('http://127.0.0.1:5000')
        app.run(debug=False, use_reloader=False)


if __name__ == "__main__":
    gui = GameWebGUI()
    gui.run()