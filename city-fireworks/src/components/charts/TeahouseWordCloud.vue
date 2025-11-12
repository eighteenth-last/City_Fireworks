<template>
  <div class="wordcloud-container">
    <div class="wordcloud-title">茶文化标签云</div>
    <div class="words-wrapper" ref="wrapperRef">
      <span 
        v-for="(word, index) in words" 
        :key="index"
        class="word-item"
        :style="getWordStyle(word, index)"
      >
        {{ word.name }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const words = ref([])
const wrapperRef = ref(null)

const loadData = async () => {
  try {
    const tags = await api.teahouse.getCulturalTags()
    // 转换数据格式并按频率排序，取前10个高频词
    words.value = tags
      .map(tag => ({
        name: tag.tag,
        value: tag.count
      }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 10)
  } catch (error) {
    console.error('Error loading teahouse tags:', error)
    // 降级到默认数据
    words.value = [
      { name: '盖碗茶', value: 200 },
      { name: '麻将', value: 180 },
      { name: '川剧', value: 160 },
      { name: '评书', value: 150 },
      { name: '采耳', value: 140 },
      { name: '茶艺', value: 130 },
      { name: '古筝', value: 120 },
      { name: '书法', value: 110 },
      { name: '品茗', value: 100 },
      { name: '清茶', value: 90 }
    ]
  }
}

onMounted(() => {
  loadData()
})

const colors = [
  '#d32f2f', '#c2185b', '#7b1fa2', '#512da8', 
  '#303f9f', '#1976d2', '#0097a7', '#00796b',
  '#388e3c', '#689f38', '#afb42b', '#f57c00',
  '#e64a19', '#5d4037', '#8d6e63', '#a1887f'
]

const getWordStyle = (word, index) => {
  // 根据词频计算字体大小
  const maxValue = Math.max(...words.value.map(w => w.value))
  const minValue = Math.min(...words.value.map(w => w.value))
  const ratio = (word.value - minValue) / (maxValue - minValue || 1)
  const fontSize = Math.floor(ratio * 32) + 24 // 24-56px
  
  // 使用固定的随机种子
  const seed = word.name.charCodeAt(0) + word.value
  const random = (seed * 9301 + 49297) % 233280 / 233280
  
  // 螺旋分布算法
  const totalWords = words.value.length
  const angle = (index / totalWords) * Math.PI * 6 + random * Math.PI * 0.5
  const radius = 60 + index * 15 + random * 20
  
  // 计算位置（相对于中心）
  const x = Math.cos(angle) * radius
  const y = Math.sin(angle) * radius
  
  // 旋转角度
  const rotation = (random - 0.5) * 60 // -30 到 30 度
  
  // 颜色选择
  const colorIndex = Math.floor(random * colors.length)
  const color = colors[colorIndex]
  
  // 字体粗细
  const fontWeight = ratio > 0.7 ? 'bold' : (ratio > 0.4 ? '600' : 'normal')
  
  return {
    fontSize: `${fontSize}px`,
    color: color,
    fontWeight: fontWeight,
    left: '50%',
    top: '50%',
    transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px)) rotate(${rotation}deg)`,
    opacity: 0.9
  }
}

const resize = () => {
  // 占位方法，保持接口一致
}

defineExpose({ resize })
</script>

<style scoped>
.wordcloud-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 10px;
}

.wordcloud-title {
  text-align: center;
  font-size: 16px;
  font-weight: bold;
  color: #5d4037;
  margin-bottom: 20px;
}

.words-wrapper {
  flex: 1;
  position: relative;
  background: linear-gradient(135deg, rgba(255, 253, 246, 0.2) 0%, rgba(255, 248, 225, 0.2) 100%);
  border-radius: 8px;
  min-height: 300px;
}

.word-item {
  font-family: 'STKaiti', 'KaiTi', 'STFangsong', 'FangSong', 'Microsoft YaHei', serif;
  cursor: pointer;
  transition: opacity 0.2s ease;
  display: inline-block;
  padding: 5px;
  user-select: none;
  white-space: nowrap;
  position: absolute;
  animation: fadeIn 0.6s ease-out backwards;
}

.word-item:nth-child(1) { animation-delay: 0.05s; }
.word-item:nth-child(2) { animation-delay: 0.1s; }
.word-item:nth-child(3) { animation-delay: 0.15s; }
.word-item:nth-child(4) { animation-delay: 0.2s; }
.word-item:nth-child(5) { animation-delay: 0.25s; }
.word-item:nth-child(6) { animation-delay: 0.3s; }
.word-item:nth-child(7) { animation-delay: 0.35s; }
.word-item:nth-child(8) { animation-delay: 0.4s; }
.word-item:nth-child(9) { animation-delay: 0.45s; }
.word-item:nth-child(10) { animation-delay: 0.5s; }

.word-item:hover {
  opacity: 1;
  text-shadow: 2px 2px 8px rgba(141, 110, 99, 0.5);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
</style>
