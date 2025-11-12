<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import api from '../../api'

const chartRef = ref(null)
let chartInstance = null

const initChart = async () => {
  if (!chartRef.value) return

  chartInstance = echarts.init(chartRef.value)

  try {
    // 从后端 API 获取数据
    const [districts, densityMatrix, restaurants] = await Promise.all([
      api.map.getDistrictBoundaries(),
      api.hotpot.getDensityMatrix(),
      api.map.getHotpotPoints()
    ])

    const colors = ['#42a5f5', '#66bb6a', '#ffa726', '#ef5350', '#ab47bc', '#26c6da', '#ffee58', '#8d6e63']
    
    // 处理数据
    const data = districts.slice(0, 8).map(district => {
      const districtRestaurants = restaurants.filter(r => r.district_id === district.id)
      const avgRating = districtRestaurants.length > 0
        ? districtRestaurants.reduce((sum, r) => sum + (r.rating || 0), 0) / districtRestaurants.length
        : 0
      const avgPrice = districtRestaurants.length > 0
        ? districtRestaurants.reduce((sum, r) => sum + (r.price_avg || 0), 0) / districtRestaurants.length
        : 0
      const avg24h = districtRestaurants.filter(r => r.is_24h).length
      const avgHours = avg24h > 0 ? 24 : 14 // 简化处理

      return [
        districtRestaurants.length,  // 火锅店数量
        district.hotpot_density || 0,    // 密度(每平方公里)
        avgRating.toFixed(1), // 平均评分
        Math.round(avgPrice),    // 人均消费
        avgHours      // 营业时长
      ]
    })

    const districtNames = districts.slice(0, 8).map(d => d.name)

  const option = {
    title: {
      text: '多维度平行坐标分析',
      left: 'center',
      top: 10,
      textStyle: {
        color: '#5d4037',
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    backgroundColor: 'transparent',
    legend: {
      top: 45,
      right: 20,
      orient: 'vertical',
      data: districtNames.map((name, index) => ({
        name: name,
        icon: 'roundRect',
        itemStyle: {
          color: colors[index]
        }
      })),
      textStyle: {
        color: '#5d4037',
        fontSize: 11
      },
      itemWidth: 20,
      itemHeight: 3,
      itemGap: 8
    },
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 253, 246, 0.95)',
      borderColor: '#8d6e63',
      borderWidth: 2,
      textStyle: {
        color: '#5d4037',
        fontSize: 13
      },
      formatter: function(params) {
        const districtName = params.seriesName
        const values = params.value
        return `<div style="padding: 5px;">
                <strong style="font-size: 14px; color: #5d4037;">${districtName}</strong><br/>
                <div style="margin-top: 8px; line-height: 1.8;">
                  火锅店数量: <strong>${values[0]}</strong> 家<br/>
                  密度: <strong>${values[1]}</strong> 店/km²<br/>
                  平均评分: <strong>${values[2]}</strong> 分<br/>
                  人均消费: <strong>${values[3]}</strong> 元<br/>
                  营业时长: <strong>${values[4]}</strong> 小时
                </div>
                </div>`
      }
    },
    parallelAxis: [
      {
        dim: 0,
        name: '火锅店数量',
        min: 0,
        max: 600,
        nameTextStyle: {
          color: '#8d6e63',
          fontSize: 12
        },
        axisLine: {
          lineStyle: {
            color: '#d7ccc8'
          }
        },
        axisLabel: {
          color: '#8d6e63',
          fontSize: 11
        }
      },
      {
        dim: 1,
        name: '密度(店/km²)',
        min: 0,
        max: 50,
        nameTextStyle: {
          color: '#8d6e63',
          fontSize: 12
        },
        axisLine: {
          lineStyle: {
            color: '#d7ccc8'
          }
        },
        axisLabel: {
          color: '#8d6e63',
          fontSize: 11
        }
      },
      {
        dim: 2,
        name: '平均评分',
        min: 3.0,
        max: 5.0,
        nameTextStyle: {
          color: '#8d6e63',
          fontSize: 12
        },
        axisLine: {
          lineStyle: {
            color: '#d7ccc8'
          }
        },
        axisLabel: {
          color: '#8d6e63',
          fontSize: 11
        }
      },
      {
        dim: 3,
        name: '人均消费(元)',
        min: 0,
        max: 150,
        nameTextStyle: {
          color: '#8d6e63',
          fontSize: 12
        },
        axisLine: {
          lineStyle: {
            color: '#d7ccc8'
          }
        },
        axisLabel: {
          color: '#8d6e63',
          fontSize: 11
        }
      },
      {
        dim: 4,
        name: '营业时长(小时)',
        min: 0,
        max: 24,
        nameTextStyle: {
          color: '#8d6e63',
          fontSize: 12
        },
        axisLine: {
          lineStyle: {
            color: '#d7ccc8'
          }
        },
        axisLabel: {
          color: '#8d6e63',
          fontSize: 11
        }
      }
    ],
    parallel: {
      left: '8%',
      right: '18%',
      top: '22%',
      bottom: '12%',
      parallelAxisDefault: {
        type: 'value',
        nameLocation: 'end',
        nameGap: 20,
        nameTextStyle: {
          fontSize: 13,
          fontWeight: 'bold'
        },
        splitLine: {
          show: true,
          lineStyle: {
            color: 'rgba(141, 110, 99, 0.1)',
            type: 'dashed'
          }
        },
        axisTick: {
          show: false
        },
        axisLine: {
          lineStyle: {
            width: 2
          }
        }
      }
    },
    series: districtNames.map((district, index) => ({
      name: district,
      type: 'parallel',
      lineStyle: {
        width: 2.5,
        opacity: 0.6,
        color: colors[index]
      },
      emphasis: {
        lineStyle: {
          width: 4,
          opacity: 1,
          shadowBlur: 10,
          shadowColor: colors[index]
        }
      },
      data: [data[index]]
    }))
  }

  chartInstance.setOption(option)
  } catch (error) {
    console.error('Error loading parallel analysis data:', error)
  }
}

const resize = () => {
  chartInstance?.resize()
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', resize)
})

onUnmounted(() => {
  window.removeEventListener('resize', resize)
  chartInstance?.dispose()
})

defineExpose({ resize })
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  min-height: 300px;
}
</style>
