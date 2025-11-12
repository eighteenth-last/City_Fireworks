<template>
  <div class="chart-container">
    <div ref="chartRef" class="chart-content"></div>
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
const rankingData = ref([])

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
    const data = await api.insight.getDistrictVitalityRanking()
    
    // 转换后端数据格式为前端需要的格式
    if (data && data.length > 0) {
      rankingData.value = data.map((district, index) => ({
        name: district.name,
        score: district.vitality_score || 0,
        rank: index + 1
      }))
    } else {
      // 提供默认数据
      rankingData.value = [
        { name: '渝中区', score: 89.2, rank: 1 },
        { name: '江北区', score: 85.6, rank: 2 },
        { name: '南岸区', score: 83.1, rank: 3 },
        { name: '沙坪坝区', score: 81.5, rank: 4 },
        { name: '九龙坡区', score: 79.8, rank: 5 }
      ]
    }
    loaded.value = true
    updateChart()
  } catch (error) {
    console.error('Error loading vitality ranking:', error)
    // 提供默认数据
    rankingData.value = [
      { name: '渝中区', score: 89.2, rank: 1 },
      { name: '江北区', score: 85.6, rank: 2 },
      { name: '南岸区', score: 83.1, rank: 3 },
      { name: '沙坪坝区', score: 81.5, rank: 4 },
      { name: '九龙坡区', score: 79.8, rank: 5 }
    ]
    loaded.value = true
    updateChart()
  }
}

const updateChart = () => {
  if (!chart || !rankingData.value.length) return

  const option = {
    backgroundColor: 'transparent',
    title: {
      text: '区县活力TOP5',
      left: 'center',
      top: 10,
      textStyle: {
        color: '#5d4037',
        fontSize: 16
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        return `
          <div style="padding: 8px;">
            <div style="font-weight: bold; margin-bottom: 5px;">${params.name}</div>
            <div>活力指数: ${params.value}分</div>
            <div>排名: 第${params.dataIndex + 1}名</div>
          </div>
        `
      },
      backgroundColor: 'rgba(255, 253, 246, 0.98)',
      borderColor: '#8d6e63',
      borderWidth: 2,
      textStyle: {
        color: '#3e2723'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '20%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: rankingData.value.slice(0, 5).map(item => item.name),
      axisLabel: {
        color: '#8d6e63',
        interval: 0,
        rotate: 45,
        fontSize: 10
      },
      axisLine: {
        lineStyle: {
          color: '#8d6e63'
        }
      }
    },
    yAxis: {
      type: 'value',
      name: '活力指数',
      nameTextStyle: {
        color: '#8d6e63'
      },
      axisLabel: {
        color: '#8d6e63'
      },
      axisLine: {
        lineStyle: {
          color: '#8d6e63'
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(141, 110, 99, 0.2)'
        }
      }
    },
    series: [
      {
        name: '活力指数',
        type: 'bar',
        data: rankingData.value.slice(0, 5).map((item, index) => ({
          value: item.score,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: getRankColor(index, true) },
              { offset: 1, color: getRankColor(index, false) }
            ]),
            borderRadius: [5, 5, 0, 0]
          }
        })),
        barWidth: '50%',
        label: {
          show: true,
          position: 'top',
          color: '#5d4037',
          fontSize: 12,
          fontWeight: 'bold',
          formatter: '{c}分'
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 20,
            shadowColor: '#8d6e63'
          }
        },
        animationDelay: (idx) => idx * 200,
        animationDuration: 1000,
        animationEasing: 'cubicOut'
      }
    ]
  }

  chart.setOption(option)
}

const getRankColor = (index, isTop) => {
  const colors = [
    ['#c62828', '#8d6e63'],  // 第1名
    ['#8d6e63', '#a1887f'],  // 第2名
    ['#a1887f', '#bcaaa4'],  // 第3名
    ['#bcaaa4', '#d7ccc8'],  // 第4名
    ['#d7ccc8', '#efebe9']   // 第5名
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
  width: 375px;
  height: 340px;
  position: relative;
}

.chart-content {
  width: 100%;
  height: 100%;
}

.loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #999;
}

</style>
