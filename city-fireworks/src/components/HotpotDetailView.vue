<template>
  <div class="hotpot-detail-view">
    <div class="charts-grid">
      <!-- 区域商户数量TOP10 -->
      <div class="chart-card">
        <DistrictMerchantTop10 ref="districtMerchantRef" />
      </div>

      <!-- 营业时长分布 -->
      <div class="chart-card">
        <TimeSlotDistribution ref="timeSlotRef" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import DistrictMerchantTop10 from './charts/DistrictMerchantTop10.vue'
import TimeSlotDistribution from './charts/TimeSlotDistribution.vue'
import ShopTypeRatingBox from './charts/ShopTypeRatingBox.vue'

const districtMerchantRef = ref(null)
const timeSlotRef = ref(null)
const ratingBoxRef = ref(null)

// 响应式处理
const handleResize = () => {
  districtMerchantRef.value?.resize()
  timeSlotRef.value?.resize()
  ratingBoxRef.value?.resize()
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.hotpot-detail-view {
  width: 100%;
  height: 100%;
  background: transparent;
  overflow-y: auto;
}

.detail-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px dashed #8d6e63;
}

.detail-header h1 {
  margin: 0 0 10px 0;
  font-size: 28px;
  color: #5d4037;
  font-weight: bold;
}

.subtitle {
  margin: 8px 0;
  font-size: 16px;
  color: #8d6e63;
  line-height: 1.6;
}

.subtitle-note {
  margin: 8px 0;
  font-size: 14px;
  color: #a1887f;
  font-style: italic;
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

.chart-card.full-width {
  grid-column: 1 / -1;
  min-height: 400px;
  height: 400px;
}

.chart-title {
  font-size: 16px;
  font-weight: bold;
  color: #5d4037;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(141, 110, 99, 0.3);
}

/* 滚动条样式 */
.hotpot-detail-view::-webkit-scrollbar {
  width: 10px;
}

.hotpot-detail-view::-webkit-scrollbar-track {
  background: rgba(248, 244, 233, 0.5);
  border-radius: 5px;
}

.hotpot-detail-view::-webkit-scrollbar-thumb {
  background: rgba(141, 110, 99, 0.5);
  border-radius: 5px;
}

.hotpot-detail-view::-webkit-scrollbar-thumb:hover {
  background: rgba(141, 110, 99, 0.7);
}

/* 响应式布局 */
@media (max-width: 1200px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-card.full-width {
    grid-column: 1;
  }
}

@media (max-width: 768px) {
  .hotpot-detail-view {
    padding: 30px;
  }
  
  .detail-header h1 {
    font-size: 22px;
  }
  
  .subtitle {
    font-size: 14px;
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
