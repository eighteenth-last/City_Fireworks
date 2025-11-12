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

  chart = echarts.init(chartRef.value)
  await loadData()

  intervalId = setInterval(loadData, 30000)
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
    console.log('Loading district merchant data...')
    // 获取火锅店列表数据（包含 district_id）
    const restaurants = await api.map.getHotpotPoints()
    console.log('Restaurants loaded:', restaurants.length)
    
    // 按区域统计商户数量
    const districtMap = new Map()
    restaurants.forEach(r => {
      const districtId = r.district_id
      if (!districtId) return
      
      if (!districtMap.has(districtId)) {
        districtMap.set(districtId, {
          count: 0,
          name: ''
        })
      }
      districtMap.get(districtId).count++
    })

    // 获取区域名称（使用后端 API）
    const districts = await api.map.getDistrictBoundaries()
    console.log('Districts loaded:', districts.length)
    
    districts.forEach(d => {
      if (districtMap.has(d.id)) {
        districtMap.get(d.id).name = d.name
      }
    })

    // 转换为数组并排序，取前10
    const data = Array.from(districtMap.values())
      .filter(item => item.name)
      .sort((a, b) => b.count - a.count)
      .slice(0, 10)

    console.log('Chart data prepared:', data)
    
    if (data.length > 0) {
      updateChart(data)
    } else {
      console.warn('No data to display')
    }
  } catch (error) {
    console.error('Error loading district merchant data:', error)
  }
}

const updateChart = (data) => {
  if (!chart) return

  const option = {
    backgroundColor: 'transparent',
    title: {
      text: '📍 区域商户数量TOP10',
      left: '3%',
      top: '3%',
      textStyle: {
        color: '#5d4037',
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params) => {
        const item = params[0]
        return `
          <div style="padding: 8px;">
            <div style="font-weight: bold; margin-bottom: 5px; color: #5d4037;">${item.name}</div>
            <div style="color: #3e2723;">商户数量：${item.value} 家</div>
          </div>
        `
      },
      backgroundColor: 'rgba(255, 253, 246, 0.98)',
      borderColor: '#8d6e63',
      borderWidth: 2,
      textStyle: {
        color: '#3e2723'
      },
      extraCssText: 'box-shadow: 6px 6px 0 #d7ccc8;'
    },
    grid: {
      left: '1%',
      right: '1%',
      bottom: '5%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisLabel: {
        color: '#5d4037',
        fontSize: 11,
        interval: 0,
        rotate: 30
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
    yAxis: {
      type: 'value',
      name: '商户数量',
      nameTextStyle: {
        color: '#5d4037',
        fontSize: 12
      },
      axisLabel: {
        color: '#5d4037',
        fontSize: 11
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
    series: [
      {
        name: '商户数量',
        type: 'bar',
        data: data.map(item => ({
          value: item.count,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#4caf50' },
              { offset: 1, color: '#81c995' }
            ]),
            borderRadius: [4, 4, 0, 0]
          }
        })),
        barWidth: '50%',
        label: {
          show: false
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(76, 175, 80, 0.5)'
          }
        },
        animationDelay: (idx) => idx * 50,
        animationDuration: 1000,
        animationEasing: 'cubicOut'
      }
    ]
  }

  chart.setOption(option)
}

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
  flex: 1;
  min-height: 200px;
}
</style>
