/**
 * 数据分享工具函数
 */

/**
 * 分享单个数据对象
 */
export const shareData = async (data: any, title?: string, text?: string) => {
  try {
    // 检查是否支持 Web Share API
    if (navigator.share && navigator.canShare) {
      const shareData = {
        title: title || '重庆城市数据',
        text: text || '查看城市数据详情',
        url: window.location.href
      }

      if (navigator.canShare(shareData)) {
        await navigator.share(shareData)
        return true
      }
    }

    // 降级到复制到剪贴板
    return await copyToClipboard(data, title, text)
  } catch (error) {
    console.error('分享失败:', error)
    return false
  }
}

/**
 * 复制数据到剪贴板
 */
export const copyToClipboard = async (data: any, title?: string, text?: string) => {
  try {
    let content = ''

    if (title) {
      content += `${title}\n`
      content += '='.repeat(title.length) + '\n\n'
    }

    if (text) {
      content += `${text}\n\n`
    }

    // 如果是对象，转换为JSON格式
    if (typeof data === 'object') {
      content += JSON.stringify(data, null, 2)
    } else {
      content += String(data)
    }

    await navigator.clipboard.writeText(content)
    alert('数据已复制到剪贴板！')
    return true
  } catch (error) {
    console.error('复制失败:', error)
    return false
  }
}

/**
 * 生成分享链接
 */
export const generateShareLink = (params: Record<string, any>) => {
  const url = new URL(window.location.href)
  Object.entries(params).forEach(([key, value]) => {
    url.searchParams.set(key, String(value))
  })
  return url.toString()
}

/**
 * 解析分享链接参数
 */
export const parseShareParams = () => {
  const url = new URL(window.location.href)
  const params: Record<string, string> = {}

  url.searchParams.forEach((value, key) => {
    params[key] = value
  })

  return params
}

/**
 * 分享图表数据
 */
export const shareChartData = async (chartData: any, chartName: string) => {
  const shareContent = {
    title: `${chartName} - 图表数据`,
    description: `来自重庆城市数据可视化大屏`,
    data: chartData
  }

  return await shareData(
    shareContent,
    shareContent.title,
    `这是一个${chartName}的数据详情，包含${Object.keys(chartData).length}个数据维度。`
  )
}

/**
 * 分享区域详情
 */
export const shareAreaDetail = async (areaData: any) => {
  const title = `【${areaData.name}】区域详情`
  const text = `活力指数: ${areaData.vitality_score}\n火锅店数量: ${areaData.hotpot_count || 0}\n茶馆数量: ${areaData.teahouse_count || 0}`

  return await shareData(areaData, title, text)
}

/**
 * 分享温度指数
 */
export const shareTemperatureIndex = async (indexData: any) => {
  const title = '城市温度指数报告'
  const text = `当前城市温度指数: ${indexData.score}/100\n更新时间: ${indexData.date}`

  return await shareData(indexData, title, text)
}

/**
 * 分享数据对比
 */
export const shareDataComparison = async (comparisonData: any, title: string) => {
  return await shareData(
    comparisonData,
    `${title} - 数据对比`,
    `这是${title}的详细对比数据，包含多个维度的分析结果。`
  )
}
