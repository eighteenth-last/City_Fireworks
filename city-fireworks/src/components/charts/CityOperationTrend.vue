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
      updateChart(processData(data))
    } else {
      console.warn('No 24-hour trend data available')
    }
  } catch (error) {
    console.error('Error loading city operation trend:', error)
  }
}

// 处理数据：将24小时数据按3小时区间聚合
const processData = (hourlyData) => {
  const timeRanges = [
    { display: '0', full: '00:00-03:00' },
    { display: '3', full: '03:00-06:00' },
    { display: '6', full: '06:00-09:00' },
    { display: '9', full: '09:00-12:00' },
    { display: '12', full: '12:00-15:00' },
    { display: '15', full: '15:00-18:00' },
    { display: '18', full: '18:00-21:00' },
    { display: '21', full: '21:00-24:00' }
  ]
  
  return timeRanges.map((range, index) => {
    const startHour = index * 3
    const endHour = startHour + 3
    const rangeData = hourlyData.slice(startHour, endHour)
    
    return {
      timeRange: range.display,
      timeRangeFull: range.full,
      population: Math.round(rangeData.reduce((sum, item) => sum + (item.population || 0), 0) / rangeData.length),
      consumption: Math.round(rangeData.reduce((sum, item) => sum + (item.consumption || 0), 0) / rangeData.length),
      activity: Math.round((rangeData.reduce((sum, item) => sum + (item.population || 0), 0) / rangeData.length) / 100)
    }
  })
}

const updateChart = (data) => {
  if (!chart) return

  const option = {
    backgroundColor: 'transparent',
    toolbox: { show: false },
    tooltip: {
      trigger: 'axis',
      confine: false,
      appendToBody: true,
      axisPointer: {
        type: 'cross',
        crossStyle: {
          color: '#ff4d4d',
          width: 1,
          type: 'dashed'
        }
      },
      formatter: (params) => {
        const timeRange = params[0].axisValue
        const dataIndex = params[0].dataIndex
        const currentData = data[dataIndex]
        const fullTimeRange = currentData.timeRangeFull || `${timeRange}:00`
        
        // 如果只有一个参数（悬停在单个图表元素上）
        if (params.length === 1) {
          const param = params[0]
          let value = param.value
          let unit = ''
          if (param.seriesName === '活跃度') {
            unit = '%'
          } else if (param.seriesName === '人流量') {
            unit = ' 人'
          } else {
            unit = ' 元'
          }
          
          return `
            <div style="padding: 10px;">
              <div style="font-weight: bold; margin-bottom: 8px; font-size: 14px; color: #5d4037;">${fullTimeRange}</div>
              <div style="display: flex; align-items: center; font-size: 13px;">
                <span style="display: inline-block; width: 12px; height: 12px; background: ${param.color}; border-radius: 50%; margin-right: 8px;"></span>
                <span style="color: #3e2723;">${param.seriesName}: <b>${value}${unit}</b></span>
              </div>
            </div>
          `
        }
        
        // 悬停在空白区域，显示该时段所有数据
        return `
          <div style="padding: 10px; min-width: 180px;">
            <div style="font-weight: bold; margin-bottom: 8px; font-size: 14px; color: #5d4037;">${fullTimeRange}</div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
              <span style="display: inline-block; width: 10px; height: 10px; background: rgba(0, 212, 255, 0.8); border-radius: 50%; margin-right: 8px;"></span>
              <span style="color: #3e2723;">人流量: <b>${currentData.population}</b> 人</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
              <span style="display: inline-block; width: 10px; height: 10px; background: rgba(185, 103, 255, 0.8); border-radius: 50%; margin-right: 8px;"></span>
              <span style="color: #3e2723;">消费额: <b>${currentData.consumption}</b> 元</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
              <span style="display: inline-block; width: 10px; height: 10px; background: #ffb800; border-radius: 50%; margin-right: 8px;"></span>
              <span style="color: #3e2723;">活跃度: <b>${currentData.activity}%</b></span>
            </div>
          </div>
        `
      },
      backgroundColor: 'rgba(255, 253, 246, 0.98)',
      borderColor: '#8d6e63',
      borderWidth: 2,
      textStyle: {
        color: '#3e2723'
      },
      extraCssText: 'box-shadow: 6px 6px 0 #d7ccc8; z-index: 9999;',
      position: function (point, params, dom, rect, size) {
        // 智能定位：避免超出边界
        const x = point[0]
        const y = point[1]
        const boxWidth = size.contentSize[0]
        const boxHeight = size.contentSize[1]
        const viewWidth = size.viewSize[0]
        const viewHeight = size.viewSize[1]
        
        let posX = x + 10
        let posY = y - boxHeight / 2
        
        // 如果右侧空间不够，显示在左侧
        if (posX + boxWidth > viewWidth) {
          posX = x - boxWidth - 10
        }
        
        // 如果上方空间不够，向下调整
        if (posY < 0) {
          posY = 10
        }
        
        // 如果下方空间不够，向上调整
        if (posY + boxHeight > viewHeight) {
          posY = viewHeight - boxHeight - 10
        }
        
        return [posX, posY]
      }
    },
    legend: {
      data: ['人流量', '消费额', '活跃度'],
      top: 0,
      textStyle: {
        color: '#5d4037',
        fontSize: 8
      },
      itemWidth: 12,
      itemHeight: 6,
      itemGap: 5
    },
    grid: {
      left: '8%',
      right: '8%',
      bottom: '22px',
      top: '18px',
      containLabel: false
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.timeRange),
      axisLabel: {
        show: true,
        color: '#8d6e63',
        fontSize: 8,
        rotate: 0,
        interval: 0,
        margin: 3,
        fontWeight: 'normal',
        formatter: (value) => value
      },
      axisLine: {
        show: true,
        lineStyle: {
          color: '#ff4d4d',
          width: 2
        }
      },
      axisTick: {
        show: true,
        alignWithLabel: true,
        length: 5,
        lineStyle: {
          color: '#ff4d4d',
          width: 1
        }
      },
      splitLine: {
        show: false
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '人流量/消费额',
        position: 'left',
        nameTextStyle: {
          color: '#8d6e63',
          fontSize: 7
        },
        axisLabel: {
          color: '#8d6e63',
          fontSize: 6
        },
        axisLine: {
          lineStyle: {
            color: '#00d4ff'
          }
        },
        splitLine: {
          lineStyle: {
            color: 'rgba(0, 212, 255, 0.1)'
          }
        }
      },
      {
        type: 'value',
        name: '活跃度(%)',
        position: 'right',
        max: 100,
        nameTextStyle: {
          color: '#8d6e63',
          fontSize: 7
        },
        axisLabel: {
          color: '#8d6e63',
          fontSize: 6,
          formatter: '{value}%'
        },
        axisLine: {
          lineStyle: {
            color: '#ffb800'
          }
        },
        splitLine: {
          show: false
        }
      }
    ],
    series: [
      {
        name: '人流量',
        type: 'bar',
        yAxisIndex: 0,
        data: data.map(item => item.population),
        barGap: '10%',
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(0, 212, 255, 0.9)' },
            { offset: 1, color: 'rgba(0, 212, 255, 0.3)' }
          ]),
          borderRadius: [4, 4, 0, 0],
          shadowColor: '#00d4ff',
          shadowBlur: 10
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(0, 212, 255, 1)' },
              { offset: 1, color: 'rgba(0, 212, 255, 0.5)' }
            ])
          }
        },
        animationDuration: 1500,
        animationEasing: 'cubicOut'
      },
      {
        name: '消费额',
        type: 'bar',
        yAxisIndex: 0,
        data: data.map(item => item.consumption),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(185, 103, 255, 0.9)' },
            { offset: 1, color: 'rgba(185, 103, 255, 0.3)' }
          ]),
          borderRadius: [4, 4, 0, 0],
          shadowColor: '#b967ff',
          shadowBlur: 10
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(185, 103, 255, 1)' },
              { offset: 1, color: 'rgba(185, 103, 255, 0.5)' }
            ])
          }
        },
        animationDuration: 1500,
        animationEasing: 'cubicOut',
        animationDelay: 200
      },
      {
        name: '活跃度',
        type: 'line',
        yAxisIndex: 1,
        data: data.map(item => item.activity),
        smooth: true,
        lineStyle: {
          width: 2,
          color: '#ffb800',
          shadowColor: '#ffb800',
          shadowBlur: 8
        },
        itemStyle: {
          color: '#ffb800',
          borderColor: '#fff',
          borderWidth: 2
        },
        symbolSize: 4,
        emphasis: {
          itemStyle: {
            color: '#ffb800',
            borderWidth: 3,
            shadowBlur: 15
          }
        },
        animationDuration: 2000,
        animationEasing: 'cubicOut',
        animationDelay: 400
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
  height: 220px;
}
</style>
