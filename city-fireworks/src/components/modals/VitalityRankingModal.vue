<template>
  <Modal
    :visible="visible"
    title="区县活力排名详情"
    width="1000px"
    height="700px"
    @update:visible="$emit('update:visible', $event)"
  >
    <div class="modal-body">
      <!-- 排名列表 -->
      <div class="ranking-list">
        <div
          v-for="(item, index) in data"
          :key="item.name"
          class="ranking-item"
          :class="{ top3: index < 3 }"
        >
          <div class="rank-number" :class="'rank-' + (index + 1)">
            {{ index + 1 }}
          </div>
          <div class="rank-info">
            <div class="rank-name">{{ item.name }}</div>
            <div class="rank-score">活力指数: {{ item.score }}分</div>
          </div>
          <div class="rank-bar">
            <div
              class="rank-bar-fill"
              :style="{ width: `${item.score}%` }"
            ></div>
          </div>
        </div>
      </div>

      <!-- 统计信息 -->
      <div class="stats-section">
        <h4>活力分布统计</h4>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-label">最高活力</div>
            <div class="stat-value">{{ maxScore }}分</div>
            <div class="stat-area">{{ topArea }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">平均活力</div>
            <div class="stat-value">{{ avgScore }}分</div>
            <div class="stat-desc">全区县平均值</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">优秀区县</div>
            <div class="stat-value">{{ excellentCount }}个</div>
            <div class="stat-desc">≥80分</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">良好区县</div>
            <div class="stat-value">{{ goodCount }}个</div>
            <div class="stat-desc">60-80分</div>
          </div>
        </div>
      </div>
    </div>
  </Modal>
</template>

<script setup>
import { computed } from 'vue'
import Modal from './Modal.vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  data: {
    type: Array,
    default: () => []
  }
})

defineEmits(['update:visible'])

const maxScore = computed(() => {
  return props.data.length > 0 ? Math.max(...props.data.map(d => d.score)) : 0
})

const topArea = computed(() => {
  return props.data.length > 0 ? props.data[0].name : '-'
})

const avgScore = computed(() => {
  if (props.data.length === 0) return 0
  const sum = props.data.reduce((acc, d) => acc + d.score, 0)
  return (sum / props.data.length).toFixed(1)
})

const excellentCount = computed(() => {
  return props.data.filter(d => d.score >= 80).length
})

const goodCount = computed(() => {
  return props.data.filter(d => d.score >= 60 && d.score < 80).length
})
</script>

<style scoped>
.modal-body {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.ranking-list {
  max-height: 300px;
  overflow-y: auto;
  padding-right: 10px;
}

.ranking-list::-webkit-scrollbar {
  width: 8px;
}

.ranking-list::-webkit-scrollbar-track {
  background: rgba(255, 77, 77, 0.1);
  border-radius: 4px;
}

.ranking-list::-webkit-scrollbar-thumb {
  background: #ff4d4d;
  border-radius: 4px;
}

.ranking-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: rgba(255, 77, 77, 0.05);
  border: 1px solid rgba(255, 77, 77, 0.2);
  border-radius: 8px;
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

.ranking-item:hover {
  background: rgba(255, 77, 77, 0.1);
  transform: translateX(5px);
}

.ranking-item.top3 {
  background: rgba(255, 77, 77, 0.1);
  border: 2px solid #ff4d4d;
}

.rank-number {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  background: rgba(255, 77, 77, 0.2);
  color: #ff4d4d;
}

.rank-number.rank-1 {
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  color: #000;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
}

.rank-number.rank-2 {
  background: linear-gradient(135deg, #c0c0c0, #e8e8e8);
  color: #000;
  box-shadow: 0 0 20px rgba(192, 192, 192, 0.5);
}

.rank-number.rank-3 {
  background: linear-gradient(135deg, #cd7f32, #e8a660);
  color: #000;
  box-shadow: 0 0 20px rgba(205, 127, 50, 0.5);
}

.rank-info {
  flex: 1;
}

.rank-name {
  font-size: 18px;
  font-weight: bold;
  color: #fff;
  margin-bottom: 5px;
}

.rank-score {
  font-size: 14px;
  color: #ff4d4d;
}

.rank-bar {
  width: 200px;
  height: 10px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
  overflow: hidden;
}

.rank-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff4d4d, #ff8c8c);
  border-radius: 5px;
  transition: width 1s ease;
}

.stats-section h4 {
  margin: 0 0 15px 0;
  color: #ff4d4d;
  font-size: 18px;
  border-left: 3px solid #ff4d4d;
  padding-left: 10px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.stat-card {
  background: rgba(255, 77, 77, 0.05);
  border: 1px solid rgba(255, 77, 77, 0.2);
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(255, 77, 77, 0.2);
}

.stat-label {
  font-size: 14px;
  color: #999;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #ff4d4d;
  margin-bottom: 5px;
}

.stat-area,
.stat-desc {
  font-size: 14px;
  color: #ccc;
}
</style>
