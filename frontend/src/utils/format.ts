/**
 * 날짜 포맷팅 유틸리티
 */
export const formatDate = {
  // 기본 날짜 포맷 (YYYY-MM-DD)
  basic: (date: string | Date): string => {
    const d = new Date(date)
    return d.toISOString().split('T')[0]
  },

  // 한국어 날짜 포맷 (YYYY년 MM월 DD일)
  korean: (date: string | Date): string => {
    const d = new Date(date)
    const year = d.getFullYear()
    const month = d.getMonth() + 1
    const day = d.getDate()
    return `${year}년 ${month}월 ${day}일`
  },

  // 한국어 날짜 + 요일 포맷 (YYYY년 MM월 DD일 (요일))
  koreanWithDay: (date: string | Date): string => {
    const d = new Date(date)
    const year = d.getFullYear()
    const month = d.getMonth() + 1
    const day = d.getDate()
    const weekday = ['일', '월', '화', '수', '목', '금', '토'][d.getDay()]
    return `${year}년 ${month}월 ${day}일 (${weekday})`
  },

  // 상대적 시간 (몇 분 전, 몇 시간 전 등)
  relative: (date: string | Date): string => {
    const now = new Date()
    const target = new Date(date)
    const diffMs = now.getTime() - target.getTime()
    const diffMinutes = Math.floor(diffMs / (1000 * 60))
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

    if (diffMinutes < 1) return '방금 전'
    if (diffMinutes < 60) return `${diffMinutes}분 전`
    if (diffHours < 24) return `${diffHours}시간 전`
    if (diffDays < 7) return `${diffDays}일 전`
    
    return formatDate.korean(date)
  },

  // 시간 포맷 (HH:MM)
  time: (time: string | Date): string => {
    const d = new Date(time)
    return d.toLocaleTimeString('ko-KR', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false 
    })
  },

  // 날짜 + 시간 포맷 (YYYY-MM-DD HH:MM)
  datetime: (datetime: string | Date): string => {
    const d = new Date(datetime)
    const date = formatDate.basic(d)
    const time = formatDate.time(d)
    return `${date} ${time}`
  }
}

/**
 * 숫자 포맷팅 유틸리티
 */
export const formatNumber = {
  // 천 단위 콤마 추가
  comma: (num: number): string => {
    return num.toLocaleString('ko-KR')
  },

  // 파일 크기 포맷 (B, KB, MB, GB)
  fileSize: (bytes: number): string => {
    if (bytes === 0) return '0 B'
    
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`
  },

  // 퍼센트 포맷
  percent: (value: number, total: number, decimals: number = 1): string => {
    if (total === 0) return '0%'
    const percentage = (value / total) * 100
    return `${percentage.toFixed(decimals)}%`
  },

  // 통화 포맷 (원화)
  currency: (amount: number): string => {
    return `${formatNumber.comma(amount)}원`
  }
}

/**
 * 텍스트 포맷팅 유틸리티
 */
export const formatText = {
  // 텍스트 자르기 (말줄임표 추가)
  truncate: (text: string, length: number): string => {
    if (text.length <= length) return text
    return `${text.slice(0, length)}...`
  },

  // 첫 글자 대문자로
  capitalize: (text: string): string => {
    return text.charAt(0).toUpperCase() + text.slice(1)
  },

  // 카멜케이스를 공백으로 분리
  camelToWords: (text: string): string => {
    return text.replace(/([A-Z])/g, ' $1').trim()
  },

  // HTML 태그 제거
  stripHtml: (html: string): string => {
    return html.replace(/<[^>]*>/g, '')
  },

  // 이메일 마스킹 (a***@***.com)
  maskEmail: (email: string): string => {
    const [local, domain] = email.split('@')
    if (!domain) return email
    
    const maskedLocal = local.charAt(0) + '*'.repeat(Math.max(0, local.length - 1))
    const [domainName, tld] = domain.split('.')
    const maskedDomain = '*'.repeat(domainName.length)
    
    return `${maskedLocal}@${maskedDomain}.${tld}`
  }
}

/**
 * 상태 관련 포맷팅 유틸리티
 */
export const formatStatus = {
  // 우선순위 텍스트
  priority: (level: string): string => {
    const priorityMap: { [key: string]: string } = {
      'low': '낮음',
      'medium': '보통',
      'high': '높음',
      'urgent': '긴급'
    }
    return priorityMap[level] || level
  },

  // 상태 텍스트
  status: (status: string): string => {
    const statusMap: { [key: string]: string } = {
      'active': '활성',
      'inactive': '비활성',
      'pending': '대기중',
      'completed': '완료',
      'cancelled': '취소',
      'draft': '임시저장',
      'published': '게시됨',
      'scheduled': '예정',
      'in_progress': '진행중'
    }
    return statusMap[status] || status
  },

  // 불린 값을 한국어로
  boolean: (value: boolean): string => {
    return value ? '예' : '아니오'
  }
}

/**
 * 색상 관련 유틸리티
 */
export const formatColor = {
  // ID를 기반으로 일관된 색상 생성 (HSL)
  fromId: (id: number): string => {
    const hue = (id * 137.508) % 360 // 황금각 사용
    const saturation = 45 + (id % 15) // 45-60% 채도
    const lightness = 60 + (id % 15)  // 60-75% 명도
    return `hsl(${hue}, ${saturation}%, ${lightness}%)`
  },

  // 문자열을 기반으로 색상 생성
  fromString: (str: string): string => {
    let hash = 0
    for (let i = 0; i < str.length; i++) {
      hash = str.charCodeAt(i) + ((hash << 5) - hash)
    }
    return formatColor.fromId(Math.abs(hash))
  },

  // 배경색에 맞는 텍스트 색상 반환
  contrastText: (backgroundColor: string): string => {
    // 간단한 명도 계산 (실제로는 더 복잡한 계산이 필요)
    const rgb = backgroundColor.match(/\d+/g)
    if (!rgb) return '#000000'
    
    const brightness = (parseInt(rgb[0]) * 299 + parseInt(rgb[1]) * 587 + parseInt(rgb[2]) * 114) / 1000
    return brightness > 128 ? '#000000' : '#ffffff'
  }
} 