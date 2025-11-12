/**
 * 懒加载工具函数
 */

import * as echarts from 'echarts'

/**
 * 懒加载图表
 */
export const lazyLoadChart = (
  chartDom: HTMLElement,
  option: any,
  delay: number = 100
): Promise<echarts.ECharts> => {
  return new Promise((resolve, reject) => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // 延迟加载，避免频繁触发
            setTimeout(() => {
              try {
                const chart = echarts.init(chartDom)
                chart.setOption(option)
                observer.unobserve(chartDom)
                resolve(chart)
              } catch (error) {
                reject(error)
              }
            }, delay)
          }
        })
      },
      {
        threshold: 0.1, // 进入10%时触发
        rootMargin: '50px' // 提前50px加载
      }
    )

    observer.observe(chartDom)
  })
}

/**
 * 批量懒加载图表
 */
export const lazyLoadCharts = (
  chartElements: { dom: HTMLElement; option: any; delay?: number }[],
  onProgress?: (loaded: number, total: number) => void
): Promise<echarts.ECharts[]> => {
  const promises = chartElements.map((item, index) =>
    lazyLoadChart(item.dom, item.option, item.delay || index * 50)
  )

  let loadedCount = 0
  const updatedPromises = promises.map((promise) =>
    promise.then((chart) => {
      loadedCount++
      onProgress?.(loadedCount, promises.length)
      return chart
    })
  )

  return Promise.all(updatedPromises)
}

/**
 * 懒加载图片
 */
export const lazyLoadImage = (
  imgElement: HTMLImageElement,
  src: string,
  placeholder?: string
): Promise<void> => {
  return new Promise((resolve, reject) => {
    // 设置占位图
    if (placeholder) {
      imgElement.src = placeholder
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const image = new Image()
            image.onload = () => {
              imgElement.src = src
              observer.unobserve(imgElement)
              resolve()
            }
            image.onerror = reject
            image.src = src
          }
        })
      },
      {
        threshold: 0.1,
        rootMargin: '100px'
      }
    )

    observer.observe(imgElement)
  })
}

/**
 * 虚拟滚动
 */
export class VirtualList {
  private container: HTMLElement
  private itemHeight: number
  private visibleCount: number
  private data: any[]
  private startIndex: number = 0
  private endIndex: number = 0
  private renderItem: (item: any, index: number) => HTMLElement
  private buffer: number = 5

  constructor(
    container: HTMLElement,
    itemHeight: number,
    data: any[],
    renderItem: (item: any, index: number) => HTMLElement
  ) {
    this.container = container
    this.itemHeight = itemHeight
    this.data = data
    this.renderItem = renderItem

    this.init()
  }

  private init() {
    this.container.addEventListener('scroll', this.onScroll.bind(this))
    this.updateVisibleItems()
  }

  private onScroll() {
    this.updateVisibleItems()
  }

  private updateVisibleItems() {
    const scrollTop = this.container.scrollTop
    const containerHeight = this.container.clientHeight

    // 计算可见区域
    this.startIndex = Math.floor(scrollTop / this.itemHeight)
    this.endIndex = Math.min(
      this.startIndex + Math.ceil(containerHeight / this.itemHeight) + this.buffer,
      this.data.length
    )

    // 清空容器
    this.container.innerHTML = ''

    // 渲染可见项
    for (let i = this.startIndex; i < this.endIndex; i++) {
      const item = this.renderItem(this.data[i], i)
      item.style.position = 'absolute'
      item.style.top = `${i * this.itemHeight}px`
      this.container.appendChild(item)
    }

    // 设置容器高度
    this.container.style.height = `${this.data.length * this.itemHeight}px`
  }

  updateData(data: any[]) {
    this.data = data
    this.updateVisibleItems()
  }

  destroy() {
    this.container.removeEventListener('scroll', this.onScroll.bind(this))
  }
}

/**
 * 监听元素进入视口
 */
export const observeElement = (
  element: HTMLElement,
  callback: () => void,
  options: IntersectionObserverInit = {}
) => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          callback()
          observer.unobserve(element)
        }
      })
    },
    {
      threshold: 0.1,
      rootMargin: '50px',
      ...options
    }
  )

  observer.observe(element)
  return observer
}

/**
 * 防抖函数
 */
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout | null = null

  return (...args: Parameters<T>) => {
    if (timeout) {
      clearTimeout(timeout)
    }
    timeout = setTimeout(() => func(...args), wait)
  }
}

/**
 * 节流函数
 */
export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean

  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}
