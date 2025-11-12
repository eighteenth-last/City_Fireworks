<template>
  <div ref="chartRef" class="chart-container">
    <div v-if="loading" class="loading-overlay">加载中...</div>
    <div v-if="error" class="error-message">{{ error.message }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useECharts } from '../../composables/useECharts'
import { useApi } from '../../composables/useApi'
import api from '../../api'
import { TEA_COLORS } from '../../config/constants'

const chartRef = ref(null)
let intervalId = null

// 使用 Composables
const { setOption, resize: resizeChart } = useECharts(chartRef)
const { data, loading, error, execute } = useApi(api.hotpot.getShopTypeDistribution)

onMounted(async () => {
  await loadData()
  // 设置自动更新
  intervalId = setInterval(loadData, 30000)
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})

const loadData = async () => {
  try {
    const typeData = await execute()
    
    if (!typeData || typeData.length === 0) {
      console.warn('No shop type data available')
      return
    }

    // 计算总数
    const total = typeData.reduce((sum, item) => sum + item.count, 0)

    // 转换为饼图数据
    const chartData = typeData.map(item => {
      const percentage = (item.count / total * 100).toFixed(1)
      return {
        name: item.type,
        value: item.count,
        percentage: parseFloat(percentage),
        itemStyle: {
          color: getTypeColor(item.type)
        }
      }
    }).sort((a, b) => b.value - a.value)

    updateChart(chartData)
  } catch (err) {
    console.error('Error loading shop type data:', err)
  }
}

const updateChart = (data) => {
  const option = {
    backgroundColor: 'transparent',
    toolbox: { show: false },
    title: {
      text: '📊 店铺类型分布',
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
      confine: false,
      appendToBody: true,
      formatter: (params) => {
        return `
          <div style="padding: 8px;">
            <div style="font-weight: bold; margin-bottom: 5px; color: #5d4037;">${params.name}</div>
            <div style="color: #3e2723;">门店数: ${params.value} 家</div>
            <div style="color: #3e2723;">占比: ${params.percent}%</div>
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
    legend: {
      orient: 'vertical',
      left: '5%',
      top: '20%',
      textStyle: {
        color: '#5d4037',
        fontSize: 13
      },
      itemGap: 15,
      itemWidth: 18,
      itemHeight: 14,
      icon: 'rect'
    },
    series: [
      {
        name: '火锅店类型',
        type: 'pie',
        radius: ['30%', '45%'],
        center: ['62%', '52%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2,
          shadowBlur: 8,
          shadowColor: 'rgba(0, 0, 0, 0.1)'
        },
        label: {
          show: false
        },
        emphasis: {
          scale: true,
          scaleSize: 10,
          label: {
            show: false
          },
          itemStyle: {
            shadowBlur: 30,
            shadowOffsetX: 0,
            shadowColor: 'rgba(141, 110, 99, 0.5)',
            shadowOffsetY: 0
          }
        },
        labelLine: {
          show: false
        },
        data: data,
        animationType: 'scale',
        animationEasing: 'elasticOut',
        animationDelay: (idx) => Math.random() * 200,
        animationDuration: 1000
      }
    ]
  }

  setOption(option)
}

const getTypeColor = (type) => {
  const colorMap = {
    '网红店': 'rgba(129, 201, 149, 0.9)',      // 绿色
    '老字号': 'rgba(255, 183, 77, 0.9)',      // 金色
    '社区店': 'rgba(110, 186, 199, 0.9)',      // 青色
    '连锁': 'rgba(185, 103, 255, 0.9)',        // 紫色
    '连锁品牌': 'rgba(107, 141, 214, 0.9)',    // 蓝色
    '高端定制': 'rgba(245, 199, 93, 0.9)',    // 黄色
    '传统小店': 'rgba(232, 139, 139, 0.9)',    // 红色
    '大众': 'rgba(255, 77, 77, 0.9)',          // 火锅红
    '中端': 'rgba(255, 157, 77, 0.9)',        // 橙色
    '精品店': 'rgba(156, 39, 176, 0.9)',      // 深紫色
    '快餐店': 'rgba(255, 152, 0, 0.9)',       // 深橙色
    '其他': 'rgba(153, 153, 153, 0.9)'         // 灰色
  }
  return colorMap[type] || 'rgba(142, 149, 166, 0.9)'
}

// 暴露方法
defineExpose({ resize: resizeChart })
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  min-height: 400px;
  position: relative;
}

.loading-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #8d6e63;
  font-size: 14px;
  z-index: 10;
}

.error-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #d32f2f;
  font-size: 14px;
  text-align: center;
  z-index: 10;
}
</style>
