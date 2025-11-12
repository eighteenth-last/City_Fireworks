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
  const brands = await api.hotpot.getBrandDistribution()

  // 转换为图表数据格式
  const chartData = brands.map(brand => ({
    name: brand.name,
    value: brand.store_count,
    marketShare: brand.market_share,
    itemStyle: {
      color: getBrandColor(brand.id)
    }
  })).sort((a, b) => b.value - a.value)

  updateChart(chartData)
}

const updateChart = (data) => {
  if (!chart) return

  const option = {
    backgroundColor: 'transparent',
    toolbox: { show: false },
    title: {
      text: '🏢 品牌分布排行',
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
        return `
          <div style="padding: 8px;">
            <div style="font-weight: bold; margin-bottom: 5px; color: #5d4037;">${params.name}</div>
            <div style="color: #3e2723;">门店数量：${params.value} 家</div>
            <div style="color: #3e2723;">市场占比：${params.data.marketShare}%</div>
          </div>
        `
      },
      backgroundColor: 'rgba(255, 253, 246, 0.98)',
      borderColor: '#8d6e63',
      borderWidth: 2,
      textStyle: {
        color: '#3e2723'
      },
      extraCssText: 'box-shadow: 6px 6px 0 #d7ccc8; z-index: 99999 !important;'
    },
    grid: {
      left: '3%',
      right: '5%',
      bottom: '3%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLabel: {
        color: '#5d4037',
        fontSize: 12
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
    yAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisLabel: {
        color: '#5d4037',
        fontSize: 12,
        margin: 10
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
    series: [
      {
        name: '门店数量',
        type: 'bar',
        data: data.map((item, index) => ({
          value: item.value,
          marketShare: item.marketShare,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
              { offset: 0, color: getBarGradientColor(index, 0) },
              { offset: 1, color: getBarGradientColor(index, 1) }
            ]),
            borderRadius: [0, 4, 4, 0]
          },
          label: {
            show: true,
            position: 'right',
            color: '#5d4037',
            fontSize: 12,
            fontWeight: 'bold',
            formatter: (params) => {
              return `${params.value} 家 (${params.data.marketShare}%)`
            }
          }
        })),
        barWidth: '60%',
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(141, 110, 99, 0.3)',
            shadowOffsetX: 2
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

const getBrandColor = (id) => {
  const colors = [
    'rgba(129, 201, 149, 0.9)',  // 绿色
    'rgba(255, 183, 77, 0.9)',   // 金色
    'rgba(110, 186, 199, 0.9)',  // 青色
    'rgba(185, 103, 255, 0.9)',  // 紫色
    'rgba(107, 141, 214, 0.9)',  // 蓝色
    'rgba(245, 199, 93, 0.9)',   // 黄色
    'rgba(232, 139, 139, 0.9)',  // 红色
    'rgba(255, 157, 77, 0.9)',   // 橙色
    'rgba(156, 39, 176, 0.9)',   // 深紫色
    'rgba(255, 152, 0, 0.9)'     // 深橙色
  ]
  return colors[(id - 1) % colors.length]
}

const getBarGradientColor = (index, position) => {
  const baseColors = [
    ['#81c995', '#4caf50'],  // 绿色渐变
    ['#ffb74d', '#ff9800'],  // 金色渐变
    ['#6ebac7', '#00bcd4'],  // 青色渐变
    ['#b967ff', '#9c27b0'],  // 紫色渐变
    ['#6b8dd6', '#3f51b5'],  // 蓝色渐变
    ['#f5c75d', '#ffc107'],  // 黄色渐变
    ['#e88b8b', '#f44336'],  // 红色渐变
    ['#ff9d4d', '#ff5722'],  // 橙色渐变
    ['#9c27b0', '#673ab7'],  // 深紫渐变
    ['#ff9800', '#ff6f00']   // 深橙渐变
  ]
  const colorPair = baseColors[index % baseColors.length]
  return colorPair[position]
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
  height: 100%;
  min-height: 400px;
}
</style>
