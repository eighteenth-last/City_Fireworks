<template>
  <div class="temperature-container">
    <!-- 主温度指数仪表盘 -->
    <div class="main-gauge">
      <div ref="chartRef" class="gauge-chart"></div>
      <div v-if="temperatureData" class="gauge-label">
        <div class="status-text">{{ getStatusText(temperatureData.score) }}</div>
        <div class="date-text">{{ temperatureData.date }}</div>
      </div>
    </div>

    <!-- 四个维度指标 -->
    <div v-if="temperatureData" class="factors-grid">
      <div class="factor-item">
        <div class="factor-icon">🍲</div>
        <div class="factor-info">
          <div class="factor-name">火锅密度</div>
          <div class="factor-bar">
            <div 
              class="factor-progress" 
              :style="{ width: temperatureData.factors.hotpot_density + '%', backgroundColor: '#c62828' }"
            ></div>
          </div>
          <div class="factor-value">{{ temperatureData.factors.hotpot_density }}分</div>
        </div>
      </div>

      <div class="factor-item">
        <div class="factor-icon">🌙</div>
        <div class="factor-info">
          <div class="factor-name">夜间经济</div>
          <div class="factor-bar">
            <div 
              class="factor-progress" 
              :style="{ width: temperatureData.factors.night_economy + '%', backgroundColor: '#1976d2' }"
            ></div>
          </div>
          <div class="factor-value">{{ temperatureData.factors.night_economy }}分</div>
        </div>
      </div>

      <div class="factor-item">
        <div class="factor-icon">🍵</div>
        <div class="factor-info">
          <div class="factor-name">茶馆文化</div>
          <div class="factor-bar">
            <div 
              class="factor-progress" 
              :style="{ width: temperatureData.factors.teahouse_culture + '%', backgroundColor: '#388e3c' }"
            ></div>
          </div>
          <div class="factor-value">{{ temperatureData.factors.teahouse_culture }}分</div>
        </div>
      </div>

      <div class="factor-item">
        <div class="factor-icon">⚡</div>
        <div class="factor-info">
          <div class="factor-name">区域活力</div>
          <div class="factor-bar">
            <div 
              class="factor-progress" 
              :style="{ width: temperatureData.factors.vitality + '%', backgroundColor: '#f57c00' }"
            ></div>
          </div>
          <div class="factor-value">{{ temperatureData.factors.vitality }}分</div>
        </div>
      </div>
    </div>

    <div v-if="!loaded" class="loading">加载中...</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import api from '../../api'

const chartRef = ref(null)
let chart = null
let intervalId = null

const loaded = ref(false)
const temperatureData = ref(null)

onMounted(async () => {
  if (!chartRef.value) return

  // 初始化图表
  chart = echarts.init(chartRef.value)

  // 加载数据
  await loadData()

  // 设置自动更新
  intervalId = setInterval(loadData, 30000) // 每30秒更新一次
})

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
  if (chart) {
    chart.dispose()
    chart = null
  }
})

const loadData = async () => {
  try {
    temperatureData.value = await api.insight.getCityTemperatureIndex()
    if (!temperatureData.value) {
      // 提供默认数据
      temperatureData.value = {
        score: 89,
        date: new Date().toISOString().split('T')[0],
        factors: {
          hotpot_density: 85,
          night_economy: 92,
          teahouse_culture: 78,
          vitality: 88
        }
      }
    }
    loaded.value = true
    updateChart()
  } catch (error) {
    console.error('Error loading temperature data:', error)
    // 提供默认数据
    temperatureData.value = {
      score: 89,
      date: new Date().toISOString().split('T')[0],
      factors: {
        hotpot_density: 85,
        night_economy: 92,
        teahouse_culture: 78,
        vitality: 88
      }
    }
    loaded.value = true
    updateChart()
  }
}

const updateChart = () => {
  if (!chart || !temperatureData.value) return

  const score = temperatureData.value.score
  const color = getGaugeColor(score)

  const option = {
    backgroundColor: 'transparent',
    title: {
      // text: '🌡️ 城市温度指数',
      left: 'center',
      top: 5,
      textStyle: {
        color: '#5d4037',
        fontSize: 18,
        fontWeight: 'bold'
      }
    },
    series: [
      {
        type: 'gauge',
        center: ['50%', '55%'],
        radius: '75%',
        min: 0,
        max: 100,
        startAngle: 210,
        endAngle: -30,
        splitNumber: 5,
        itemStyle: {
          color: color
        },
        progress: {
          show: true,
          width: 18,
          itemStyle: {
            color: color,
            shadowBlur: 10,
            shadowColor: color
          }
        },
        pointer: {
          show: true,
          length: '65%',
          width: 5,
          itemStyle: {
            color: color,
            shadowBlur: 5,
            shadowColor: 'rgba(0,0,0,0.3)'
          }
        },
        axisLine: {
          lineStyle: {
            width: 18,
            color: [
              [0.3, 'rgba(211, 211, 211, 0.3)'],
              [0.7, 'rgba(211, 211, 211, 0.3)'],
              [1, 'rgba(211, 211, 211, 0.3)']
            ]
          }
        },
        axisTick: {
          distance: -25,
          splitNumber: 5,
          lineStyle: {
            width: 1.5,
            color: '#999'
          }
        },
        splitLine: {
          distance: -28,
          length: 12,
          lineStyle: {
            width: 2,
            color: '#666'
          }
        },
        axisLabel: {
          distance: -40,
          color: '#5d4037',
          fontSize: 11,
          fontWeight: 'bold'
        },
        anchor: {
          show: false
        },
        title: {
          show: false
        },
        detail: {
          valueAnimation: true,
          fontSize: 48,
          offsetCenter: [0, '10%'],
          fontWeight: 'bold',
          color: color,
          formatter: '{value}',
          rich: {
            unit: {
              fontSize: 20,
              color: '#999',
              padding: [0, 0, 0, 5]
            }
          }
        },
        data: [
          {
            value: score,
            name: '温度指数'
          }
        ]
      }
    ]
  }

  chart.setOption(option, true)
}

const getGaugeColor = (score) => {
  if (score >= 80) return '#d32f2f'
  if (score >= 60) return '#f57c00'
  if (score >= 40) return '#fbc02d'
  return '#8d6e63'
}

const getStatusText = (score) => {
  if (score >= 80) return '🔥 极热'
  if (score >= 60) return '🌡️ 温热'
  if (score >= 40) return '☀️ 温和'
  return '❄️ 偏冷'
}

// 暴露方法
defineExpose({
  resize: () => {
    if (chart) {
      chart.resize()
    }
  }
})
</script>

<style scoped>
.temperature-container {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 0 10px;
  padding-top: 0;
  background: transparent;
  transform: translateY(-20px);
}

.main-gauge {
  position: relative;
  flex: 0 0 180px;
  width: 100%;
}

.gauge-chart {
  width: 100%;
  height: 100%;
}

.gauge-label {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
}

.status-text {
  font-size: 16px;
  font-weight: bold;
  color: #5d4037;
  margin-bottom: 4px;
}

.date-text {
  font-size: 11px;
  color: #999;
}

.factors-grid {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  padding: 5px;
  overflow-y: auto;
}

.factor-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 8px;
  background: rgba(255, 253, 246, 0.6);
  border-radius: 8px;
  border: 1px solid rgba(141, 110, 99, 0.2);
  transition: all 0.3s ease;
  height: 50px;
}

.factor-item:hover {
  background: rgba(255, 253, 246, 0.9);
  border-color: rgba(141, 110, 99, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.factor-icon {
  font-size: 20px;
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.factor-info {
  flex: 1;
  min-width: 0;
}

.factor-name {
  font-size: 11px;
  color: #5d4037;
  font-weight: 600;
  margin-bottom: 4px;
}

.factor-bar {
  width: 100%;
  height: 5px;
  background: rgba(211, 211, 211, 0.3);
  border-radius: 2.5px;
  overflow: hidden;
  margin-bottom: 3px;
}

.factor-progress {
  height: 100%;
  border-radius: 2.5px;
  transition: width 0.8s ease;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.2);
}

.factor-value {
  font-size: 10px;
  color: #666;
  font-weight: 600;
  text-align: right;
}

.loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #999;
  font-size: 14px;
}

/* 响应式调整 */
@media (max-width: 400px) {
  .factors-grid {
    grid-template-columns: 1fr;
  }
}
</style>
