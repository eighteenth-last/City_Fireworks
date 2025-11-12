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
  const restaurants = await api.hotpot.getPriceDistribution()

  // 价格区间划分
  const priceRanges = [
    { min: 0, max: 60, label: '0-60元' },
    { min: 60, max: 80, label: '60-80元' },
    { min: 80, max: 100, label: '80-100元' },
    { min: 100, max: 120, label: '100-120元' },
    { min: 120, max: 150, label: '120-150元' },
    { min: 150, max: 200, label: '150-200元' },
    { min: 200, max: 999, label: '200元以上' }
  ]

  // 统计各价格区间数量
  const priceData = priceRanges.map(range => {
    const count = restaurants.filter(r =>
      r.price_avg >= range.min && r.price_avg < range.max
    ).length
    const percentage = (count / restaurants.length * 100).toFixed(1)
    return {
      label: range.label,
      count,
      percentage: parseFloat(percentage)
    }
  })

  updateChart(priceData)
}

const updateChart = (data) => {
  if (!chart) return

  const option = {
    backgroundColor: 'transparent',
    toolbox: { show: false },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params) => {
        const item = params[0]
        return `
          <div style="padding: 8px;">
            <div style="font-weight: bold; margin-bottom: 5px;">${item.name}</div>
            <div>门店数: ${item.value} 家</div>
            <div>占比: ${item.data.percentage}%</div>
          </div>
        `
      },
      backgroundColor: 'rgba(10, 15, 28, 0.95)',
      borderColor: '#ff4d4d',
      borderWidth: 1,
      textStyle: {
        color: '#fff'
      }
    },
    grid: {
      left: '8%',
      right: '5%',
      bottom: '15%',
      top: '12%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.label),
      axisLabel: {
        color: '#fff',
        interval: 0,
        rotate: 30,
        fontSize: 11,
        margin: 10
      },
      axisLine: {
        lineStyle: {
          color: '#ff4d4d'
        }
      }
    },
    yAxis: {
      type: 'value',
      name: '门店数',
      nameTextStyle: {
        color: '#fff'
      },
      axisLabel: {
        color: '#fff',
        fontSize: 11
      },
      axisLine: {
        lineStyle: {
          color: '#ff4d4d'
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 77, 77, 0.2)'
        }
      }
    },
    series: [
      {
        name: '门店数',
        type: 'bar',
        data: data.map((item, index) => ({
          value: item.count,
          percentage: item.percentage,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: getBarColor(index, true) },
              { offset: 1, color: getBarColor(index, false) }
            ]),
            borderRadius: index === 2 ? [5, 5, 0, 0] : [0, 0, 0, 0] // 80-100元区间突出显示
          }
        })),
        barWidth: '55%',
        label: {
          show: true,
          position: 'top',
          color: '#ffcccc',
          fontSize: 12,
          fontWeight: 'bold',
          formatter: (params) => {
            return params.data.percentage > 8 ?
              `${params.data.percentage}%` : ''
          }
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: '#ff4d4d'
          }
        },
        animationDelay: (idx) => idx * 100,
        animationDuration: 1000,
        animationEasing: 'cubicOut'
      }
    ]
  }

  chart.setOption(option)
}

const getBarColor = (index, isTop) => {
  const colors = [
    ['#ff9999', '#ff6666'],
    ['#ffaaaa', '#ff7777'],
    ['#ff4d4d', '#ff0000'], // 80-100元区间最突出
    ['#ff8888', '#ff5555'],
    ['#ff7777', '#ff4444'],
    ['#ff6666', '#ff3333'],
    ['#ff5555', '#ff2222']
  ]
  const colorPair = colors[index] || colors[0]
  return isTop ? colorPair[0] : colorPair[1]
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
