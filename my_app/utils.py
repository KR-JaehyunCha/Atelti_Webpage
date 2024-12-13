import requests
import logging

logger = logging.getLogger(__name__)

def fetch_api_data(endpoint, params, headers):
    """
    공통 API 호출 함수
    :param endpoint: API 엔드포인트 URL
    :param params: 요청 파라미터 (dict)
    :param headers: 요청 헤더 (dict)
    :return: API 응답 데이터 (dict)
    """
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()  # 상태 코드가 200이 아니면 예외 발생
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API 호출 오류: {e}")
        return {"error": "API 호출 실패"}
