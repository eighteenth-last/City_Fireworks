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
    const districts = await api.night.getDistrictComparison()

    if (districts && districts.length) {
      // 取活力分数最高的前3个区县作为商圈对比
      const top3 = districts
        .sort((a, b) => b.vitality_score - a.vitality_score)
        .slice(0, 3)
        .map((d) => ({
          name: d.name,
          value: [
            Math.min(d.hotpot_density * 5, 100),  // 商业活力 (火锅密度*5，最大100)
            Math.min(d.vitality_score * 0.9, 100), // 交通便利 (基于活力分数)
            Math.min(d.vitality_score, 100),       // 消费水平
            Math.min(d.population / 10000, 100),   // 人流密度
            Math.min(d.vitality_score * 0.8, 100)  // 文化氛围
          ]
        }))
      updateChart(top3)
    } else {
      console.warn('No district comparison data available')
    }
  } catch (error) {
    console.error('Error loading district radar:', error)
  }
}

const updateChart = (data) => {
  if (!chart) return

  const indicator = [
    { name: '商业活力', max: 100 },
    { name: '交通便利', max: 100 },
    { name: '消费水平', max: 100 },
    { name: '人流密度', max: 100 },
    { name: '文化氛围', max: 100 }
  ]

  const option = {
    backgroundColor: 'transparent',
    toolbox: { show: false },
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        return `
          <div style="padding: 8px;">
            <div style="font-weight: bold; margin-bottom: 5px;">${params.name}</div>
            <div>商业活力: ${params.value[0]}</div>
            <div>交通便利: ${params.value[1]}</div>
            <div>消费水平: ${params.value[2]}</div>
            <div>人流密度: ${params.value[3]}</div>
            <div>文化氛围: ${params.value[4]}</div>
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
      data: data.map(item => item.name),
      top: '5%',
      textStyle: {
        color: '#fff'
      }
    },
    radar: {
      center: ['50%', '55%'],
      radius: '65%',
      indicator: indicator,
      splitNumber: 5,
      name: {
        textStyle: {
          color: '#fff'
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(0, 212, 255, 0.3)'
        }
      },
      splitArea: {
        show: true,
        areaStyle: {
          color: [
            'rgba(0, 212, 255, 0.05)',
            'rgba(0, 212, 255, 0.1)',
            'rgba(0, 212, 255, 0.15)',
            'rgba(0, 212, 255, 0.2)',
            'rgba(0, 212, 255, 0.25)'
          ]
        }
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(0, 212, 255, 0.5)'
        }
      }
    },
    series: [
      {
        name: '商圈对比',
        type: 'radar',
        data: data.map((item, index) => ({
          value: item.value,
          name: item.name,
          lineStyle: {
            color: getDistrictColor(index),
            width: 2
          },
          areaStyle: {
            color: getDistrictColor(index),
            opacity: 0.3
          },
          itemStyle: {
            color: '#fff',
            borderColor: getDistrictColor(index),
            borderWidth: 2
          },
          symbol: 'circle',
          symbolSize: 6
        })),
        emphasis: {
          lineStyle: {
            width: 4
          }
        },
        animationDuration: 1500,
        animationEasing: 'cubicOut'
      }
    ]
  }

  chart.setOption(option)
}

const getDistrictColor = (index) => {
  const colors = [
    '#00d4ff',  // 解放碑
    '#b967ff',  // 观音桥
    '#ff4d4d'   // 洪崖洞
  ]
  return colors[index] || '#999999'
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
