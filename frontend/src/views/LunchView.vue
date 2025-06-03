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
  <div class="space-y-6">
    <!-- 헤더 섹션 -->
    <div class="flex items-center space-x-4 mb-6">
      <div class="w-12 h-12 bg-gradient-to-br from-green-400 to-green-600 rounded-xl flex items-center justify-center shadow-lg">
        <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </div>
      <div>
        <h1 class="text-3xl font-bold text-gray-900">🍽️ 오늘의 점심 추천</h1>
        <p class="text-gray-600">위치 기반 맛집 추천 서비스</p>
      </div>
    </div>

    <!-- 오류 메시지 -->
    <div v-if="error && !locationPermissionDenied" class="bg-red-50 border border-red-200 rounded-xl p-4">
      <div class="flex items-center">
        <svg class="w-5 h-5 text-red-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="text-red-700">{{ error }}</p>
      </div>
    </div>

    <!-- 위치 권한 거부 시 안내 -->
    <div v-if="locationPermissionDenied" class="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
      <div class="text-center">
        <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        
        <h3 class="text-xl font-bold text-yellow-900 mb-3">위치 권한이 필요합니다</h3>
        <p class="text-yellow-800 mb-6 leading-relaxed">
          맛집 추천을 위해 현재 위치 정보가 필요합니다.<br>
          위치를 공유하시면 주변 맛집을 추천해드릴게요!
        </p>
        
        <div class="space-y-3">
          <button
            @click="requestLocationPermission"
            :disabled="isLoading"
            class="w-full bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
          >
            <span v-if="isLoading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              위치 확인 중...
            </span>
            <span v-else class="flex items-center justify-center">
              <span class="text-xl mr-2">📍</span>
              위치 공유하기
            </span>
          </button>
          
          <button
            @click="showLocationGuide = !showLocationGuide"
            class="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg transition-colors"
          >
            <span class="flex items-center justify-center">
              <span class="text-sm mr-2">⚙️</span>
              {{ showLocationGuide ? '설정 안내 접기' : '브라우저 설정 도움말' }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- 브라우저 설정 안내 -->
    <div v-if="showLocationGuide" class="bg-blue-50 border border-blue-200 rounded-xl p-4">
      <h4 class="font-bold text-blue-900 mb-2 flex items-center">
        <span class="text-lg mr-2">💡</span>
        브라우저 설정 방법
      </h4>
      <p class="text-blue-800 text-sm mb-3">{{ getLocationGuideText() }}</p>
      <div class="text-xs text-blue-600">
        <p>• 설정 변경 후 페이지를 새로고침해주세요</p>
        <p>• 여전히 문제가 있다면 브라우저를 재시작해보세요</p>
      </div>
    </div>

    <!-- 시작 화면 -->
    <div v-if="!recommendedRestaurant && !locationPermissionDenied" class="bg-white rounded-2xl shadow-xl border border-gray-100 p-8 text-center">
      <div class="mb-8">
        <div class="w-20 h-20 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg">
          <svg class="w-10 h-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <h3 class="text-2xl font-bold text-gray-900 mb-3">맛집 추천 서비스</h3>
        <p class="text-gray-600 leading-relaxed">
          현재 위치를 기반으로 주변의 맛집 카테고리를 추천합니다.<br>
          카테고리를 선택하면 실제 맛집들을 네이버지도에서 확인할 수 있어요!
        </p>
      </div>
      
      <button
        @click="requestLocationAndRecommend"
        :disabled="isLoading"
        class="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-semibold py-4 px-8 rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
      >
        <span v-if="isLoading" class="flex items-center">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          위치 확인 중...
        </span>
        <span v-else class="flex items-center">
          <span class="text-xl mr-2">🎯</span>
          맛집 추천받기
        </span>
      </button>
    </div>

    <!-- 추천 결과 화면 -->
    <div v-if="recommendedRestaurant" class="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
      <!-- 추천 카드 -->
      <div class="bg-gradient-to-r from-green-500 to-green-600 px-6 py-6">
        <h3 class="text-xl font-bold text-white flex items-center">
          <span class="text-2xl mr-2">🎯</span>
          오늘의 추천 맛집
        </h3>
      </div>
      
      <div class="p-6">
        <div class="mb-6">
          <h4 class="text-2xl font-bold text-gray-900 mb-3">{{ recommendedRestaurant.name }}</h4>
          <div class="flex items-center space-x-2 text-gray-600 mb-4">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span class="text-sm">{{ recommendedRestaurant.address }}</span>
          </div>
          
          <!-- 현재 위치 정보 표시 -->
          <div v-if="currentLocation?.address" class="bg-gray-50 rounded-lg p-3 mb-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <span class="text-xs font-medium text-gray-500">현재 위치</span>
                <span class="text-sm text-gray-700">{{ currentLocation.address }}</span>
              </div>
              <button
                @click="requestLocationPermission"
                :disabled="isLoading"
                class="text-xs bg-blue-100 hover:bg-blue-200 text-blue-700 px-2 py-1 rounded transition-colors"
              >
                📍 위치 재설정
              </button>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 gap-4 mb-6">
          <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <span class="text-sm font-medium text-gray-600">분류</span>
            <span class="px-3 py-1 bg-green-100 text-green-800 text-sm font-medium rounded-full">
              {{ recommendedRestaurant.category }}
            </span>
          </div>
          
          <div v-if="recommendedRestaurant.rating" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <span class="text-sm font-medium text-gray-600">평점</span>
            <div class="flex items-center">
              <span class="text-yellow-400 text-lg">★</span>
              <span class="text-sm font-semibold ml-1">{{ recommendedRestaurant.rating }}</span>
            </div>
          </div>
          
          <div v-if="recommendedRestaurant.distance" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <span class="text-sm font-medium text-gray-600">거리</span>
            <span class="text-sm font-semibold">{{ recommendedRestaurant.distance }}m</span>
          </div>
        </div>

        <div class="space-y-3">
          <button
            @click="getNewRecommendation"
            :disabled="isLoading"
            class="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-medium py-3 px-4 rounded-xl transition-colors"
          >
            <span class="flex items-center justify-center">
              <span class="text-lg mr-2">🔄</span>
              다른 곳 추천받기
            </span>
          </button>
          
          <button
            @click="openInMap(recommendedRestaurant)"
            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-xl transition-colors"
          >
            <span class="flex items-center justify-center">
              <span class="text-lg mr-2">🗺️</span>
              실제 맛집 찾아보기
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- 사용 안내 -->
    <div class="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-6">
      <h4 class="font-bold text-blue-900 mb-3 flex items-center">
        <span class="text-xl mr-2">💡</span>
        서비스 이용 안내
      </h4>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-blue-800 text-sm">
        <div class="space-y-2">
          <div class="flex items-center">
            <span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
            위치 권한을 허용하면 정확한 추천을 받을 수 있습니다
          </div>
          <div class="flex items-center">
            <span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
            실수로 위치 권한을 거부했다면 "위치 공유하기" 버튼을 눌러주세요
          </div>
          <div class="flex items-center">
            <span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
            현재 위치 기준 1km 반경 내 음식점을 추천합니다
          </div>
        </div>
        <div class="space-y-2">
          <div class="flex items-center">
            <span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
            카테고리를 추천받고 네이버지도에서 실제 맛집을 확인하세요
          </div>
          <div class="flex items-center">
            <span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
            현재 위치 기준으로 해당 카테고리의 음식점들을 검색합니다
          </div>
          <div class="flex items-center">
            <span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
            마음에 들지 않으면 다른 카테고리를 추천받을 수 있습니다
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