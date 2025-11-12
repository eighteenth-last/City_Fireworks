<template>
  <div class="ranking-detail-view">
    <div class="chart-full">
      <ParallelAnalysis ref="parallelRef" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import ParallelAnalysis from './charts/ParallelAnalysis.vue'

const parallelRef = ref(null)

const handleResize = () => {
  parallelRef.value?.resize()
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.ranking-detail-view {
  width: 100%;
  height: 100%;
  background: transparent;
  overflow-y: auto;
}

.chart-full {
  background: rgba(255, 253, 246, 0.8);
  border: 2px solid #8d6e63;
  border-radius: 12px;
  padding: 12px;
  box-shadow: 6px 6px 0 #d7ccc8;
  transition: all 0.3s ease;
  height: 400px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chart-full:hover {
  transform: translateY(-4px);
  box-shadow: 8px 8px 0 #d7ccc8;
}

/* 滚动条样式 */
.ranking-detail-view::-webkit-scrollbar {
  width: 10px;
}

.ranking-detail-view::-webkit-scrollbar-track {
  background: rgba(248, 244, 233, 0.5);
  border-radius: 5px;
}

.ranking-detail-view::-webkit-scrollbar-thumb {
  background: rgba(141, 110, 99, 0.5);
  border-radius: 5px;
}

.ranking-detail-view::-webkit-scrollbar-thumb:hover {
  background: rgba(141, 110, 99, 0.7);
}
</style>
