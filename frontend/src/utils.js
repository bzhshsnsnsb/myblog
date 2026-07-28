export const formatDate = (value, full = false) => {
  if (!value) return ''
  return new Intl.DateTimeFormat('zh-CN', full
    ? { year: 'numeric', month: 'long', day: 'numeric' }
    : { year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date(value))
}

export const readingTime = (content = '') => Math.max(1, Math.ceil(content.replace(/\s/g, '').length / 500))

