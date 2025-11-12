<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import api from '../../api'

const chartRef = ref(null)
let chart = null
let intervalId = null

onMounted(async () => {
  if (!chartRef.value) return

  chart = echarts.init(chartRef.value)
  await loadData()

  intervalId = setInterval(loadData, 30000)
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
    const restaurants = await api.hotpot.getShopTypeDistribution()
    
    // 按店铺类型分组评分
    const typeMap = new Map()
    restaurants.forEach(r => {
      const type = r.shop_type || '其他'
      if (!typeMap.has(type)) {
        typeMap.set(type, [])
      }
      if (r.rating) {
        typeMap.get(type).push(r.rating)
      }
    })

    // 计算箱线图数据
    const data = []
    const categories = []
    
    typeMap.forEach((ratings, type) => {
      if (ratings.length > 0) {
        categories.push(type)
        const sorted = ratings.sort((a, b) => a - b)
        const len = sorted.length
        
        const min = sorted[0]
        const max = sorted[len - 1]
        const q1 = sorted[Math.floor(len * 0.25)]
        const median = sorted[Math.floor(len * 0.5)]
        const q3 = sorted[Math.floor(len * 0.75)]
        
        data.push([min, q1, median, q3, max])
      }
    })

    updateChart(categories, data)
  } catch (error) {
    console.error('Error loading shop type rating data:', error)
  }
}

const updateChart = (categories, data) => {
  if (!chart) return

  const option = {
    backgroundColor: 'transparent',
    title: {
      text: '📊 各类型店铺评分分布',
      left: '3%',
      top: '3%',
      textStyle: {
        color: '#5d4037',
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        if (params.componentSubType === 'boxplot') {
          const data = params.data
          return `
            <div style="padding: 8px;">
              <div style="font-weight: bold; margin-bottom: 5px; color: #5d4037;">${params.name}</div>
              <div style="color: #3e2723;">最高分：${data[5]}</div>
              <div style="color: #3e2723;">上四分位：${data[4]}</div>
              <div style="color: #3e2723;">中位数：${data[3]}</div>
              <div style="color: #3e2723;">下四分位：${data[2]}</div>
              <div style="color: #3e2723;">最低分：${data[1]}</div>
            </div>
          `
        }
        return ''
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
      left: '15%',
      right: '5%',
      bottom: '10%',
      top: '15%',
      containLabel: false
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLabel: {
        color: '#5d4037',
        fontSize: 11,
        interval: 0,
        rotate: 30
      },
      axisLine: {
        lineStyle: {
          color: '#8d6e63'
        }
      },
      axisTick: {
        alignWithLabel: true
      },
      splitLine: {
        show: false
      }
    },
    yAxis: {
      type: 'value',
      name: '评分',
      nameTextStyle: {
        color: '#5d4037',
        fontSize: 12
      },
      min: 3,
      max: 5,
      axisLabel: {
        color: '#5d4037',
        fontSize: 11
      },
      axisLine: {
        lineStyle: {
          color: '#8d6e63'
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(141, 110, 99, 0.1)'
        }
      }
    },
    series: [
      {
        name: '评分分布',
        type: 'boxplot',
        data: data,
        itemStyle: {
          color: 'rgba(156, 39, 176, 0.7)',
          borderColor: '#9c27b0',
          borderWidth: 1.5
        },
        boxWidth: ['40%', '60%'],
        emphasis: {
          itemStyle: {
            color: 'rgba(156, 39, 176, 0.9)',
            shadowBlur: 10,
            shadowColor: 'rgba(156, 39, 176, 0.5)'
          }
        },
        animationDuration: 1000,
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
  height: 100%;
  flex: 1;
  min-height: 300px;
}
</style>
