<template>
  <div v-if="visible" class="modal-wrapper" @click="handleClose">
    <!-- 背景遮罩 -->
    <div class="modal-overlay"></div>

    <!-- 弹窗主体 -->
    <div class="modal-container" :style="modalStyle" @click.stop>
      <!-- 标题栏 -->
      <div class="modal-header">
        <h3>{{ title }}</h3>
        <div class="header-meta">
          <span class="update-time">{{ updateTime }}</span>
          <button class="close-btn" @click="handleClose">
            <span>×</span>
          </button>
        </div>
      </div>

      <!-- 内容区 -->
      <div class="modal-content">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  width: {
    type: String,
    default: '1200px'
  },
  height: {
    type: String,
    default: '800px'
  }
})

const emit = defineEmits(['close', 'update:visible'])

const updateTime = ref(new Date().toLocaleString('zh-CN'))

const modalStyle = computed(() => {
  return {
    width: props.width,
    height: props.height
  }
})

const handleClose = () => {
  emit('update:visible', false)
  emit('close')
}

// 键盘事件
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && props.visible) {
    handleClose()
  }
})
</script>

<style scoped>
.modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
}

.modal-container {
  position: relative;
  background: rgba(10, 15, 28, 0.98);
  border: 2px solid #ff4d4d;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(255, 77, 77, 0.3);
  display: flex;
  flex-direction: column;
  animation: modalAppear 0.3s ease-out;
  max-width: 90vw;
  max-height: 90vh;
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  background: linear-gradient(135deg, #0a0f1c 0%, #1a2530 100%);
  padding: 20px 30px;
  border-radius: 12px 12px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 77, 77, 0.3);
}

.modal-header h3 {
  margin: 0;
  font-size: 24px;
  color: #ff4d4d;
  font-weight: bold;
}

.header-meta {
  display: flex;
  align-items: center;
  gap: 20px;
}

.update-time {
  font-size: 14px;
  color: #999;
}

.close-btn {
  width: 36px;
  height: 36px;
  background: rgba(255, 77, 77, 0.1);
  border: 1px solid #ff4d4d;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  color: #ff4d4d;
  font-size: 24px;
  line-height: 1;
}

.close-btn:hover {
  background: #ff4d4d;
  color: white;
  transform: rotate(90deg);
}

.modal-content {
  padding: 30px;
  overflow-y: auto;
  flex: 1;
  color: #fff;
}
</style>
