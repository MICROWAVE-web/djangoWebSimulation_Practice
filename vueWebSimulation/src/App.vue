<template>
  <div class="container">
    <header>
      <h1>Симуляция эволюции клеток</h1>
      <div class="subtitle">Исследуйте эволюцию в действии</div>
    </header>

    <div class="content">
      <StatsPanel
        :reproductionCost="reproductionCost"
        :photosynthesisEnergy="photosynthesisEnergy"
        @change-reproduction-cost="changeReproductionCost"
        @change-photosynthesis-energy="changePhotosynthesisEnergy"
        :simulationTime="simulationTime"
        :cells="cells"
        :isPlaying="isPlaying"
        :speed="speed"
        @toggle-play="togglePlay"
        @step="step"
        @reset="reset"
      />

      <CellGrid
        :cells="cells"
        @cell-hover="showTooltip"
        @cell-leave="hideTooltip"
      />



      <Tooltip
        v-if="tooltipVisible"
        :cell="currentCell"
        :position="{ x: tooltipX, y: tooltipY }"
      />
    </div>
  </div>
</template>

<script>
import StatsPanel from './components/StatsPanel.vue'
import CellGrid from './components/CellGrid.vue'
import Tooltip from './components/Tooltip.vue'
import api from './services/api'

export default {
  components: { StatsPanel, CellGrid, Tooltip },
  data() {
    return {
      cells: [],
      simulationTime: 0,
      isPlaying: false,
      speed: 6,
      timer: null,
      loading: false,
      currentCell: {},
      tooltipVisible: false,
      tooltipX: 0,
      tooltipY: 0,
      reproductionCost: 0,
      photosynthesisEnergy: 0
    }
  },
  methods: {
    async fetchCells() {
      try {
        const response = await api.getCells()
        this.cells = response.data
      } catch (error) {
        console.error('Error fetching cells:', error)
      }
    },
    async resetSimulation() {
      try {
        const response = await api.resetSimulation()
      } catch (error) {
        console.error('Error fetching cells:', error)
      }
    },
    async step() {
      try {
        this.loading = true
        await api.makeStep()
        this.simulationTime++
        await this.fetchCells()
      } catch (error) {
        console.error('Error performing step:', error)
      } finally {
        this.loading = false
      }
    },
    togglePlay() {
      this.isPlaying = !this.isPlaying
      if (this.isPlaying) {
        this.startAutoPlay()
      } else {
        this.stopAutoPlay()
      }
    },
    startAutoPlay() {
      this.stopAutoPlay()
      this.timer = setInterval(() => {
        this.step()
      }, 1000 / this.speed)
    },
    stopAutoPlay() {
      if (this.timer) {
        clearInterval(this.timer)
        this.timer = null
      }
    },
    reset() {
      this.stopAutoPlay()
      this.isPlaying = false
      this.simulationTime = 0
      this.resetSimulation()
      this.fetchCells()
    },
    showTooltip(cell, position) {
      this.currentCell = cell
      this.tooltipVisible = true
      this.tooltipX = position.x
      this.tooltipY = position.y
    },
    hideTooltip() {
      this.tooltipVisible = false
    },
    async fetchParams() {
      try {
        const reprodResponse = await api.getParam('REPRODUCTION_COST');
        this.reproductionCost = reprodResponse.data.value;

        const photoResponse = await api.getParam('PHOTOSYNTHESIS_ENERGY');
        this.photosynthesisEnergy = photoResponse.data.value;
      } catch (error) {
        console.error('Error fetching params:', error);
      }
    },

    async changeReproductionCost(value) {
      try {
        await api.changeParam('REPRODUCTION_COST', value);
        this.reproductionCost = value;
      } catch (error) {
        console.error('Error changing reproduction cost:', error);
      }
    },

    async changePhotosynthesisEnergy(value) {
      try {
        await api.changeParam('PHOTOSYNTHESIS_ENERGY', value);
        this.photosynthesisEnergy = value;
      } catch (error) {
        console.error('Error changing photosynthesis energy:', error);
      }
    }
  },
  created() {
    this.fetchParams();
    this.fetchCells();



    window.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') this.step()
      if (event.key === ' ') {
        event.preventDefault()
        this.togglePlay()
      }
    })
  },
  beforeUnmount() {
    this.stopAutoPlay()
    window.removeEventListener('keydown')
  }
}
</script>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background: linear-gradient(135deg, #1a2a6c, #2c3e50);
            color: #ecf0f1;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        header {
            text-align: center;
            padding: 20px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            color: #3498db;
            text-shadow: 0 0 10px rgba(52, 152, 219, 0.5);
        }

        .subtitle {
            font-size: 1.2rem;
            opacity: 0.8;
        }

        .content {
            width: 1560px;
            display: flex;
            gap: 20px;
        }

        @media (max-width: 1000px) {
            .content {
                flex-direction: column;
            }
        }

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

        .simulation-area {
            width: fit-content;
            flex: 1;
            background: rgba(25, 35, 65, 0.8);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            position: relative;
            overflow: hidden;
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

        .simulation-grid {
            position: relative;
            width: 100%;
            height: 600px;
            background: rgba(15, 25, 45, 0.7);
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid rgba(52, 152, 219, 0.3);
        }

        .cell {
            position: absolute;
            width: 12px;
            height: 12px;
            //border-radius: 50%;
            //transform: translate(-50%, -50%);
            //transition: all 0.3s;
            //box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
        }

        .cell:hover {
            //transform: translate(-50%, -50%) scale(1.5);
            z-index: 10;
        }

        .plant {
            background: linear-gradient(135deg, #2ecc71, #1abc9c);
            border: 1px solid rgba(46, 204, 113, 0.5);
        }

        .predator {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            border: 1px solid rgba(231, 76, 60, 0.5);
        }

        .tooltip {
            position: absolute;
            background: rgba(30, 40, 70, 0.95);
            border: 1px solid #3498db;
            border-radius: 8px;
            padding: 15px;
            z-index: 100;
            width: 250px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(5px);
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s;
        }

        .tooltip.visible {
            opacity: 1;
        }

        .tooltip-title {
            font-size: 1.2rem;
            margin-bottom: 10px;
            color: #3498db;
            border-bottom: 1px solid #3498db;
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

        footer {
            text-align: center;
            padding: 20px;
            opacity: 0.7;
            font-size: 0.9rem;
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
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>