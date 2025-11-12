<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import api from '../../api'

const chartRef = ref(null)
let chart = null

onMounted(async () => {
  if (!chartRef.value) return

  chart = echarts.init(chartRef.value)
  await loadData()
})

onUnmounted(() => {
  if (chart) {
    chart.dispose()
    chart = null
  }
})

const loadData = async () => {
  try {
    // 使用后端 API
    const data = await api.map.getDistrictBoundaries()
    
    // 按火锅密度降序排序，只取前12个
    const sortedData = data.sort((a, b) => b.hotpot_density - a.hotpot_density).slice(0, 12)
    
    updateChart(sortedData)
  } catch (error) {
    console.error('Error loading hotpot ranking:', error)
  }
}

const updateChart = (data) => {
  if (!chart) return

  const districts = data.map(item => item.name)
  const densities = data.map(item => item.hotpot_density)
  
  // 找出最大值用于高亮显示
  const maxDensity = Math.max(...densities)

  const option = {
    backgroundColor: 'transparent',
    title: {
      text: '🏆 火锅密度排行榜 TOP 12',
      left: 'center',
      top: 0,
      textStyle: {
        color: '#5d4037',
        fontSize: 12,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      confine: true,
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params) => {
        const item = params[0]
        const district = item.name
        const density = item.value
        const dataItem = data.find(d => d.name === district)
        
        return `
          <div style="padding: 10px; min-width: 160px;">
            <div style="font-weight: bold; margin-bottom: 8px; font-size: 14px; color: #5d4037;">${district}</div>
            <div style="margin: 5px 0; font-size: 13px;">
              <span style="color: #3e2723;">火锅密度: <b style="color: #c62828;">${density}</b> 家/km²</span>
            </div>
            ${dataItem ? `
              <div style="margin: 5px 0; font-size: 12px; color: #8d6e63;">
                面积: ${dataItem.area_km2} km²
              </div>
              <div style="margin: 5px 0; font-size: 12px; color: #8d6e63;">
                人口: ${dataItem.population.toLocaleString()} 人
              </div>
            ` : ''}
          </div>
        `
      },
      backgroundColor: 'rgba(255, 253, 246, 0.98)',
      borderColor: '#8d6e63',
      borderWidth: 2,
      textStyle: {
        color: '#3e2723'
      },
      extraCssText: 'box-shadow: 6px 6px 0 #d7ccc8;'
    },
    grid: {
      left: '18%',
      right: '12%',
      top: '20px',
      bottom: '0px',
      containLabel: false
    },
    xAxis: {
      type: 'value',
      // name: '火锅密度',
      nameTextStyle: {
        color: '#8d6e63',
        fontSize: 10
      },
      axisLabel: {
        color: '#8d6e63',
        fontSize: 9
      },
      axisLine: {
        lineStyle: {
          color: '#ff4d4d'
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 77, 77, 0.1)'
        }
      }
    },
    yAxis: {
      type: 'category',
      data: districts,
      inverse: true,
      axisLabel: {
        color: '#8d6e63',
        fontSize: 9,
        margin: 5
      },
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      splitLine: {
        show: false
      }
    },
    series: [
      {
        name: '火锅密度',
        type: 'bar',
        data: densities.map((value, index) => ({
          value: value,
          itemStyle: {
            color: value === maxDensity 
              ? new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  { offset: 0, color: 'rgba(255, 77, 77, 0.9)' },
                  { offset: 1, color: 'rgba(255, 77, 77, 0.5)' }
                ])
              : new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  { offset: 0, color: 'rgba(0, 212, 255, 0.7)' },
                  { offset: 1, color: 'rgba(0, 212, 255, 0.3)' }
                ]),
            borderRadius: [0, 4, 4, 0]
          }
        })),
        barWidth: '65%',
        barCategoryGap: '20%',
        label: {
          show: true,
          position: 'right',
          formatter: '{c}',
          color: '#5d4037',
          fontSize: 9,
          distance: 3,
          fontWeight: 'bold'
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: 'rgba(255, 140, 140, 1)' },
              { offset: 1, color: 'rgba(255, 140, 140, 0.6)' }
            ])
          }
        },
        animationDuration: 1500,
        animationEasing: 'cubicOut'
      }
    ]
  }

  chart.setOption(option)
}

defineExpose({
  resize: () => {
    if (chart) {
      chart.resize()
    }
  }
})
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 260px;
}
</style>
