/**
 * ECharts 公共 Composable
 * 统一管理 ECharts 实例的创建、更新和销毁
 */
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

export function useECharts(chartRef) {
  const chartInstance = ref(null)
  const loading = ref(false)

  /**
   * 初始化图表
   */
  const initChart = () => {
    if (!chartRef.value) return null
    
    if (chartInstance.value) {
      chartInstance.value.dispose()
    }
    
    chartInstance.value = echarts.init(chartRef.value)
    return chartInstance.value
  }

  /**
   * 设置图表配置
   */
  const setOption = (option, notMerge = false) => {
    if (!chartInstance.value) {
      initChart()
    }
    chartInstance.value?.setOption(option, notMerge)
  }

  /**
   * 显示加载动画
   */
  const showLoading = () => {
    loading.value = true
    chartInstance.value?.showLoading('default', {
      text: '加载中...',
      color: '#8d6e63',
      textColor: '#5d4037',
      maskColor: 'rgba(255, 253, 246, 0.8)'
    })
  }

  /**
   * 隐藏加载动画
   */
  const hideLoading = () => {
    loading.value = false
    chartInstance.value?.hideLoading()
  }

  /**
   * 调整图表大小
   */
  const resize = () => {
    chartInstance.value?.resize()
  }

  /**
   * 销毁图表实例
   */
  const dispose = () => {
    chartInstance.value?.dispose()
    chartInstance.value = null
  }

  /**
   * 清空图表
   */
  const clear = () => {
    chartInstance.value?.clear()
  }

  // 自动处理窗口大小变化
  onMounted(() => {
    window.addEventListener('resize', resize)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', resize)
    dispose()
  })

  return {
    chartInstance,
    loading,
    initChart,
    setOption,
    showLoading,
    hideLoading,
    resize,
    dispose,
    clear
  }
}
