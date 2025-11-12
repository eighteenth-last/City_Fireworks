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
  const data = await api.hotpot.getDensityMatrix()

  // 取前9个区县（九宫格）
  const top9 = data.slice(0, 9)

  // 构建九宫格数据
  const matrixData = []
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      const index = i * 3 + j
      if (index < top9.length) {
        const item = top9[index]
        matrixData.push({
          name: item.district,
          value: [j, i, item.density, item.count],
          density: item.density,
          count: item.count
        })
      } else {
        matrixData.push({
          name: '暂无数据',
          value: [j, i, 0, 0],
          density: 0,
          count: 0
        })
      }
    }
  }

  updateChart(matrixData)
}

const updateChart = (data) => {
  if (!chart) return

  const option = {
    backgroundColor: 'transparent',
    toolbox: { show: false },
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        const data = params.data
        return `
          <div style="padding: 8px;">
            <div style="font-weight: bold; margin-bottom: 5px;">${data.name}</div>
            <div>密度: ${data.density.toFixed(2)} 家/km²</div>
            <div>门店数: ${data.count} 家</div>
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
      left: '5%',
      right: '5%',
      top: '10%',
      bottom: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      min: 0,
      max: 2,
      interval: 1,
      show: false
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 2,
      interval: 1,
      show: false
    },
    series: [
      {
        type: 'custom',
        renderItem: (params, api) => {
          const xIndex = api.value(0)
          const yIndex = api.value(1)
          const density = api.value(2)
          const count = api.value(3)

          const center = api.coord([xIndex, yIndex])
          const size = api.size([1, 1])
          const halfWidth = size[0] / 2 * 0.8
          const halfHeight = size[1] / 2 * 0.8

          // 颜色根据密度变化
          const color = getColorByDensity(density)

          return {
            type: 'group',
            children: [
              {
                type: 'rect',
                shape: {
                  x: center[0] - halfWidth,
                  y: center[1] - halfHeight,
                  width: halfWidth * 2,
                  height: halfHeight * 2
                },
                style: {
                  fill: color,
                  stroke: '#ff4d4d',
                  lineWidth: 2,
                  opacity: 0.8
                }
              },
              {
                type: 'text',
                style: {
                  text: `${density.toFixed(1)}`,
                  x: center[0],
                  y: center[1] - 5,
                  textAlign: 'center',
                  textVerticalAlign: 'middle',
                  fontSize: 18,
                  fontWeight: 'bold',
                  fill: '#fff'
                }
              },
              {
                type: 'text',
                style: {
                  text: `${count}家`,
                  x: center[0],
                  y: center[1] + 15,
                  textAlign: 'center',
                  textVerticalAlign: 'middle',
                  fontSize: 12,
                  fill: '#ffcccc'
                }
              }
            ]
          }
        },
        data: data,
        animationDuration: 1000,
        animationEasing: 'cubicOut'
      }
    ]
  }

  chart.setOption(option)
}

const getColorByDensity = (density) => {
  if (density < 5) return 'rgba(255, 212, 212, 0.8)'
  if (density < 10) return 'rgba(255, 153, 153, 0.8)'
  if (density < 15) return 'rgba(255, 102, 102, 0.8)'
  if (density < 20) return 'rgba(255, 51, 51, 0.8)'
  return 'rgba(255, 0, 0, 0.8)'
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
