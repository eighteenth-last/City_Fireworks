<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import api from '../../api'

const chartRef = ref(null)
let chartInstance = null

const initChart = async () => {
  if (!chartRef.value) return

  chartInstance = echarts.init(chartRef.value)

  try {
    // 从后端 API 获取茶馆数据
    const teahouses = await api.map.getTeahousePoints()
    
    // 转换数据格式
    const data = teahouses
      .filter(t => t.coordinates && t.coordinates.lng && t.coordinates.lat)
      .map(t => {
        const isHistoric = t.is_historic
        const isPopular = t.popularity > 600
        
        // 根据类型设置颜色
        let color = '#a1887f' // 普通茶馆 - 浅棕色
        if (isHistoric) {
          color = '#d32f2f' // 历史悠久 - 红色
        } else if (isPopular) {
          color = '#e64a19' // 人气高 - 橙红色
        }
        
        return {
          value: [t.coordinates.lng, t.coordinates.lat, t.popularity || 50],
          name: t.name,
          itemStyle: {
            color: color,
            opacity: isHistoric ? 0.9 : (isPopular ? 0.75 : 0.5),
            borderColor: isHistoric ? '#b71c1c' : 'transparent',
            borderWidth: isHistoric ? 2 : 0
          }
        }
      })
    
    if (data.length === 0) {
      console.warn('No teahouse data available')
      return
    }
    
    renderChart(data)
  } catch (error) {
    console.error('Error loading teahouse distribution:', error)
  }
}

const renderChart = (data) => {
  if (!chartInstance) return

  const option = {
    title: {
      text: '茶馆文化地理分布',
      left: 'center',
      top: 10,
      textStyle: {
        color: '#5d4037',
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 253, 246, 0.95)',
      borderColor: '#8d6e63',
      borderWidth: 2,
      textStyle: {
        color: '#5d4037',
        fontSize: 13
      },
      formatter: function(params) {
        const name = params.data.name || '未知茶馆'
        const lng = params.value[0].toFixed(4)
        const lat = params.value[1].toFixed(4)
        const popularity = params.value[2]
        return `<strong>${name}</strong><br/>经度: ${lng}<br/>纬度: ${lat}<br/>人气值: ${popularity}`
      }
    },
    grid: {
      left: '5%',
      right: '5%',
      top: '15%',
      bottom: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '经度',
      nameTextStyle: {
        color: '#8d6e63',
        fontSize: 12
      },
      min: 106.3,
      max: 107.0,
      splitLine: {
        lineStyle: {
          color: 'rgba(141, 110, 99, 0.1)'
        }
      },
      axisLine: {
        lineStyle: {
          color: '#d7ccc8'
        }
      },
      axisLabel: {
        color: '#8d6e63',
        fontSize: 11
      }
    },
    yAxis: {
      type: 'value',
      name: '纬度',
      nameTextStyle: {
        color: '#8d6e63',
        fontSize: 12
      },
      min: 29.2,
      max: 30.2,
      splitLine: {
        lineStyle: {
          color: 'rgba(141, 110, 99, 0.1)'
        }
      },
      axisLine: {
        lineStyle: {
          color: '#d7ccc8'
        }
      },
      axisLabel: {
        color: '#8d6e63',
        fontSize: 11
      }
    },
    series: [{
      type: 'scatter',
      symbolSize: function(val) {
        // 将 popularity 映射到合理的气泡大小范围 (6-20)
        const popularity = val[2] || 50
        return Math.min(Math.max(popularity / 50, 6), 20)
      },
      data: data,
      emphasis: {
        scale: 1.5,
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(141, 110, 99, 0.5)'
        }
      },
      animationDelay: function(idx) {
        return idx * 3
      }
    }]
  }

  chartInstance.setOption(option)
}

const resize = () => {
  chartInstance?.resize()
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', resize)
})

onUnmounted(() => {
  window.removeEventListener('resize', resize)
  chartInstance?.dispose()
})

defineExpose({ resize })
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  min-height: 300px;
}
</style>
