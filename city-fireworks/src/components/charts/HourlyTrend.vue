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
    const data = await api.night.get24HourTrend()
    if (data && data.length) {
      updateChart(data)
    } else {
      console.warn('No 24-hour trend data available')
    }
  } catch (error) {
    console.error('Error loading hourly trend:', error)
  }
}

const updateChart = (data) => {
  if (!chart) return

  const option = {
    backgroundColor: 'transparent',
    toolbox: { show: false },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      formatter: (params) => {
        const hour = params[0].axisValue
        const population = params[0].value
        const consumption = params[1].value
        return `
          <div style="padding: 8px;">
            <div style="font-weight: bold; margin-bottom: 5px;">${hour}点</div>
            <div>人流量: ${population} 人</div>
            <div>消费额: ${consumption} 元</div>
          </div>
        `
      },
      backgroundColor: 'rgba(10, 15, 28, 0.95)',
      borderColor: '#00d4ff',
      borderWidth: 1,
      textStyle: {
        color: '#fff'
      }
    },
    legend: {
      data: ['人流量', '消费额'],
      top: 0,
      textStyle: {
        color: '#fff'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: data.map(item => item.hour),
      axisLabel: {
        color: '#fff',
        formatter: (value) => `${value}:00`
      },
      axisLine: {
        lineStyle: {
          color: '#00d4ff'
        }
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '人流量',
        position: 'left',
        nameTextStyle: {
          color: '#fff'
        },
        axisLabel: {
          color: '#fff'
        },
        axisLine: {
          lineStyle: {
            color: '#00d4ff'
          }
        },
        splitLine: {
          lineStyle: {
            color: 'rgba(0, 212, 255, 0.2)'
          }
        }
      },
      {
        type: 'value',
        name: '消费额',
        position: 'right',
        nameTextStyle: {
          color: '#fff'
        },
        axisLabel: {
          color: '#fff'
        },
        axisLine: {
          lineStyle: {
            color: '#b967ff'
          }
        }
      }
    ],
    series: [
      {
        name: '人流量',
        type: 'line',
        yAxisIndex: 0,
        data: data.map(item => item.population),
        smooth: true,
        lineStyle: {
          width: 3,
          color: '#00d4ff',
          shadowColor: '#00d4ff',
          shadowBlur: 10
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(0, 212, 255, 0.5)' },
            { offset: 1, color: 'rgba(0, 212, 255, 0)' }
          ])
        },
        emphasis: {
          focus: 'series'
        },
        animationDuration: 2000,
        animationEasing: 'cubicOut'
      },
      {
        name: '消费额',
        type: 'line',
        yAxisIndex: 1,
        data: data.map(item => item.consumption),
        smooth: true,
        lineStyle: {
          width: 3,
          color: '#b967ff',
          shadowColor: '#b967ff',
          shadowBlur: 10
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(185, 103, 255, 0.5)' },
            { offset: 1, color: 'rgba(185, 103, 255, 0)' }
          ])
        },
        emphasis: {
          focus: 'series'
        },
        animationDuration: 2000,
        animationEasing: 'cubicOut'
      },
      {
        // 21:00峰值标注
        name: '峰值',
        type: 'scatter',
        data: [
          [21, data[21]?.population || 0, data[21]?.consumption || 0]
        ],
        symbolSize: 20,
        itemStyle: {
          color: '#ff4d4d',
          borderColor: '#fff',
          borderWidth: 2,
          shadowColor: '#ff4d4d',
          shadowBlur: 20
        },
        label: {
          show: true,
          formatter: '峰值21:00',
          position: 'top',
          color: '#ff4d4d',
          fontSize: 12,
          fontWeight: 'bold'
        },
        animationDelay: 1000
      }
    ]
  }

  chart.setOption(option)
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
.chart-container {
  width: 100%;
  height: 250px;
}
</style>
