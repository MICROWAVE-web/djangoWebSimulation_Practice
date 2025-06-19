<template>
  <div class="simulation-area">
    <div class="panel-title">Поле эволюции</div>
    <div
        class="simulation-grid"
        @mousemove="handleMouseMove"
        ref="grid"
    >
      <!-- Сетка -->
      <div
          v-for="(line, index) in gridLines"
          :key="'line-'+index"
          class="grid-line"
          :style="line.style"
      ></div>

      <!-- Клетки -->
      <div
          v-for="(cell, index) in cells"
          :key="'cell-'+index"
          class="cell"
          :style="getCellStyle(cell)"
          @mouseover="handleCellHover(cell, $event)"
          @mouseleave="handleCellLeave"
      >{{ getEmodji(cell) }}</div>

      <div>

      </div>
      <!-- Всплывающее окно -->
      <transition name="fade">
        <div
            v-if="hoveredCell"
            class="cell-popup"
            :style="popupStyle"
        >
          <CellPopup :cell="hoveredCell" :color="getCellColor(hoveredCell)"/>
        </div>
      </transition>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>
    </div>

    <div>
      <br>
      <br>
      <h1>Классы организмов</h1>

      <div class="card plant">
        <h2>🌿 Plant (Растение)</h2>
        <ul>
          <li>Фотосинтезирует для получения энергии</li>
          <li>Медленно двигается к свету</li>
          <li>Зеленый цвет (интенсивность зависит от эффективности фотосинтеза)</li>
        </ul>
      </div>

      <div class="card predator">
        <h2>🦁 Predator (Хищник)</h2>
        <ul>
          <li>Охотится на травоядных и растения</li>
          <li>Быстрый и агрессивный</li>
          <li>Красный цвет</li>
        </ul>
      </div>

      <div class="card herbivore">
        <h2>🐄 Herbivore (Травоядное)</h2>
        <ul>
          <li>Питается растениями</li>
          <li>Умеренная скорость</li>
          <li>Оранжевый цвет</li>
        </ul>
      </div>

      <div class="card fungus">
        <h2>🍄 Fungus (Гриб)</h2>
        <ul>
          <li>Неподвижен (скорость = 0)</li>
          <li>Получает энергию из почвы и фотосинтеза</li>
          <li>Фиолетовый цвет</li>
          <li>Низкая скорость размножения</li>
        </ul>
      </div>

      <div class="card omnivore">
        <h2>🦊 Omnivore (Всеядное)</h2>
        <ul>
          <li>Ест растения, грибы и других животных</li>
          <li>Адаптивный цвет (бирюзовый)</li>
          <li>Умеренная скорость и эффективность</li>
        </ul>
      </div>
    </div>


  </div>
</template>

<script>
import CellPopup from './CellPopup.vue'

export default {
  components: {CellPopup},
  props: {
    cells: Array,
    loading: Boolean,
    gridSize: {
      type: Number,
      default: 20
    }
  },
  data() {
    return {
      gridLines: [],
      hoveredCell: null,
      popupPosition: {x: 100, y: 100},
      popupTimeout: null
    }
  },
  computed: {
    popupStyle() {
      return {
        position: 'absolute',
        left: `${this.popupPosition.x}px`,
        top: `${this.popupPosition.y}px`,
        'border-color': this.hoveredCell?.predator ? '#ff3c3c' : '#2ecc71'
      }
    }
  },
  mounted() {
    this.generateGrid()
  },
  methods: {
    generateGrid() {
      const lines = []
      const gridWidth = 200
      const gridHeight = 100
      console.log(gridHeight)
      console.log(gridWidth)

      // Вертикальные линии
      for (let x = 0; x <= gridWidth * this.gridSize; x += this.gridSize) {
        lines.push({
          style: {
            left: `${x}px`,
            top: '0',
            width: '1px',
            height: `${gridHeight * this.gridSize}px`
          }
        })
      }

      // Горизонтальные линии
      for (let y = 0; y <= gridHeight * this.gridSize; y += this.gridSize) {
        lines.push({
          style: {
            left: '0',
            top: `${y}px`,
            width: `${gridWidth * this.gridSize}px`,
            height: '1px'
          }
        })
      }

      this.gridLines = lines
    },
    getCellStyle(cell) {
      const size = this.gridSize - 2 // Оставляем небольшие промежутки
      const color = this.getCellColor(cell)

      return {
        cursor: 'pointer',
        'line-height': '17px',
        'font-size': '13px',
        left: `${cell.x * this.gridSize}px`,
        top: `${cell.y * this.gridSize}px`,
        width: `${size}px`,
        height: `${size}px`,
        backgroundColor: `rgb(${color.join(',')})`,
        border: `1px solid rgba(${color.map(c => Math.max(0, c - 40)).join(',')}, 0.7)`
      }
    },
    getEmodji(cell) {
      switch(cell.type) {
        case "Plant":
            return "🌿"

        case "Predator":
            return "🦁"

        case "Herbivore":
            return "🐄"

        case "Fungus":
            return "🍄"

        case "Omnivore":
            return "🦊"

        default:
            return "🔥"
        }
      },
    getCellColor(cell) {
    switch(cell.type) {
        case "Plant":
            // Зеленый зависит от фотосинтеза, синий от скорости
            const green = Math.min(255 , Math.abs(255 * (0.3 + cell.photosynthesis)))
            const blue = Math.min(255, Math.abs(255 * (0.3 + cell.speed)))
            return [25, green, blue]

        case "Predator":
            // Красный зависит от (1 - фотосинтез)
            const aggression = Math.min(255, Math.abs(150 + 105 * (1 - cell.photosynthesis)))
            return [aggression, 40, 40]

        case "Herbivore":
            // Фиксированный оранжевый цвет
            return [255, 165, 0]

        case "Fungus":
            // Фиксированный фиолетовый цвет
            return [128, 0, 128]

        case "Omnivore":
            // Фиксированный бирюзовый цвет
            return [0, 128, 128]

        default:
            // Белый для неизвестных типов
            return [255, 255, 255]
        }
    },
    handleCellHover(cell, event) {
      clearTimeout(this.popupTimeout)

      const gridRect = this.$refs.grid.getBoundingClientRect()
      const cellSize = this.gridSize - 2

      // Позиционируем всплывающее окно рядом с клеткой
      this.popupPosition = {
        x: event.clientX - gridRect.left + 15,
        y: event.clientY - gridRect.top + 15
      }
      console.log(this.popupPosition)

      // Проверяем, чтобы окно не выходило за границы сетки
      //const popupWidth = 280
      //const popupHeight = 582

      //if (this.popupPosition.x + popupWidth > gridRect.width) {
      //  this.popupPosition.x = event.clientX - gridRect.left - popupWidth - 5
      //}

      //if (this.popupPosition.y + popupHeight > gridRect.height) {
      //  this.popupPosition.y = event.clientY - gridRect.top - popupHeight - 5
      //}

      this.hoveredCell = cell
    },
    handleCellLeave() {
      // Добавляем небольшую задержку перед исчезновением
      this.popupTimeout = setTimeout(() => {
        this.hoveredCell = null
      }, 1)
    },
    handleMouseMove(event) {
      if (this.hoveredCell) {
        const gridRect = this.$refs.grid.getBoundingClientRect()
        this.popupPosition = {
          x: event.clientX - gridRect.left + 15,
          y: event.clientY - gridRect.top + 15
        }
      }
    }
  }
}
</script>

<style scoped>

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f0f4f8;
  margin: 0;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #438cbd;
  margin-bottom: 40px;
}

.card {
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.plant {
  background: linear-gradient(135deg, #76c043, #a8e063);
}

.predator {
  background: linear-gradient(135deg, #d32f2f, #f44336);
}

.herbivore {
  background: linear-gradient(135deg, #ff9800, #ffc107);
}

.fungus {
  background: linear-gradient(135deg, #9c27b0, #e040fb);
}

.omnivore {
  background: linear-gradient(135deg, #26c6da, #00acc1);
}

.card h2 {
  margin-top: 0;
  font-size: 24px;
}

.card ul {
  margin: 10px 0 0 0;
  padding-left: 20px;
}


.simulation-grid {
  position: relative;
  width: 1200px;
  height: 600px;
  background: #070f47;
background: linear-gradient(0deg, rgba(7, 15, 71, 1) 0%, rgba(11, 20, 107, 1) 31%, rgba(29, 39, 131, 1) 57%, rgba(98, 110, 222, 1) 100%);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(52, 152, 219, 0.3);
}

.grid-line {
  position: absolute;
  background: rgba(52, 152, 219, 0.1);
  z-index: 1;
}

.cell {
  position: absolute;
  z-index: 2;
}

.cell:hover {
  transform: scale(1.2);
  z-index: 3;
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.5);
}

.loading {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  border-radius: 8px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(52, 152, 219, 0.3);
  border-top: 5px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>