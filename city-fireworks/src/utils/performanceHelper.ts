/**
 * 性能优化工具函数
 */

import * as echarts from 'echarts'

/**
 * 内存缓存管理
 */
export class MemoryCache {
  private cache = new Map<string, { data: any; timestamp: number; size: number }>()
  private maxSize: number
  private ttl: number

  constructor(maxSize: number = 100, ttl: number = 5 * 60 * 1000) {
    this.maxSize = maxSize
    this.ttl = ttl
  }

  set(key: string, data: any): void {
    // 清理过期数据
    this.cleanup()

    // 如果缓存已满，删除最旧的数据
    if (this.cache.size >= this.maxSize) {
      const oldestKey = this.getOldestKey()
      if (oldestKey) {
        this.cache.delete(oldestKey)
      }
    }

    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      size: this.calculateSize(data)
    })
  }

  get(key: string): any | null {
    const item = this.cache.get(key)
    if (!item) return null

    // 检查是否过期
    if (Date.now() - item.timestamp > this.ttl) {
      this.cache.delete(key)
      return null
    }

    return item.data
  }

  has(key: string): boolean {
    const item = this.cache.get(key)
    if (!item) return false

    if (Date.now() - item.timestamp > this.ttl) {
      this.cache.delete(key)
      return false
    }

    return true
  }

  clear(): void {
    this.cache.clear()
  }

  private cleanup(): void {
    const now = Date.now()
    for (const [key, item] of this.cache.entries()) {
      if (now - item.timestamp > this.ttl) {
        this.cache.delete(key)
      }
    }
  }

  private getOldestKey(): string | null {
    let oldestKey: string | null = null
    let oldestTime = Infinity

    for (const [key, item] of this.cache.entries()) {
      if (item.timestamp < oldestTime) {
        oldestTime = item.timestamp
        oldestKey = key
      }
    }

    return oldestKey
  }

  private calculateSize(data: any): number {
    return new Blob([JSON.stringify(data)]).size
  }

  getStats() {
    return {
      size: this.cache.size,
      maxSize: this.maxSize,
      usage: `${this.cache.size}/${this.maxSize}`,
      totalSize: Array.from(this.cache.values()).reduce((sum, item) => sum + item.size, 0)
    }
  }
}

/**
 * 数据分页加载
 */
export class DataPager {
  private pageSize: number
  private currentPage: number = 0
  private totalItems: number = 0
  private data: any[] = []

  constructor(pageSize: number = 100) {
    this.pageSize = pageSize
  }

  setData(data: any[]): void {
    this.data = data
    this.totalItems = data.length
  }

  getPage(page: number): any[] {
    this.currentPage = page
    const start = page * this.pageSize
    const end = start + this.pageSize
    return this.data.slice(start, end)
  }

  getTotalPages(): number {
    return Math.ceil(this.totalItems / this.pageSize)
  }

  getCurrentPage(): number {
    return this.currentPage
  }

  hasNextPage(): boolean {
    return this.currentPage < this.getTotalPages() - 1
  }

  hasPreviousPage(): boolean {
    return this.currentPage > 0
  }

  getItemCount(): number {
    return this.totalItems
  }
}

/**
 * 图表性能优化
 */
export class ChartOptimizer {
  private static instance: ChartOptimizer
  private cache = new MemoryCache(50, 10 * 60 * 1000) // 10分钟缓存
  private renderQueue: Map<string, Promise<echarts.ECharts>> = new Map()

  static getInstance(): ChartOptimizer {
    if (!ChartOptimizer.instance) {
      ChartOptimizer.instance = new ChartOptimizer()
    }
    return ChartOptimizer.instance
  }

  /**
   * 优化大数据集图表渲染
   */
  optimizeLargeDataset(option: any, threshold: number = 1000): any {
    // 如果数据量超过阈值，进行优化
    if (option.series && option.series[0]?.data) {
      const data = option.series[0].data
      if (data.length > threshold) {
        option.series[0].data = this.reduceDataResolution(data, Math.floor(data.length / 10))
        option.tooltip = option.tooltip || {}
        option.tooltip.axisPointer = {
          type: 'cross',
          animation: false
        }
      }
    }

    return option
  }

  /**
   * 降低数据分辨率
   */
  private reduceDataResolution(data: any[], targetSize: number): any[] {
    if (data.length <= targetSize) return data

    const step = Math.floor(data.length / targetSize)
    const reduced: any[] = []

    for (let i = 0; i < data.length; i += step) {
      const chunk = data.slice(i, i + step)
      reduced.push(this.aggregateChunk(chunk))
    }

    return reduced
  }

  /**
   * 聚合数据块
   */
  private aggregateChunk(chunk: any[]): any {
    if (typeof chunk[0] === 'number') {
      return chunk.reduce((sum, val) => sum + val, 0) / chunk.length
    }
    return chunk[Math.floor(chunk.length / 2)] // 取中间值
  }

  /**
   * 缓存图表实例
   */
  cacheChart(key: string, chart: echarts.ECharts): void {
    this.cache.set(key, chart)
  }

  /**
   * 获取缓存的图表实例
   */
  getCachedChart(key: string): echarts.ECharts | null {
    return this.cache.get(key)
  }

  /**
   * 异步渲染图表
   */
  async renderChart(
    container: HTMLElement,
    option: any,
    key?: string
  ): Promise<echarts.ECharts> {
    const cacheKey = key || this.generateKey(container, option)

    // 检查是否有正在进行的渲染
    if (this.renderQueue.has(cacheKey)) {
      return this.renderQueue.get(cacheKey)!
    }

    // 开始渲染
    const promise = (async () => {
      try {
        // 检查缓存
        const cached = this.getCachedChart(cacheKey)
        if (cached) {
          cached.setOption(option, true)
          return cached
        }

        // 优化选项
        const optimizedOption = this.optimizeLargeDataset(option)

        // 创建图表
        const chart = echarts.init(container, null, {
          renderer: 'canvas', // 使用canvas渲染器
          useDirtyRect: true // 脏矩形优化
        })

        chart.setOption(optimizedOption, true)
        this.cacheChart(cacheKey, chart)

        return chart
      } finally {
        this.renderQueue.delete(cacheKey)
      }
    })()

    this.renderQueue.set(cacheKey, promise)
    return promise
  }

  private generateKey(container: HTMLElement, option: any): string {
    return `chart_${container.id || 'default'}_${JSON.stringify(option)}`
  }

  /**
   * 销毁所有图表实例
   */
  disposeAll(): void {
    const charts = this.cache as any
    for (const item of charts.cache.values()) {
      if (item.data && item.data.dispose) {
        item.data.dispose()
      }
    }
    charts.clear()
  }
}

/**
 * 监控性能
 */
export class PerformanceMonitor {
  private static instance: PerformanceMonitor
  private metrics: Map<string, number[]> = new Map()

  static getInstance(): PerformanceMonitor {
    if (!PerformanceMonitor.instance) {
      PerformanceMonitor.instance = new PerformanceMonitor()
    }
    return PerformanceMonitor.instance
  }

  /**
   * 记录性能指标
   */
  record(name: string, value: number): void {
    if (!this.metrics.has(name)) {
      this.metrics.set(name, [])
    }
    this.metrics.get(name)!.push(value)

    // 限制保存的数据点数量
    const data = this.metrics.get(name)!
    if (data.length > 100) {
      data.shift()
    }
  }

  /**
   * 获取性能指标
   */
  getMetrics(name: string): number[] {
    return this.metrics.get(name) || []
  }

  /**
   * 获取平均性能
   */
  getAverage(name: string): number {
    const data = this.getMetrics(name)
    if (data.length === 0) return 0
    return data.reduce((sum, val) => sum + val, 0) / data.length
  }

  /**
   * 获取性能报告
   */
  getReport(): Record<string, { average: number; min: number; max: number; count: number }> {
    const report: Record<string, any> = {}

    for (const [name, data] of this.metrics.entries()) {
      report[name] = {
        average: this.getAverage(name),
        min: Math.min(...data),
        max: Math.max(...data),
        count: data.length
      }
    }

    return report
  }

  /**
   * 清除所有指标
   */
  clear(): void {
    this.metrics.clear()
  }
}

/**
 * 批量处理数据
 */
export const batchProcess = async <T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  batchSize: number = 10
): Promise<R[]> => {
  const results: R[] = []
  const batches = Math.ceil(items.length / batchSize)

  for (let i = 0; i < batches; i++) {
    const start = i * batchSize
    const end = Math.min(start + batchSize, items.length)
    const batch = items.slice(start, end)

    const batchResults = await Promise.all(batch.map(processor))
    results.push(...batchResults)

    // 让出控制权，避免阻塞UI
    await new Promise(resolve => setTimeout(resolve, 0))
  }

  return results
}
