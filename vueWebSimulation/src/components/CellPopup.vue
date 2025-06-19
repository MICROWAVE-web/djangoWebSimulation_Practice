<template>
  <div class="cell-popup-content">
    <!-- Заголовок с типом клетки -->
    <div class="popup-header" :style="{ background: `rgb(${this.color.join(',')})` }" :class="{ 'predator-header': cell.predator, 'plant-header': !cell.predator }">
      <div class="cell-type">
        {{ cell.type }}
      </div>

      <!--<div class="cell-id">ID: {{ cell.id || 'N/A' }}</div>-->
    </div>

    <!-- Основная информация -->
    <div class="popup-section">
      <div class="info-row">
        <span class="info-label">Координаты:</span>
        <span class="info-value">({{ cell.x }}, {{ cell.y }})</span>
      </div>
      <div class="info-row">
        <span class="info-label">Энергия:</span>
        <span class="info-value">{{ cell.energy.toFixed(1) }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">Возраст:</span>
        <span class="info-value">{{ cell.age }} шагов</span>
      </div>
    </div>

    <!-- Генетические характеристики -->
    <div class="popup-section">
      <h3 class="section-title">Генетические параметры</h3>

      <div class="genome-row">
        <span class="genome-label">Фотосинтез:</span>
        <div class="genome-visual">
          <div class="genome-bar-bg">
            <div
              class="genome-bar-fill"
              :style="{ width: (cell.photosynthesis * 100) + '%', background: `rgb(${this.color.join(',')})` }"
            ></div>
          </div>
          <span class="genome-value">{{ cell.photosynthesis.toFixed(3) }}</span>
        </div>
      </div>

      <div class="genome-row">
        <span class="genome-label">Скорость:</span>
        <div class="genome-visual">
          <div class="genome-bar-bg">
            <div
              class="genome-bar-fill"
              :style="{ width: (cell.speed * 100) + '%', background: `rgb(${this.color.join(',')})` }"
            ></div>
          </div>
          <span class="genome-value">{{ cell.speed.toFixed(3) }}</span>
        </div>
      </div>

      <div class="genome-row">
        <span class="genome-label">Чувствительность:</span>
        <div class="genome-visual">
          <div class="sense-dots">
            <div
              v-for="n in 5"
              :key="n"
              class="sense-dot"
              :class="{ 'active-dot': n <= cell.sense_distance }"
            ></div>
          </div>
          <span class="genome-value">{{ cell.sense_distance }}</span>
        </div>
      </div>

      <div class="genome-row">
        <span class="genome-label">Размножение:</span>
        <div class="genome-visual">
          <div class="genome-bar-bg">
            <div
              class="genome-bar-fill"
              :style="{ width: (cell.reproduction_rate * 1000) + '%', background: `rgb(${this.color.join(',')})` }"
            ></div>
          </div>
          <span class="genome-value">{{ cell.reproduction_rate.toFixed(4) }}</span>
        </div>
      </div>
    </div>


  </div>
</template>

<script>
export default {
  props: {
    cell: {
      type: Object,
      required: true,
      default: () => ({
        x: 0,
        y: 0,
        energy: 0,
        age: 0,
        predator: false,
        photosynthesis: 0,
        speed: 0,
        sense_distance: 0,
        reproduction_rate: 0
      })
    },
    color: {
      type: String,
      required: true
    }
  },
  computed: {
    genomeBarColor() {
      return this.color
    }
  }
}
</script>

<style scoped>
.cell-popup-content {
  width: 280px;
  background: rgba(20, 30, 50, 0.97);
  border-radius: 8px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.6);
  overflow: hidden;
  backdrop-filter: blur(5px);
  position: fixed;
  z-index: 1000;
}

.popup-header {
  padding: 12px 15px;
  color: white;
  text-align: center;
  position: relative;
}


.cell-type {
  font-weight: bold;
  font-size: 1.2rem;
  letter-spacing: 1px;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}

.cell-id {
  font-size: 0.7rem;
  opacity: 0.7;
  margin-top: 3px;
}

.popup-section {
  padding: 12px 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.section-title {
  font-size: 0.85rem;
  color: #3498db;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  margin: 8px 0;
  font-size: 0.9rem;
}

.info-label {
  color: #7f8c8d;
}

.info-value {
  color: #ecf0f1;
  font-weight: bold;
}

.genome-row {
  margin: 12px 0;
}

.genome-label {
  display: block;
  font-size: 0.8rem;
  color: #bdc3c7;
  margin-bottom: 5px;
}

.genome-visual {
  display: flex;
  align-items: center;
}

.genome-bar-bg {
  flex-grow: 1;
  height: 10px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 5px;
  overflow: hidden;
  margin-right: 10px;
}

.genome-bar-fill {
  height: 100%;
  border-radius: 5px;
  transition: width 0.3s ease;
}

.genome-value {
  font-size: 0.8rem;
  font-weight: bold;
  min-width: 40px;
  text-align: right;
}

.sense-dots {
  display: flex;
  gap: 5px;
  margin-right: 10px;
}

.sense-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.active-dot {
  background: #3498db;
  border-color: #2980b9;
  box-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
}

/* Анимации */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>