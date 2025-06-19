<template>
  <div
    class="tooltip"
    :style="{
      left: position.x + 'px',
      top: position.y + 'px',
      borderColor: cell.predator ? 'rgba(255, 60, 60, 0.7)' : 'rgba(60, 255, 60, 0.7)'
    }"
  >
    <div
      class="tooltip-title"
      :style="{ color: cell.predator ? '#ff3c3c' : '#2ecc71' }"
    >
      {{ cell.predator ? 'Хищник' : 'Растение' }}
    </div>

    <div class="tooltip-row">
      <span class="tooltip-label">Координаты:</span>
      <span class="tooltip-value">({{ cell.x }}, {{ cell.y }})</span>
    </div>

    <div class="tooltip-row">
      <span class="tooltip-label">Энергия:</span>
      <span class="tooltip-value">{{ cell.energy.toFixed(1) }}</span>
    </div>

    <div class="tooltip-row">
      <span class="tooltip-label">Возраст:</span>
      <span class="tooltip-value">{{ cell.age }}</span>
    </div>

    <div class="genome-section">
      <div class="genome-title">Геном:</div>

      <div class="genome-row">
        <span class="genome-label">Фотосинтез:</span>
        <div class="genome-bar-container">
          <div
            class="genome-bar"
            :style="{ width: (cell.photosynthesis * 100) + '%' }"
          ></div>
          <span class="genome-value">{{ cell.photosynthesis.toFixed(3) }}</span>
        </div>
      </div>

      <div class="genome-row">
        <span class="genome-label">Скорость:</span>
        <div class="genome-bar-container">
          <div
            class="genome-bar"
            :style="{ width: (cell.speed * 100) + '%' }"
          ></div>
          <span class="genome-value">{{ cell.speed.toFixed(3) }}</span>
        </div>
      </div>

      <div class="genome-row">
        <span class="genome-label">Чувствительность:</span>
        <span class="genome-value">{{ cell.sense_distance }}</span>
      </div>

      <div class="genome-row">
        <span class="genome-label">Размножение:</span>
        <div class="genome-bar-container">
          <div
            class="genome-bar"
            :style="{ width: (cell.reproduction_rate * 1000) + '%' }"
          ></div>
          <span class="genome-value">{{ cell.reproduction_rate.toFixed(3) }}</span>
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
    position: {
      type: Object,
      required: true,
      default: () => ({ x: 0, y: 0 })
    }
  }
}
</script>

<style scoped>
.tooltip {
  position: fixed;
  background: rgba(30, 40, 70, 0.95);
  border: 1px solid;
  border-radius: 8px;
  padding: 15px;
  z-index: 100;
  width: 280px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  pointer-events: none;
  transform: translate(10px, -50%);
}

.tooltip-title {
  font-size: 1.2rem;
  margin-bottom: 10px;
  border-bottom: 1px solid;
  padding-bottom: 5px;
}

.tooltip-row {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.tooltip-label {
  opacity: 0.8;
}

.tooltip-value {
  font-weight: bold;
}

.genome-section {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.genome-title {
  font-weight: bold;
  margin-bottom: 8px;
  color: #3498db;
}

.genome-row {
  display: flex;
  align-items: center;
  margin: 6px 0;
}

.genome-label {
  flex: 0 0 120px;
  font-size: 0.9rem;
  opacity: 0.8;
}

.genome-bar-container {
  flex: 1;
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  height: 20px;
  position: relative;
}

.genome-bar {
  height: 100%;
  border-radius: 4px;
  background: linear-gradient(90deg, #3498db, #2ecc71);
}

.genome-value {
  position: absolute;
  right: 5px;
  font-size: 0.8rem;
  font-weight: bold;
}
</style>