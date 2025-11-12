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
    // 获取火锅店列表数据
    const restaurants = await api.map.getHotpotPoints()
    
    // 定义时段
    const timeSlots = [
      { label: '14-16小时', min: 14, max: 16 },
      { label: '10-12小时', min: 10, max: 12 },
      { label: '8-10小时', min: 8, max: 10 },
      { label: '12-14小时', min: 12, max: 14 },
      { label: '24小时', min: 24, max: 24 }
    ]

    // 统计各时段数量
    const data = timeSlots.map(slot => {
      let count = 0
      restaurants.forEach(r => {
        if (r.is_24h && slot.min === 24) {
          count++
        } else if (!r.is_24h && r.business_hours) {
          const hours = calculateBusinessHours(r.business_hours)
          if (hours >= slot.min && hours < slot.max) {
            count++
          }
        }
      })
      return {
        label: slot.label,
        value: count
      }
    })

    updateChart(data)
  } catch (error) {
    console.error('Error loading time slot data:', error)
  }
}

const calculateBusinessHours = (businessHours) => {
  // 解析营业时间，例如 "10:00-23:00"
  const match = businessHours.match(/(\d+):(\d+)-(\d+):(\d+)/)
  if (match) {
    const startHour = parseInt(match[1])
    const startMin = parseInt(match[2])
    const endHour = parseInt(match[3])
    const endMin = parseInt(match[4])
    
    let hours = endHour - startHour
    if (endMin < startMin) {
      hours -= 1
    }
    return hours
  }
  return 0
}

const updateChart = (data) => {
  if (!chart) return

  const option = {
    backgroundColor: 'transparent',
    title: {
      text: '⏰ 营业时长分布',
      left: '3%',
      top: '3%',
      textStyle: {
        color: '#5d4037',
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params) => {
        const item = params[0]
        return `
          <div style="padding: 8px;">
            <div style="font-weight: bold; margin-bottom: 5px; color: #5d4037;">${item.name}</div>
            <div style="color: #3e2723;">商户数量：${item.value} 家</div>
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
      left: '10%',
      right: '5%',
      bottom: '5%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.label),
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
      }
    },
    yAxis: {
      type: 'value',
      name: '商户数量',
      nameTextStyle: {
        color: '#5d4037',
        fontSize: 12
      },
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
        name: '商户数量',
        type: 'bar',
        data: data.map(item => ({
          value: item.value,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#ff9800' },
              { offset: 1, color: '#ffb74d' }
            ]),
            borderRadius: [4, 4, 0, 0]
          }
        })),
        barWidth: '50%',
        label: {
          show: false
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(255, 152, 0, 0.5)'
          }
        },
        animationDelay: (idx) => idx * 50,
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
