<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { api } from '../../api'

const chartRef = ref(null)
let chartInstance = null

onMounted(async () => {
  if (!chartRef.value) return

  chartInstance = echarts.init(chartRef.value)
  
  // 加载数据
  await loadData()
  
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  window.removeEventListener('resize', handleResize)
})

const loadData = async () => {
  try {
    // 后端 API 返回的是已统计好的数据：[{decade, count}, ...]
    const decadeData = await api.teahouse.getTimeSeriesData()
    
    if (!decadeData || decadeData.length === 0) {
      console.warn('No teahouse time series data available')
      return
    }
    
    // 转换为 Map 格式
    const decadeMap = new Map()
    decadeData.forEach(item => {
      decadeMap.set(item.decade, item.count)
    })
    
    // 生成按年代排序的数据
    const sortedDecades = Array.from(decadeMap.keys()).sort((a, b) => a - b)
    const categories = sortedDecades.map(d => `${d}年代`)
    const values = sortedDecades.map(d => decadeMap.get(d))
    
    const option = {
      backgroundColor: 'transparent',
      title: {
        text: '📅 开店年代分布',
        left: 'center',
        top: 15,
        textStyle: {
          color: '#5d4e37',
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#8b7355',
        borderWidth: 1,
        textStyle: {
          color: '#5d4e37'
        },
        axisPointer: {
          type: 'line',
          lineStyle: {
            color: '#8b7355',
            type: 'dashed'
          }
        },
        formatter: (params) => {
          const p = params[0]
          return `${p.name}<br/>开店数量: <strong>${p.value}</strong>`
        }
      },
      grid: {
        left: '12%',
        right: '8%',
        top: '25%',
        bottom: '15%'
      },
      xAxis: {
        type: 'category',
        data: categories,
        axisLine: {
          lineStyle: {
            color: '#d4c4a8'
          }
        },
        axisLabel: {
          color: '#8b7355',
          fontSize: 11,
          rotate: 0
        },
        axisTick: {
          show: false
        }
      },
      yAxis: {
        type: 'value',
        name: '开店数量',
        nameTextStyle: {
          color: '#8b7355',
          fontSize: 12
        },
        axisLine: {
          show: false
        },
        axisLabel: {
          color: '#8b7355',
          fontSize: 11
        },
        splitLine: {
          lineStyle: {
            color: '#e8dfd0',
            type: 'solid'
          }
        }
      },
      series: [
        {
          type: 'line',
          data: values,
          smooth: true,
          symbol: 'circle',
          symbolSize: 8,
          itemStyle: {
            color: '#5b9bd5',
            borderWidth: 2,
            borderColor: '#fff'
          },
          lineStyle: {
            color: '#8b7355',
            width: 2
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(139, 115, 85, 0.3)' },
              { offset: 0.5, color: 'rgba(139, 115, 85, 0.15)' },
              { offset: 1, color: 'rgba(212, 196, 168, 0.1)' }
            ])
          },
          emphasis: {
            itemStyle: {
              color: '#5b9bd5',
              borderColor: '#fff',
              borderWidth: 3,
              shadowBlur: 10,
              shadowColor: 'rgba(91, 155, 213, 0.5)'
            }
          }
        }
      ]
    }
    
    chartInstance.setOption(option)
  } catch (error) {
    console.error('Failed to load teahouse timeline data:', error)
  }
}

const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

// 暴露方法供父组件调用
defineExpose({
  resize: handleResize
})
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  min-height: 250px;
}
</style>
