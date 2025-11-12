<template>
  <Modal
    :visible="visible"
    :title="`城市温度指数 - ${data?.score || 0}分`"
    width="1000px"
    height="700px"
    @update:visible="$emit('update:visible', $event)"
  >
    <div class="modal-body">
      <!-- 温度指数大屏 -->
      <div class="temp-display">
        <div class="temp-circle" :style="{ borderColor: getTempColor(data?.score || 0) }">
          <div class="temp-value" :style="{ color: getTempColor(data?.score || 0) }">
            {{ data?.score || 0 }}
          </div>
          <div class="temp-label">城市温度</div>
        </div>
        <div class="temp-desc">
          <div class="temp-status" :style="{ color: getTempColor(data?.score || 0) }">
            {{ getTempStatus(data?.score || 0) }}
          </div>
          <div class="temp-date">更新时间: {{ data?.date }}</div>
        </div>
      </div>

      <!-- 因素分解 -->
      <div class="factors-section">
        <h4>温度构成因素</h4>
        <div class="factors-grid">
          <div
            v-for="(value, key) in data?.factors || {}"
            :key="key"
            class="factor-card"
            :style="{ borderLeftColor: getFactorColor(key) }"
          >
            <div class="factor-name">{{ getFactorName(key) }}</div>
            <div class="factor-value">{{ value }}分</div>
            <div class="factor-bar">
              <div
                class="factor-bar-fill"
                :style="{ width: `${value}%`, background: getFactorColor(key) }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 详细说明 -->
      <div class="analysis-section">
        <h4>数据分析</h4>
        <div class="analysis-text">
          <p>当前城市温度指数为 <strong>{{ data?.score || 0 }}分</strong>，属于{{ getTempStatus(data?.score || 0) }}状态。</p>
          <p v-if="data?.score >= 80">
            城市烟火气息浓郁，火锅文化活跃，夜经济发展良好，市民生活满意度高。
          </p>
          <p v-else-if="data?.score >= 60">
            城市发展稳健，各项指标均衡，但仍有提升空间。
          </p>
          <p v-else>
            城市活力有待提升，建议加强文化建设、促进夜间经济发展。
          </p>
        </div>
      </div>
    </div>
  </Modal>
</template>

<script setup>
import Modal from './Modal.vue'

defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  data: {
    type: Object,
    default: null
  }
})

defineEmits(['update:visible'])

const getTempColor = (score) => {
  if (score >= 80) return '#ff4d4d'
  if (score >= 60) return '#ff9d4d'
  if (score >= 40) return '#ffd700'
  return '#00d4ff'
}

const getTempStatus = (score) => {
  if (score >= 80) return '热情似火'
  if (score >= 60) return '温暖如春'
  if (score >= 40) return '平和适中'
  return '清新凉爽'
}

const getFactorColor = (key) => {
  const colors = {
    hotpot_density: '#ff4d4d',
    night_economy: '#b967ff',
    teahouse_culture: '#d4a574',
    vitality: '#00d4ff'
  }
  return colors[key] || '#999999'
}

const getFactorName = (key) => {
  const names = {
    hotpot_density: '火锅密度',
    night_economy: '夜间经济',
    teahouse_culture: '茶馆文化',
    vitality: '城市活力'
  }
  return names[key] || key
}
</script>

<style scoped>
.modal-body {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.temp-display {
  display: flex;
  align-items: center;
  gap: 40px;
  padding: 20px;
  background: rgba(255, 77, 77, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 77, 77, 0.3);
}

.temp-circle {
  width: 150px;
  height: 150px;
  border: 4px solid;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(255, 77, 77, 0.7);
  }
  50% {
    box-shadow: 0 0 0 20px rgba(255, 77, 77, 0);
  }
}

.temp-value {
  font-size: 48px;
  font-weight: bold;
}

.temp-label {
  font-size: 14px;
  color: #999;
  margin-top: 5px;
}

.temp-desc {
  flex: 1;
}

.temp-status {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 10px;
}

.temp-date {
  font-size: 14px;
  color: #999;
}

.factors-section h4,
.analysis-section h4 {
  margin: 0 0 15px 0;
  color: #ff4d4d;
  font-size: 18px;
  border-left: 3px solid #ff4d4d;
  padding-left: 10px;
}

.factors-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.factor-card {
  background: rgba(255, 77, 77, 0.05);
  border: 1px solid rgba(255, 77, 77, 0.2);
  border-left: 4px solid;
  border-radius: 8px;
  padding: 20px;
  transition: all 0.3s ease;
}

.factor-card:hover {
  transform: translateX(5px);
  box-shadow: 0 5px 15px rgba(255, 77, 77, 0.2);
}

.factor-name {
  font-size: 16px;
  color: #fff;
  margin-bottom: 10px;
}

.factor-value {
  font-size: 28px;
  font-weight: bold;
  color: #ff4d4d;
  margin-bottom: 10px;
}

.factor-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.factor-bar-fill {
  height: 100%;
  transition: width 1s ease;
}

.analysis-text {
  background: rgba(255, 77, 77, 0.05);
  border: 1px solid rgba(255, 77, 77, 0.2);
  border-radius: 8px;
  padding: 20px;
  line-height: 1.8;
}

.analysis-text p {
  margin: 0 0 10px 0;
  color: #ccc;
}

.analysis-text strong {
  color: #ff4d4d;
}
</style>
