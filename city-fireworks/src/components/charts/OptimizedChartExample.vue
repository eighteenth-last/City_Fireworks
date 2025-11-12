<!--
  优化后的图表组件示例
  展示如何使用公共 Composables 简化代码
-->
<template>
  <div ref="chartRef" class="chart-container">
    <div v-if="loading" class="loading-overlay">加载中...</div>
    <div v-if="error" class="error-message">{{ error.message }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useECharts } from '../../composables/useECharts'
import { useApi } from '../../composables/useApi'
import api from '../../api'
import { TEA_COLORS, CHART_DEFAULTS } from '../../config/constants'

const chartRef = ref(null)

// 使用 ECharts Composable
const { setOption, showLoading, hideLoading, resize } = useECharts(chartRef)

// 使用 API Composable
const { data, loading, error, execute } = useApi(api.hotpot.getRanking)

// 初始化图表
const initChart = async () => {
  showLoading()
  
  try {
    const rankingData = await execute()
    
    const option = {
      ...CHART_DEFAULTS,
      title: {
        text: '火锅密度排行',
        textStyle: {
          color: TEA_COLORS.deepDark,
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      xAxis: {
        type: 'category',
        data: rankingData.map(item => item.name)
      },
      yAxis: {
        type: 'value'
      },
      series: [{
        type: 'bar',
        data: rankingData.map(item => item.count),
        itemStyle: {
          color: TEA_COLORS.primary
        }
      }]
    }
    
    setOption(option)
  } catch (err) {
    console.error('Failed to load chart data:', err)
  } finally {
    hideLoading()
  }
}

onMounted(() => {
  initChart()
})

// 暴露 resize 方法供父组件调用
defineExpose({ resize })
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.loading-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #8d6e63;
  font-size: 14px;
}

.error-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #d32f2f;
  font-size: 14px;
  text-align: center;
}
</style>
