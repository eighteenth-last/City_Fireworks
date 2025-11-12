<template>
  <div class="teahouse-detail-view">
    <div class="charts-grid">
      <!-- 词云图 -->
      <div class="chart-card">
        <TeahouseWordCloud ref="wordCloudRef" />
      </div>

      <!-- 地理分布图 -->
      <div class="chart-card">
        <TeahouseDistribution ref="distributionRef" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import TeahouseWordCloud from './charts/TeahouseWordCloud.vue'
import TeahouseDistribution from './charts/TeahouseDistribution.vue'

const wordCloudRef = ref(null)
const distributionRef = ref(null)

const handleResize = () => {
  wordCloudRef.value?.resize()
  distributionRef.value?.resize()
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.teahouse-detail-view {
  width: 100%;
  height: 100%;
  background: transparent;
  overflow-y: auto;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  max-width: 1400px;
  margin: 0 auto;
  padding-bottom: 0;
}

.chart-card {
  background: rgba(255, 253, 246, 0.8);
  border: 2px solid #8d6e63;
  border-radius: 12px;
  padding: 12px;
  box-shadow: 6px 6px 0 #d7ccc8;
  transition: all 0.3s ease;
  min-height: 400px;
  height: 400px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chart-card:hover {
  transform: translateY(-4px);
  box-shadow: 8px 8px 0 #d7ccc8;
}

/* 滚动条样式 */
.teahouse-detail-view::-webkit-scrollbar {
  width: 10px;
}

.teahouse-detail-view::-webkit-scrollbar-track {
  background: rgba(248, 244, 233, 0.5);
  border-radius: 5px;
}

.teahouse-detail-view::-webkit-scrollbar-thumb {
  background: rgba(141, 110, 99, 0.5);
  border-radius: 5px;
}

.teahouse-detail-view::-webkit-scrollbar-thumb:hover {
  background: rgba(141, 110, 99, 0.7);
}

/* 响应式布局 */
@media (max-width: 1200px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .teahouse-detail-view {
    padding: 15px;
  }
  
  .charts-grid {
    gap: 16px;
  }
  
  .chart-card {
    padding: 15px;
    min-height: 350px;
  }
}
</style>
