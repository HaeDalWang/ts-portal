<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 상태 관리
const isLoading = ref(false)
const hasLocationPermission = ref(false)
const locationPermissionDenied = ref(false)
const showLocationGuide = ref(false)
const currentLocation = ref<LocationData | null>(null)
const recommendedRestaurant = ref<any>(null)
const error = ref<string>('')

// 타입 정의
interface Restaurant {
  name: string
  address: string
  category: string
  rating?: number
  distance?: number
  phone?: string
}

interface LocationData {
  lat: number
  lng: number
  address?: string
  city?: string
  district?: string
  country?: string
}

// 현재 위치 가져오기 (향상된 버전)
const getCurrentLocation = (): Promise<LocationData> => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('이 브라우저에서는 위치 서비스가 지원되지 않습니다.'))
      return
    }

    console.log('📍 GPS 위치 요청 중...')
    
    // 권한 상태 초기화
    locationPermissionDenied.value = false
    showLocationGuide.value = false
    
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const lat = position.coords.latitude
        const lng = position.coords.longitude
        console.log('✅ GPS 좌표 획득:', lat, lng)
        
        // 권한 허용됨
        hasLocationPermission.value = true
        locationPermissionDenied.value = false
        
        try {
          // Nominatim Reverse Geocoding으로 실제 주소 얻기
          const addressInfo = await reverseGeocode(lat, lng)
          const locationData: LocationData = {
            lat,
            lng,
            ...addressInfo
          }
          console.log('✅ 완전한 위치 정보:', locationData)
          resolve(locationData)
        } catch (error) {
          console.warn('⚠️ 주소 변환 실패, GPS 좌표만 사용:', error)
          // 주소 변환 실패해도 GPS 좌표는 반환
          resolve({ lat, lng })
        }
      },
      (error) => {
        let message = '위치를 가져올 수 없습니다.'
        let isPermissionError = false
        
        switch (error.code) {
          case error.PERMISSION_DENIED:
            message = '위치 권한이 거부되었습니다.'
            isPermissionError = true
            locationPermissionDenied.value = true
            hasLocationPermission.value = false
            break
          case error.POSITION_UNAVAILABLE:
            message = '위치 정보를 사용할 수 없습니다. GPS나 네트워크를 확인해주세요.'
            break
          case error.TIMEOUT:
            message = '위치 요청이 시간 초과되었습니다. 다시 시도해주세요.'
            break
        }
        
        console.error('❌ GPS 위치 오류:', message)
        
        // 권한 오류가 아닌 경우만 일반 오류로 처리
        if (!isPermissionError) {
          reject(new Error(message))
        } else {
          // 권한 오류는 특별히 처리 (UI에서 안내 표시)
          reject(new Error(message))
        }
      },
      {
        enableHighAccuracy: true, // 고정밀 위치 요청
        timeout: 15000, // 15초 타임아웃
        maximumAge: 300000 // 5분간 캐시된 위치 사용
      }
    )
  })
}

// Nominatim Reverse Geocoding API 호출
const reverseGeocode = async (lat: number, lng: number): Promise<Partial<LocationData>> => {
  console.log('🌍 주소 변환 시작:', lat, lng)
  
  try {
    const url = `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json&addressdetails=1&accept-language=ko,en`
    
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'TS-Portal/1.0 (Lunch-Recommendation-Service)' // 한글을 영문으로 변경
      }
    })
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    
    const data = await response.json()
    console.log('🗺️ Nominatim 응답:', data)
    
    if (!data || data.error) {
      throw new Error(data?.error || '주소를 찾을 수 없습니다.')
    }
    
    // 주소 정보 추출 및 한국어 형식으로 변환
    const address = data.address || {}
    const addressComponents = []
    
    // 한국 주소 형식: 시/도 + 구/군 + 동/읍면 순서
    if (address.country === '대한민국' || address.country === 'South Korea') {
      // 한국 주소
      if (address.province || address.state) addressComponents.push(address.province || address.state)
      if (address.city || address.county) addressComponents.push(address.city || address.county)
      if (address.borough || address.district) addressComponents.push(address.borough || address.district)
      if (address.neighbourhood || address.suburb) addressComponents.push(address.neighbourhood || address.suburb)
    } else {
      // 해외 주소
      if (address.country) addressComponents.push(address.country)
      if (address.state) addressComponents.push(address.state)
      if (address.city || address.town || address.village) {
        addressComponents.push(address.city || address.town || address.village)
      }
      if (address.suburb || address.neighbourhood) {
        addressComponents.push(address.suburb || address.neighbourhood)
      }
    }
    
    const fullAddress = addressComponents.join(' ') || data.display_name || '알 수 없는 위치'
    
    const result = {
      address: fullAddress,
      city: address.city || address.town || address.village || '알 수 없는 도시',
      district: address.quarter || address.borough || address.district || address.county || address.neighbourhood || address.suburb || '알 수 없는 구역',
      country: address.country || '알 수 없는 국가'
    }
    
    console.log('✅ 주소 변환 완료:', result)
    return result
    
  } catch (error) {
    console.error('❌ Reverse Geocoding 오류:', error)
    throw error
  }
}

// 향상된 더미 데이터 (실제 위치 및 주소 기반)
const getDummyRestaurants = (userLocation: LocationData): Restaurant[] => {
  console.log('🍽️ 음식점 데이터 생성:', userLocation)
  
  // 위치 기반 음식점 카테고리 결정
  const isKorea = userLocation.country === '대한민국' || userLocation.country === 'South Korea'
  console.log('🇰🇷 한국 위치 판별:', { country: userLocation.country, isKorea })
  
  const restaurantTypes = isKorea 
    ? ['한식', '중식', '일식', '양식', '치킨', '피자', '분식', '카페']
    : ['현지음식', '아시안', '이탈리안', '패스트푸드', '카페', '피자', '버거', '베이커리']
  
  const restaurants: Restaurant[] = [
    { 
      name: isKorea ? '이 지역의 한식 맛집' : 'Local Food in this area', 
      address: `${userLocation.city} ${userLocation.district}`, 
      category: restaurantTypes[0], 
      rating: 4.5, 
      distance: 200
    },
    { 
      name: isKorea ? '이 지역의 양식 맛집' : 'Western Food in this area', 
      address: `${userLocation.city} ${userLocation.district}`, 
      category: restaurantTypes[3], 
      rating: 4.2, 
      distance: 350
    },
    { 
      name: isKorea ? '이 지역의 일식 맛집' : 'Japanese Food in this area', 
      address: `${userLocation.city} ${userLocation.district}`, 
      category: restaurantTypes[2], 
      rating: 4.7, 
      distance: 180
    },
    { 
      name: isKorea ? '이 지역의 중식 맛집' : 'Chinese Food in this area', 
      address: `${userLocation.city} ${userLocation.district}`, 
      category: restaurantTypes[1], 
      rating: 4.0, 
      distance: 420
    },
    { 
      name: isKorea ? '이 지역의 치킨 맛집' : 'Chicken in this area', 
      address: `${userLocation.city} ${userLocation.district}`, 
      category: restaurantTypes[4], 
      rating: 3.8, 
      distance: 150
    },
    { 
      name: isKorea ? '이 지역의 일식 맛집' : 'Japanese Food in this area', 
      address: `${userLocation.city} ${userLocation.district}`, 
      category: restaurantTypes[2], 
      rating: 4.3, 
      distance: 280
    },
    { 
      name: isKorea ? '이 지역의 카페' : 'Cafes in this area', 
      address: `${userLocation.city} ${userLocation.district}`, 
      category: restaurantTypes[7], 
      rating: 4.1, 
      distance: 380
    },
    { 
      name: isKorea ? '이 지역의 피자 맛집' : 'Pizza in this area', 
      address: `${userLocation.city} ${userLocation.district}`, 
      category: restaurantTypes[5], 
      rating: 4.4, 
      distance: 320
    }
  ]
  
  console.log('✅ 음식점 데이터 생성 완료:', restaurants.length, '개')
  return restaurants
}

// 랜덤 음식점 추천
const getRandomRestaurant = (restaurants: Restaurant[]): Restaurant => {
  const randomIndex = Math.floor(Math.random() * restaurants.length)
  return restaurants[randomIndex]
}

// 위치 권한 요청 및 추천 실행
const requestLocationAndRecommend = async () => {
  try {
    isLoading.value = true
    error.value = ''
    console.log('🎯 점심 추천 프로세스 시작')
    
    // 1. 현재 위치 가져오기
    console.log('📍 현재 위치 요청 중...')
    const location = await getCurrentLocation()
    currentLocation.value = location
    hasLocationPermission.value = true
    console.log('✅ 위치 획득 성공:', location)
    
    // 2. 주변 음식점 검색 (더미 데이터 사용)
    console.log('🍽️ 음식점 데이터 생성 중...')
    const restaurants = getDummyRestaurants(location)
    
    if (restaurants.length === 0) {
      throw new Error('주변에 음식점을 찾을 수 없습니다.')
    }
    console.log('✅ 음식점 데이터 생성 완료:', restaurants.length, '개')
    
    // 3. 랜덤 추천
    const recommended = getRandomRestaurant(restaurants)
    recommendedRestaurant.value = recommended
    console.log('🎯 추천 음식점:', recommended)
    console.log('✅ 점심 추천 프로세스 완료!')
    
  } catch (err) {
    const errorMessage = err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.'
    error.value = errorMessage
    console.error('❌ 추천 오류:', err)
  } finally {
    isLoading.value = false
  }
}

// 다시 추천받기
const getNewRecommendation = async () => {
  if (!currentLocation.value) {
    await requestLocationAndRecommend()
    return
  }
  
  try {
    isLoading.value = true
    const restaurants = getDummyRestaurants(currentLocation.value)
    const recommended = getRandomRestaurant(restaurants)
    recommendedRestaurant.value = recommended
    
  } catch (err) {
    error.value = err instanceof Error ? err.message : '추천을 가져올 수 없습니다.'
  } finally {
    isLoading.value = false
  }
}

// 위치 권한 재요청 함수
const requestLocationPermission = async () => {
  try {
    isLoading.value = true
    error.value = ''
    showLocationGuide.value = false
    
    console.log('🔄 위치 권한 재요청 중...')
    await requestLocationAndRecommend()
    
  } catch (err) {
    console.error('❌ 위치 권한 재요청 실패:', err)
    // 여전히 권한이 거부된 경우 브라우저 설정 안내 표시
    if (locationPermissionDenied.value) {
      showLocationGuide.value = true
    }
  } finally {
    isLoading.value = false
  }
}

// 네이버 지도에서 보기 함수 (카테고리별 지역 검색)
const openInMap = (restaurant: Restaurant) => {
  // 현재 위치의 시/구 + 음식 카테고리로 검색
  const location = currentLocation.value?.city || currentLocation.value?.district || '현재위치'
  const searchQuery = encodeURIComponent(`${location} ${restaurant.category}`)
  const url = `https://map.naver.com/v5/search/${searchQuery}`
  window.open(url, '_blank')
}

// 브라우저별 위치 설정 안내
const getLocationGuideText = (): string => {
  const userAgent = navigator.userAgent
  
  if (userAgent.includes('Chrome')) {
    return '주소창 왼쪽의 🔒 아이콘 → 위치 → "허용" 선택 후 새로고침'
  } else if (userAgent.includes('Firefox')) {
    return '주소창 왼쪽의 🛡️ 아이콘 → 권한 → 위치 → "허용" 선택 후 새로고침'
  } else if (userAgent.includes('Safari')) {
    return 'Safari → 환경설정 → 웹사이트 → 위치 서비스 → 이 웹사이트 "허용" 설정'
  } else if (userAgent.includes('Edge')) {
    return '주소창 오른쪽의 🔒 아이콘 → 위치 → "허용" 선택 후 새로고침'
  }
  
  return '브라우저 설정에서 이 사이트의 위치 권한을 허용해주세요.'
}

// 컴포넌트 마운트시 위치 권한 상태 체크
onMounted(() => {
  if (navigator.permissions) {
    navigator.permissions.query({ name: 'geolocation' }).then((result) => {
      hasLocationPermission.value = result.state === 'granted'
    })
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 컴팩트 헤더 -->
    <div class="bg-white border-b border-gray-200 px-6 py-3">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-gray-900">점심 추천</h1>
          <p class="text-sm text-gray-500">오늘의 맛집 추천과 팀원 추천 메뉴</p>
        </div>
        
        <!-- 통계 정보 -->
        <div class="flex items-center space-x-4">
          <div class="text-center">
            <div class="text-sm font-semibold text-green-600">{{ recommendedRestaurant ? '1' : '0' }}</div>
            <div class="text-xs text-gray-500">추천 맛집</div>
          </div>
          <div class="text-center">
            <div class="text-sm font-semibold text-blue-600">{{ currentLocation ? '허용' : '미허용' }}</div>
            <div class="text-xs text-gray-500">위치 권한</div>
          </div>
          <div class="text-center">
            <div class="text-sm font-semibold text-purple-600">{{ currentLocation?.city || '알 수 없음' }}</div>
            <div class="text-xs text-gray-500">현재 위치</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="p-6 space-y-6">
      <!-- 위치 권한 요청 카드 -->
      <div v-if="!hasLocationPermission && !locationPermissionDenied" class="bg-gradient-to-r from-green-500 to-blue-600 rounded-xl p-6 text-white">
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-bold mb-2">위치 기반 맛집 추천을 위해 위치 권한이 필요합니다</h3>
            <p class="text-green-100 text-sm mb-4">현재 위치를 기반으로 주변 맛집을 추천해드립니다.</p>
            <button 
              @click="requestLocationAndRecommend"
              :disabled="isLoading"
              class="bg-white bg-opacity-20 hover:bg-opacity-30 text-white px-4 py-2 rounded-lg transition-colors text-sm font-medium"
            >
              {{ isLoading ? '위치 확인 중...' : '위치 허용하고 추천받기' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 위치 권한 거부 시 안내 -->
      <div v-if="locationPermissionDenied" class="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
        <div class="flex items-start space-x-4">
          <svg class="w-6 h-6 text-yellow-600 mt-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <div class="flex-1">
            <h3 class="text-sm font-semibold text-yellow-800 mb-2">위치 권한이 거부되었습니다</h3>
            <p class="text-xs text-yellow-700 mb-4">
              맞춤형 맛집 추천을 위해 위치 권한을 허용해주세요. 브라우저 설정에서 위치 권한을 허용하거나 새로고침 후 다시 시도해보세요.
            </p>
            <div class="flex space-x-3">
              <button 
                @click="requestLocationAndRecommend"
                :disabled="isLoading"
                class="bg-yellow-600 hover:bg-yellow-700 text-white px-3 py-2 rounded-lg text-xs"
              >
                다시 시도
              </button>
              <button 
                @click="showLocationGuide = true"
                class="bg-gray-200 hover:bg-gray-300 text-gray-700 px-3 py-2 rounded-lg text-xs"
              >
                설정 도움말
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 위치 설정 도움말 -->
      <div v-if="showLocationGuide" class="bg-blue-50 border border-blue-200 rounded-xl p-6">
        <div class="flex items-start justify-between mb-4">
          <h3 class="text-sm font-semibold text-blue-800">위치 권한 설정 방법</h3>
          <button @click="showLocationGuide = false" class="text-blue-400 hover:text-blue-600">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="space-y-3 text-xs text-blue-700">
          <div>
            <strong>Chrome:</strong> 주소창 왼쪽의 자물쇠/위치 아이콘 클릭 → '위치' 허용
          </div>
          <div>
            <strong>Safari:</strong> Safari 메뉴 → 환경설정 → 웹사이트 → 위치 서비스 → 허용
          </div>
          <div>
            <strong>Firefox:</strong> 주소창 왼쪽의 방패/자물쇠 아이콘 클릭 → 권한 → 위치 허용
          </div>
        </div>
      </div>

      <!-- 오류 메시지 -->
      <div v-if="error" class="bg-red-50 border border-red-200 rounded-xl p-6">
        <div class="flex items-center space-x-3">
          <svg class="w-5 h-5 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h3 class="text-sm font-semibold text-red-800">오류가 발생했습니다</h3>
            <p class="text-xs text-red-700 mt-1">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- 로딩 상태 -->
      <div v-if="isLoading" class="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
        <div class="flex items-center justify-center space-x-3">
          <svg class="animate-spin h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span class="text-xs text-gray-600">맛집을 찾는 중...</span>
        </div>
      </div>

      <!-- 현재 위치 정보 -->
      <div v-if="currentLocation && !isLoading" class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
        <h3 class="text-sm font-semibold text-gray-900 mb-4 flex items-center">
          <svg class="w-4 h-4 text-green-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          현재 위치 정보
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div class="space-y-2">
            <div class="flex justify-between">
              <span class="font-medium text-gray-700">주소:</span>
              <span class="text-gray-600">{{ currentLocation.address || '주소 정보 없음' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="font-medium text-gray-700">도시:</span>
              <span class="text-gray-600">{{ currentLocation.city || '알 수 없음' }}</span>
            </div>
          </div>
          <div class="space-y-2">
            <div class="flex justify-between">
              <span class="font-medium text-gray-700">구역:</span>
              <span class="text-gray-600">{{ currentLocation.district || '알 수 없음' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="font-medium text-gray-700">국가:</span>
              <span class="text-gray-600">{{ currentLocation.country || '알 수 없음' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 추천 맛집 -->
      <div v-if="recommendedRestaurant && !isLoading" class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        <!-- 카드 헤더 -->
        <div class="bg-gradient-to-r from-green-50 to-green-100 px-6 py-4 border-b border-green-200">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-gradient-to-br from-green-400 to-green-600 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C20.832 18.477 19.246 18 17.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div>
                <h3 class="text-sm font-semibold text-gray-900">오늘의 추천 맛집</h3>
                <p class="text-xs text-gray-600">현재 위치 기반 추천</p>
              </div>
            </div>
            
            <!-- 카테고리 배지 -->
            <div class="px-2 py-1 bg-green-100 text-green-600 rounded-full text-xs font-semibold">
              {{ recommendedRestaurant.category }}
            </div>
          </div>
        </div>

        <!-- 카드 본문 -->
        <div class="p-6">
          <h2 class="text-sm font-semibold text-gray-900 mb-3">
            {{ recommendedRestaurant.name }}
          </h2>
          
          <div class="space-y-2 mb-4">
            <div class="flex items-center text-xs text-gray-600">
              <svg class="w-3 h-3 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              {{ recommendedRestaurant.address }}
            </div>
            
            <div v-if="recommendedRestaurant.distance" class="flex items-center text-xs text-gray-600">
              <svg class="w-3 h-3 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              도보 약 {{ recommendedRestaurant.distance }}m
            </div>
            
            <div v-if="recommendedRestaurant.rating" class="flex items-center text-xs text-gray-600">
              <svg class="w-3 h-3 mr-2 text-yellow-500" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
              </svg>
              평점 {{ recommendedRestaurant.rating }}/5.0
            </div>
          </div>

          <!-- 액션 버튼 -->
          <div class="flex items-center justify-between pt-4 border-t border-gray-100">
            <button
              @click="requestLocationAndRecommend"
              :disabled="isLoading"
              class="flex items-center space-x-2 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors text-xs"
            >
              <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span>다른 맛집 추천</span>
            </button>
            
            <div class="text-xs text-gray-500">
              AI 추천 알고리즘 기반
            </div>
          </div>
        </div>
      </div>

      <!-- 팀원 추천 메뉴 섹션 -->
      <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
        <h3 class="text-sm font-semibold text-gray-900 mb-4 flex items-center">
          <svg class="w-4 h-4 text-purple-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          팀원 추천 메뉴
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          <div class="bg-purple-50 border border-purple-200 rounded-lg p-3">
            <div class="flex items-center space-x-2 mb-2">
              <div class="w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center">
                <span class="text-white text-xs font-bold">김</span>
              </div>
              <span class="text-xs font-medium text-gray-700">김철수</span>
            </div>
            <p class="text-xs text-gray-600">"오늘은 김치찌개가 생각나네요! 🍲"</p>
          </div>
          
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
            <div class="flex items-center space-x-2 mb-2">
              <div class="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
                <span class="text-white text-xs font-bold">박</span>
              </div>
              <span class="text-xs font-medium text-gray-700">박영희</span>
            </div>
            <p class="text-xs text-gray-600">"파스타 한 그릇 어떠세요? 🍝"</p>
          </div>
          
          <div class="bg-green-50 border border-green-200 rounded-lg p-3">
            <div class="flex items-center space-x-2 mb-2">
              <div class="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                <span class="text-white text-xs font-bold">이</span>
              </div>
              <span class="text-xs font-medium text-gray-700">이민수</span>
            </div>
            <p class="text-xs text-gray-600">"치킨 한 마리 시킬까요? 🍗"</p>
          </div>
        </div>
      </div>

      <!-- 기능 안내 -->
      <div class="bg-gray-50 rounded-xl p-6">
        <h3 class="text-sm font-semibold text-gray-900 mb-4">💡 점심 추천 서비스 안내</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-gray-600">
          <div class="space-y-2">
            <div class="flex items-start space-x-2">
              <svg class="w-3 h-3 text-green-500 mt-0.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>현재 위치 기반 맛집 추천</span>
            </div>
            <div class="flex items-start space-x-2">
              <svg class="w-3 h-3 text-green-500 mt-0.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>팀원들의 실시간 메뉴 추천</span>
            </div>
          </div>
          <div class="space-y-2">
            <div class="flex items-start space-x-2">
              <svg class="w-3 h-3 text-green-500 mt-0.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>거리 및 평점 정보 제공</span>
            </div>
            <div class="flex items-start space-x-2">
              <svg class="w-3 h-3 text-green-500 mt-0.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>AI 기반 개인 맞춤 추천</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 점심 추천 페이지 전용 스타일 */

/* 카드 호버 효과 */
.hover-card {
  transition: all 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* 버튼 애니메이션 */
button {
  transition: all 0.2s ease;
}

button:hover:not(:disabled) {
  transform: translateY(-1px);
}

button:active:not(:disabled) {
  transform: translateY(0);
}
</style> 