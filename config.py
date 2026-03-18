"""
애플리케이션 전역 설정 파일
"""

import os

# 애플리케이션 정보
APP_NAME = "자원봉사자 출퇴근 관리 시스템"
APP_VERSION = "1.0.0"

# 데이터베이스 설정
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'volunteer.db')

# 관리자 암호
ADMIN_PASSWORD = "admin123"  # 실제 운영 시 변경 필요

# UI 설정
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_TITLE = APP_NAME

# 봉사처 목록 (초기 데이터)
INITIAL_LOCATIONS = [
    "본관 1층",
    "암센터",
    "본관 4층",
    "병리팀",
    "국제진료센터",
    "농협 암센터",
    "농협 본관 1층"
]

# 세션 정보
current_session = {
    'volunteer_id': None,
    'volunteer_name': None,
    'volunteer_phone': None,
    'check_in_time': None,
    'location_id': None,
    'is_admin': False
}
