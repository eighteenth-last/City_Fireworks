/**
 * API 请求 Composable
 * 统一处理 API 请求的加载状态和错误处理
 */
import { ref } from 'vue'

export function useApi(apiFn) {
  const data = ref(null)
  const loading = ref(false)
  const error = ref(null)

  /**
   * 执行 API 请求
   */
  const execute = async (...args) => {
    loading.value = true
    error.value = null
    
    try {
      const result = await apiFn(...args)
      data.value = result
      return result
    } catch (err) {
      error.value = err
      console.error('API Error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 重置状态
   */
  const reset = () => {
    data.value = null
    loading.value = false
    error.value = null
  }

  return {
    data,
    loading,
    error,
    execute,
    reset
  }
}
