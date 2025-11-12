<template>
  <div class="app-container">
    <!-- 顶部标题栏 -->
    <header class="app-header">
      <h1>重庆城市人文市井烟火大屏</h1>
      <div class="header-actions">
<!--        <div class="action-buttons">-->
<!--          <button class="action-btn export-btn" @click="handleExport" title="导出数据">-->
<!--            <span class="btn-icon">📤</span>-->
<!--            <span class="btn-text">导出</span>-->
<!--          </button>-->
<!--          <button class="action-btn import-btn" @click="handleImport" title="导入数据">-->
<!--            <span class="btn-icon">📥</span>-->
<!--            <span class="btn-text">导入</span>-->
<!--          </button>-->
<!--        </div>-->
        <div class="header-stats">
          <div class="stat-item">
            <span class="stat-value">{{ currentTime }}</span>
          </div>
        </div>
      </div>
    </header>

    <!-- 主体内容区域 -->
    <div class="app-body">
      <!-- 左屏 -->
      <aside class="left-panel">
        <section class="panel-section">
          <div class="section-header">
            <h2>火锅江湖</h2>
            <button class="detail-btn" @click="showHotpotDetail">详情</button>
          </div>
          <div class="chart-single">
            <ShopTypePie ref="shopTypePieRef" />
          </div>
        </section>
        <section class="panel-section">
          <div class="section-header">
            <h2>茶馆岁月</h2>
            <button class="detail-btn" @click="showTeahouseDetail">详情</button>
          </div>
          <div class="chart-single">
            <TeahouseTimeline ref="teahouseTimelineRef" />
          </div>
        </section>
      </aside>

      <!-- 中心地图 -->
      <main class="map-section">
        <ChongqingMap ref="mapRef" />
      </main>

      <!-- 右屏 -->
      <aside class="right-panel">
        <section class="panel-section">
          <div class="section-header">
            <h2>24小时城市运行趋势</h2>
            <button class="detail-btn" @click="showCityTrendDetail">详情</button>
          </div>
          <div class="chart-single">
            <CityOperationTrend ref="cityOperationTrendRef" />
          </div>
        </section>
        <section class="panel-section">
          <div class="section-header">
            <h2>火锅密度排行</h2>
            <button class="detail-btn" @click="showRankingDetail">详情</button>
          </div>
          <div class="chart-single">
            <HotpotRanking ref="hotpotRankingRef" />
          </div>
        </section>
      </aside>
    </div>

    <!-- 详情弹窗 -->
    <DetailModal v-model:visible="hotpotDetailVisible" title="火锅江湖 - 详细信息">
      <HotpotDetailView />
    </DetailModal>

    <DetailModal v-model:visible="teahouseDetailVisible" title="茶馆岁月 - 详细信息">
      <TeahouseDetailView />
    </DetailModal>

    <DetailModal v-model:visible="cityTrendDetailVisible" title="24小时城市运行趋势 - 详细信息">
      <div class="detail-content">
        
        <div class="detail-charts">
          <div class="chart-item">
            <h3>🚇 地铁客流情况</h3>
            <MetroPassengers ref="metroPassengersRef" />
          </div>
          <div class="chart-item">
            <h3>🌡️ 城市温度指数</h3>
            <TemperatureIndex ref="temperatureIndexRef" />
          </div>
          <div class="chart-item">
            <h3>🏆 区县活力排行</h3>
            <VitalityRanking ref="vitalityRankingRef" />
          </div>
        </div>
      </div>
    </DetailModal>

    <DetailModal v-model:visible="rankingDetailVisible" title="火锅密度排行 - 详细信息">
      <RankingDetailView />
    </DetailModal>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import ChongqingMap from './components/charts/ChongqingMap.vue'
import ShopTypePie from './components/charts/ShopTypePie.vue'
import CityOperationTrend from './components/charts/CityOperationTrend.vue'
import HotpotRanking from './components/charts/HotpotRanking.vue'
import TeahouseTimeline from './components/charts/TeahouseTimeline.vue'
import DetailModal from './components/DetailModal.vue'
import MetroPassengers from './components/charts/MetroPassengers.vue'
import TemperatureIndex from './components/charts/TemperatureIndex.vue'
import VitalityRanking from './components/charts/VitalityRanking.vue'
import HotpotDetailView from './components/HotpotDetailView.vue'
import TeahouseDetailView from './components/TeahouseDetailView.vue'
import RankingDetailView from './components/RankingDetailView.vue'

const mapRef = ref(null)
const chongqingMapRef = ref(null)
const cityOperationTrendRef = ref(null)
const hotpotRankingRef = ref(null)
const teahouseTimelineRef = ref(null)
const metroPassengersRef = ref(null)
const temperatureIndexRef = ref(null)
const vitalityRankingRef = ref(null)

const currentTime = ref('')

// 详情弹窗状态
const hotpotDetailVisible = ref(false)
const teahouseDetailVisible = ref(false)
const cityTrendDetailVisible = ref(false)
const rankingDetailVisible = ref(false)

let timeInterval = null

onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)

  // 窗口大小改变时，响应式调整图表
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
  window.removeEventListener('resize', handleResize)
})

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN')
}

// 显示详情弹窗
const showHotpotDetail = () => {
  hotpotDetailVisible.value = true
}

const showTeahouseDetail = () => {
  teahouseDetailVisible.value = true
}

const showCityTrendDetail = () => {
  cityTrendDetailVisible.value = true
}

const showRankingDetail = () => {
  rankingDetailVisible.value = true
}

const handleResize = () => {
  // 响应式调整图表大小
  nextTick(() => {
    mapRef.value?.resize()
    shopTypePieRef.value?.resize()
    cityOperationTrendRef.value?.resize()
    hotpotRankingRef.value?.resize()
    teahouseTimelineRef.value?.resize()
  })
}

// 导出数据
const handleExport = async () => {
  try {
    const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'
    const exportURL = `${baseURL}/export/all`
    
    // 创建一个隐藏的 a 标签来触发下载
    const link = document.createElement('a')
    link.href = exportURL
    link.download = `city_fireworks_data_${new Date().getTime()}.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    console.log('数据导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    alert('导出失败，请稍后重试')
  }
}

// 导入数据
const handleImport = () => {
  // 创建文件输入元素
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.csv,.json'
  
  input.onchange = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'
      const response = await fetch(`${baseURL}/import/data`, {
        method: 'POST',
        body: formData
      })
      
      if (response.ok) {
        alert('数据导入成功！')
        // 刷新页面数据
        window.location.reload()
      } else {
        const error = await response.json()
        alert(`导入失败: ${error.message || '未知错误'}`)
      }
    } catch (error) {
      console.error('导入失败:', error)
      alert('导入失败，请检查文件格式')
    }
  }
  
  input.click()
}

</script>

<style scoped>
.app-container {
  width: 100%;
  height: 100vh;
  background: #f8f4e9;
  color: #3e2723;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-sizing: border-box;
}

.app-header {
  height: 70px;
  background: linear-gradient(135deg, #fffdf6 0%, #f8f4e9 100%);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  border-bottom: 3px solid #8d6e63;
  box-shadow: 0 2px 10px rgba(141, 110, 99, 0.2);
  position: relative;
  z-index: 100;
  flex-shrink: 0;
}

.app-header h1 {
  margin: 0;
  font-size: 26px;
  font-weight: 600;
  letter-spacing: 2px;
  color: #5d4037;
  text-shadow: 2px 2px 4px rgba(93, 64, 55, 0.1);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  padding: 8px 16px;
  background: rgba(141, 110, 99, 0.08);
  border: 2px solid #d32f2f;
  border-radius: 6px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: linear-gradient(135deg, #fff 0%, #fffdf6 100%);
  border: 2px solid #8d6e63;
  border-radius: 4px;
  color: #5d4037;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(141, 110, 99, 0.2);
}

.action-btn:hover {
  background: linear-gradient(135deg, #8d6e63 0%, #a1887f 100%);
  color: #fff;
  border-color: #6d4c41;
  box-shadow: 0 4px 8px rgba(141, 110, 99, 0.4);
  transform: translateY(-2px);
}

.action-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(141, 110, 99, 0.2);
}

.btn-icon {
  font-size: 16px;
}

.btn-text {
  font-size: 13px;
  letter-spacing: 0.5px;
}

.header-stats {
  display: flex;
  gap: 30px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.stat-label {
  font-size: 12px;
  color: #8d6e63;
}

.stat-value {
  font-size: 16px;
  color: #8d6e63;
  font-weight: bold;
}

.app-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.left-panel,
.right-panel {
  width: 420px;
  background: #fffdf6;
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  border-left: 2px solid #d7ccc8;
  border-right: 2px solid #d7ccc8;
  overflow-y: auto;
  overflow-x: hidden;
  flex-shrink: 0;
}

.right-panel {
  border-left: 2px solid #d7ccc8;
  border-right: none;
}

.left-panel::-webkit-scrollbar,
.right-panel::-webkit-scrollbar {
  width: 6px;
}

.left-panel::-webkit-scrollbar-track,
.right-panel::-webkit-scrollbar-track {
  background: rgba(215, 204, 200, 0.3);
}

.left-panel::-webkit-scrollbar-thumb,
.right-panel::-webkit-scrollbar-thumb {
  background: rgba(141, 110, 99, 0.5);
  border-radius: 3px;
}

.left-panel::-webkit-scrollbar-thumb:hover,
.right-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(141, 110, 99, 0.7);
}

.panel-section {
  flex: 1;
  padding: 15px;
  border: 2px solid #8d6e63;
  background: #fffdf6;
  margin: 8px;
  border-radius: 8px;
  box-shadow: 6px 6px 0 #d7ccc8;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.panel-section:hover {
  background: #fffdf6;
  box-shadow: 8px 8px 0 #d7ccc8;
  transform: translateY(-2px);
}

.panel-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #8d6e63, #d7ccc8, #8d6e63);
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.panel-section h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #5d4037;
  border-left: 4px solid #8d6e63;
  padding-left: 12px;
  letter-spacing: 1px;
  position: relative;
  flex: 1;
}


.chart-single {
  flex: 1;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.right-charts {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow: hidden;
}

.insight-charts {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  overflow: hidden;
}

.chart-placeholder {
  background: rgba(141, 110, 99, 0.05);
  border: 2px dashed rgba(141, 110, 99, 0.3);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8d6e63;
  font-size: 14px;
  transition: all 0.3s ease;
}

.chart-placeholder:hover {
  background: rgba(141, 110, 99, 0.1);
  border-color: rgba(141, 110, 99, 0.5);
}

.map-section {
  flex: 1;
  position: relative;
  background: #fffdf6;
}

.detail-btn {
  padding: 6px 16px;
  background: linear-gradient(135deg, #8d6e63 0%, #a1887f 100%);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(141, 110, 99, 0.3);
  font-weight: 500;
}

.detail-btn:hover {
  background: linear-gradient(135deg, #6d4c41 0%, #8d6e63 100%);
  box-shadow: 0 4px 12px rgba(141, 110, 99, 0.5);
  transform: translateY(-1px);
}

.detail-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(141, 110, 99, 0.3);
}

.detail-content {
  font-size: 14px;
  line-height: 1.8;
  color: #3e2723;
}

.detail-content p {
  margin: 12px 0;
}

.detail-intro {
  margin-bottom: 24px;
  padding: 16px;
  background: rgba(141, 110, 99, 0.05);
  border-left: 4px solid #8d6e63;
  border-radius: 4px;
}

.detail-intro p {
  margin: 0;
  color: #5d4037;
  line-height: 1.6;
}

.detail-charts {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.chart-item {
  background: rgba(255, 253, 246, 0.5);
  border: 2px solid #d7ccc8;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 4px 4px 0 rgba(215, 204, 200, 0.3);
  transition: all 0.3s ease;
  width: 375px;
}

.chart-item:hover {
  box-shadow: 6px 6px 0 rgba(215, 204, 200, 0.5);
  transform: translateY(-2px);
}

.chart-item h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  color: #5d4037;
  border-bottom: 2px dashed #d7ccc8;
  padding-bottom: 8px;
  font-weight: 600;
}
</style>
