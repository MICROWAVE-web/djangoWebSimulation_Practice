<template>
  <div class="stats-panel">
    <div class="panel-section">
      <div class="panel-title">Статистика симуляции</div>
      <div class="stat-item">
        <span>Время симуляции:</span>
        <span class="stat-value">{{ simulationTime }} шагов</span>
      </div>
      <div class="stat-item">
        <span>Клеток всего:</span>
        <span class="stat-value">{{ totalCells }}</span>
      </div>
      <div class="stat-item">
        <span>Растения:</span>
        <span class="stat-value">{{ plantCount }}</span>
      </div>
      <div class="stat-item">
        <span>Хищники:</span>
        <span class="stat-value">{{ predatorCount }}</span>
      </div>
      <div class="stat-item">
        <span>Поколение:</span>
        <span class="stat-value">{{ generation }}</span>
      </div>
      <div class="stat-item">
        <span>Макс. возраст:</span>
        <span class="stat-value">{{ maxAge }}</span>
      </div>
      <div class="stat-item">
        <span>Сред. фотосинтез:</span>
        <span class="stat-value">{{ avgPhotosynthesis.toFixed(2) }}</span>
      </div>
      <div class="stat-item">
        <span>Сред. скорость:</span>
        <span class="stat-value">{{ avgSpeed.toFixed(2) }}</span>
      </div>
    </div>

    <div class="panel-section">
      <div class="panel-title">Управление</div>
      <div class="controls">
        <button class="btn" @click="$emit('step')">Следующий шаг (Enter)</button>
        <button class="btn btn-pause" @click="$emit('toggle-play')">
          {{ isPlaying ? 'Пауза' : 'Авто' }} (Пробел)
        </button>
        <button class="btn btn-reset" @click="$emit('reset')">Сброс</button>
      </div>
    </div>


    <div class="panel-section">
      <div class="panel-title">Состояние</div>
      <div class="stat-item">
        <span>Статус:</span>
        <span class="stat-value" :style="{color: isPlaying ? '#2ecc71' : '#e67e22'}">
          {{ isPlaying ? 'Выполняется' : 'На паузе' }}
        </span>
      </div>
      <div class="stat-item">
        <span>Скорость:</span>
        <span class="stat-value">{{ speed }} шаг/сек</span>
      </div>
    </div>

    <div class="panel-section">
      <div class="panel-title">Параметры симуляции</div>

      <div class="slider-control">
        <label>Стоимость репродукции: {{ reproductionCost }}</label>
        <input
          type="range"
          min="0"
          max="100"
          :value="reproductionCost"
          @input="$emit('change-reproduction-cost', $event.target.valueAsNumber)"
          class="slider"
        >
      </div>

      <div class="slider-control">
        <label>Энергия фотосинтеза: {{ photosynthesisEnergy }}</label>
        <input
          type="range"
          min="0"
          max="100"
          :value="photosynthesisEnergy"
          @input="$emit('change-photosynthesis-energy', $event.target.valueAsNumber)"
          class="slider"
        >
      </div>

    <div class="keyboard-hint">
      Управление: <span class="key">Enter</span> - следующий шаг,
      <span class="key">Пробел</span> - пауза/авто
    </div>

  </div></div>
</template>

<script>
export default {
  props: {
    simulationTime: Number,
    cells: Array,
    isPlaying: Boolean,
    speed: Number,
    reproductionCost: Number,
    photosynthesisEnergy: Number
  },
  computed: {
    totalCells() {
      return this.cells.length
    },
    plantCount() {
      return this.cells.filter(cell => !cell.predator).length
    },
    predatorCount() {
      return this.cells.filter(cell => cell.predator).length
    },
    generation() {
      return Math.floor(this.simulationTime / 10) + 1
    },
    maxAge() {
      return Math.max(...this.cells.map(cell => cell.age), 0)
    },
    avgPhotosynthesis() {
      const plants = this.cells.filter(cell => !cell.predator)
      if (plants.length === 0) return 0
      return plants.reduce((sum, cell) => sum + cell.photosynthesis, 0) / plants.length
    },
    avgSpeed() {
      if (this.cells.length === 0) return 0
      return this.cells.reduce((sum, cell) => sum + cell.speed, 0) / this.cells.length
    }
  }
}
</script>

<style scoped>
.stats-panel {
  flex: 0 0 300px;
  background: rgba(25, 35, 65, 0.8);
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.panel-section {
  background: rgba(30, 40, 70, 0.7);
  border-radius: 8px;
  padding: 15px;
}

.panel-title {
  font-size: 1.2rem;
  margin-bottom: 12px;
  color: #3498db;
  border-bottom: 1px solid #3498db;
  padding-bottom: 5px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-value {
  font-weight: bold;
  color: #2ecc71;
}

.controls {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn {
  flex: 1;
  min-width: 120px;
  padding: 12px;
  border: none;
  border-radius: 5px;
  background: #3498db;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.btn:hover {
  background: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
}

.btn:active {
  transform: translateY(0);
}

.btn-pause {
  background: #e67e22;
}

.btn-pause:hover {
  background: #d35400;
}

.btn-reset {
  background: #e74c3c;
}

.btn-reset:hover {
  background: #c0392b;
}

.keyboard-hint {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 0.9rem;
  opacity: 0.7;
}

.key {
  display: inline-block;
  padding: 2px 8px;
  background: rgba(52, 152, 219, 0.3);
  border-radius: 4px;
  margin: 0 3px;
}

.cell {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 10px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}

.plant {
  background: linear-gradient(135deg, #2ecc71, #1abc9c);
  border: 1px solid rgba(46, 204, 113, 0.5);
}

.predator {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  border: 1px solid rgba(231, 76, 60, 0.5);
}
.slider-control {
  margin: 15px 0;
}

.slider-control label {
  display: block;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.slider {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: rgba(52, 152, 219, 0.3);
  outline: none;
  -webkit-appearance: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #3498db;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #3498db;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}
</style>