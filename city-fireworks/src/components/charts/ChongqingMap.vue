<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import api from '../../api'

const chartRef = ref(null)
let chart = null
let districtData = new Map()

onMounted(async () => {
  if (!chartRef.value) return

  // 初始化图表
  chart = echarts.init(chartRef.value)
  chart.showLoading()

  try {
    // 并行加载所有数据（地图 JSON 仍从本地加载，其他数据从 API 获取）
    const [geoResponse, districts, hotpots, teahouses] = await Promise.all([
      fetch('/data/CQ.json'),
      api.map.getDistrictBoundaries(),
      api.map.getHotpotPoints(),
      api.map.getTeahousePoints()
    ])
    
    const geoJson = await geoResponse.json()
    
    // 统计每个区县的数据
    processDistrictData(districts, hotpots, teahouses)
    
    chart.hideLoading()
    
    // 注册地图
    echarts.registerMap('CQ', geoJson)
    
    // 设置图表配置
    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'item',
        formatter: (params) => {
          let districtName = params.name
          // 尝试映射名称
          const mappedName = districtNameMap[districtName] || districtName
          const data = districtData.get(mappedName)
          
          if (!data) {
            return `<div style="padding: 10px;"><strong>${districtName}</strong></div>`
          }
          
          return `
            <div style="padding: 12px; min-width: 200px;">
              <div style="font-weight: bold; margin-bottom: 10px; font-size: 16px; color: #5d4037; border-bottom: 2px dashed #8d6e63; padding-bottom: 5px;">
                ${districtName}
              </div>
              <div style="margin: 6px 0; font-size: 13px; color: #3e2723;">
                <span style="display: inline-block; width: 8px; height: 8px; background: #c62828; border-radius: 50%; margin-right: 8px;"></span>
                火锅店: <strong style="color: #c62828;">${data.hotpotCount}</strong> 家
              </div>
              <div style="margin: 6px 0; font-size: 13px; color: #3e2723;">
                <span style="display: inline-block; width: 8px; height: 8px; background: #8d6e63; border-radius: 50%; margin-right: 8px;"></span>
                茶馆: <strong style="color: #8d6e63;">${data.teahouseCount}</strong> 家
              </div>
              <div style="margin: 6px 0; font-size: 13px; color: #3e2723;">
                <span style="display: inline-block; width: 8px; height: 8px; background: #6d4c41; border-radius: 50%; margin-right: 8px;"></span>
                火锅均价: <strong style="color: #6d4c41;">¥${data.avgPrice}</strong>
              </div>
              <div style="margin: 6px 0; font-size: 12px; color: #8d6e63; border-top: 1px dashed #d7ccc8; padding-top: 6px; margin-top: 8px;">
                面积: ${data.area} km² | 人口: ${data.population}
              </div>
            </div>
          `
        },
        confine: true,
        backgroundColor: 'rgba(255, 253, 246, 0.98)',
        borderColor: '#8d6e63',
        borderWidth: 2,
        textStyle: {
          color: '#3e2723'
        },
        extraCssText: 'box-shadow: 8px 8px 0 #d7ccc8; border-radius: 8px;'
      },
      visualMap: {
        show: true,
        min: 0,
        max: 500,
        text: ['高', '低'],
        realtime: false,
        calculable: true,
        inRange: {
          color: [
            '#fffdf6',  // 极浅 - 几乎没有数据
            '#f5f5dc',  // 米白 - 很少数据
            '#e8dcc8',  // 浅米色
            '#d7ccc8',  // 浅棕
            '#c4b5a8',  // 中浅棕
            '#a1887f',  // 中棕
            '#8d6e63',  // 棕灰
            '#7d5e52',  // 深棕灰
            '#6d4c41',  // 深棕
            '#5d4037'   // 最深棕 - 数据最多
          ]
        },
        textStyle: {
          color: '#5d4037'
        },
        left: 'left',
        top: 'bottom',
        orient: 'horizontal',
        itemWidth: 20,
        itemHeight: 140
      },
      series: [
        {
          name: '重庆区县',
          type: 'map',
          map: 'CQ',
          roam: false,
          zoom: 1.1,
          center: [107.7, 30.0],
          label: {
            show: true,
            color: '#5d4037',
            fontSize: 10,
            fontWeight: 'normal'
          },
          emphasis: {
            label: {
              show: true,
              color: '#3e2723',
              fontSize: 12,
              fontWeight: 'bold'
            },
            itemStyle: {
              areaColor: '#a1887f',
              borderColor: '#5d4037',
              borderWidth: 2,
              shadowBlur: 15,
              shadowColor: 'rgba(141, 110, 99, 0.6)'
            }
          },
          itemStyle: {
            borderColor: '#8d6e63',
            borderWidth: 1.5,
            shadowBlur: 5,
            shadowColor: 'rgba(141, 110, 99, 0.2)'
          },
          select: {
            label: {
              show: true,
              color: '#3e2723'
            },
            itemStyle: {
              areaColor: '#d7ccc8'
            }
          },
          data: generateDistrictData(geoJson)
        }
      ]
    }
    
    chart.setOption(option)
  } catch (error) {
    console.error('Failed to load map data:', error)
    chart.hideLoading()
  }
})

onUnmounted(() => {
  if (chart) {
    chart.dispose()
    chart = null
  }
})

// 处理区县数据
const processDistrictData = (districts, hotpots, teahouses) => {
  // 按district_id统计火锅店
  const hotpotByDistrict = new Map()
  hotpots.forEach(h => {
    const districtId = h.district_id
    if (!hotpotByDistrict.has(districtId)) {
      hotpotByDistrict.set(districtId, { count: 0, totalPrice: 0 })
    }
    const data = hotpotByDistrict.get(districtId)
    data.count++
    if (h.price_avg) {
      data.totalPrice += h.price_avg
    }
  })
  
  // 按district_id统计茶馆
  const teahouseByDistrict = new Map()
  teahouses.forEach(t => {
    const districtId = t.district_id
    if (!teahouseByDistrict.has(districtId)) {
      teahouseByDistrict.set(districtId, 0)
    }
    teahouseByDistrict.set(districtId, teahouseByDistrict.get(districtId) + 1)
  })
  
  // 整合数据
  districts.forEach(d => {
    const hotpotData = hotpotByDistrict.get(d.id) || { count: 0, totalPrice: 0 }
    const teahouseCount = teahouseByDistrict.get(d.id) || 0
    const avgPrice = hotpotData.count > 0 ? Math.round(hotpotData.totalPrice / hotpotData.count) : 0
    
    districtData.set(d.name, {
      hotpotCount: hotpotData.count,
      teahouseCount: teahouseCount,
      avgPrice: avgPrice,
      area: d.area_km2.toFixed(2),
      population: d.population.toLocaleString()
    })
  })
  
  // 调试：打印数据映射情况
  console.log('District data mapping:', {
    totalDistricts: districts.length,
    mappedDistricts: districtData.size,
    districtNames: Array.from(districtData.keys())
  })
}

// 区县名称映射（地图JSON名称 -> 数据库名称）
const districtNameMap = {
  '石柱土家族自治县': '石柱县',
  '秀山土家族苗族自治县': '秀山县',
  '酉阳土家族苗族自治县': '酉阳县',
  '彭水苗族土家族自治县': '彭水县'
}

// 生成区县数据（根据实际数据着色）
const generateDistrictData = (geoJson) => {
  if (!geoJson.features) return []
  
  const result = geoJson.features.map((feature) => {
    let name = feature.properties.name
    
    // 尝试映射名称
    const mappedName = districtNameMap[name] || name
    const data = districtData.get(mappedName)
    
    // 直接使用火锅店数量作为值
    const value = data ? data.hotpotCount : 0
    
    // 调试：记录没有数据的区县
    if (!data || value === 0) {
      console.warn(`No data for district: ${name} (mapped to: ${mappedName})`)
    }
    
    return {
      name: name,  // 保持原始名称用于地图显示
      value: value
    }
  })
  
  console.log('Generated district data:', result.filter(d => d.value > 0).length, '/', result.length)
  return result
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
