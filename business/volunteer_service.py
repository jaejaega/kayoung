"""
자원봉사자 관련 비즈니스 로직
"""

import re
from datetime import datetime
from database.db_manager import DatabaseManager


class VolunteerService:
    """자원봉사자 관리 서비스"""

    def __init__(self):
        self.db = DatabaseManager()

    # ============ 유효성 검사 ============

    @staticmethod
    def validate_name(name):
        """이름 유효성 검사"""
        if not name or len(name.strip()) == 0:
            raise ValueError("이름을 입력해주세요.")
        if len(name.strip()) > 50:
            raise ValueError("이름은 50자 이내여야 합니다.")
        return True

    @staticmethod
    def validate_gender(gender):
        """성별 유효성 검사"""
        if gender not in ['M', 'F']:
            raise ValueError("성별을 선택해주세요.")
        return True

    @staticmethod
    def validate_birth_date(birth_date_str):
        """생년월일 유효성 검사 (YYYY-MM-DD)"""
        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
            today = datetime.now()
            if birth_date > today:
                raise ValueError("생년월일은 오늘보다 이전이어야 합니다.")
            return True
        except ValueError:
            raise ValueError("생년월일 형식이 올바르지 않습니다. (YYYY-MM-DD)")

    @staticmethod
    def validate_organization(organization):
        """소속 유효성 검사"""
        if not organization or len(organization.strip()) == 0:
            raise ValueError("소속을 입력해주세요.")
        if len(organization.strip()) > 100:
            raise ValueError("소속은 100자 이내여야 합니다.")
        return True

    @staticmethod
    def validate_phone(phone):
        """핸드폰번호 유효성 검사 (010-XXXX-XXXX)"""
        pattern = r'^01[0-9]-\d{3,4}-\d{4}$'
        if not re.match(pattern, phone):
            raise ValueError("핸드폰번호 형식이 올바르지 않습니다. (예: 010-1234-5678)")
        return True

    @staticmethod
    def validate_pin(pin_str):
        """PIN 유효성 검사 (4자리 숫자)"""
        pattern = r'^\d{4}$'
        if not re.match(pattern, pin_str):
            raise ValueError("PIN은 4자리 숫자여야 합니다.")
        return True

    # ============ PIN 생성 ============

    @staticmethod
    def extract_pin_from_phone(phone_number):
        """핸드폰번호에서 PIN 추출 (뒷4자리)"""
        # 010-1234-5678 형식에서 5678 추출
        parts = phone_number.split('-')
        if len(parts) == 3:
            return parts[2]  # 뒷4자리
        return None

    # ============ 자원봉사자 등록 ============

    def register_volunteer(self, name, gender, birth_date, organization, phone_number):
        """자원봉사자 신규 등록"""
        # 유효성 검사
        self.validate_name(name)
        self.validate_gender(gender)
        self.validate_birth_date(birth_date)
        self.validate_organization(organization)
        self.validate_phone(phone_number)

        # 중복 확인
        if self.db.check_phone_exists(phone_number):
            raise ValueError(f"'{phone_number}'은(는) 이미 등록된 번호입니다.")

        # PIN 생성
        pin_number = self.extract_pin_from_phone(phone_number)

        if not pin_number:
            raise ValueError("PIN 생성 실패")

        if self.db.check_pin_exists(pin_number):
            raise ValueError(f"PIN '{pin_number}'은(는) 이미 사용 중입니다.")

        # 데이터베이스에 저장
        volunteer_id = self.db.add_volunteer(
            name=name,
            gender=gender,
            birth_date=birth_date,
            organization=organization,
            phone_number=phone_number,
            pin_number=pin_number
        )

        return {
            'id': volunteer_id,
            'name': name,
            'pin_number': pin_number,
            'message': f"'{name}' 자원봉사자가 등록되었습니다.\nPIN: {pin_number}"
        }

    # ============ 자원봉사자 조회 ============

    def login_by_pin(self, pin_number):
        """PIN으로 로그인"""
        self.validate_pin(pin_number)

        volunteer = self.db.get_volunteer_by_pin(pin_number)

        if not volunteer:
            raise ValueError("등록되지 않은 번호입니다.")

        return volunteer

    def get_all_volunteers(self):
        """모든 자원봉사자 조회"""
        return self.db.get_all_volunteers()

    def get_volunteer_by_id(self, volunteer_id):
        """ID로 자원봉사자 조회"""
        volunteer = self.db.get_volunteer_by_id(volunteer_id)
        if not volunteer:
            raise ValueError("해당 자원봉사자를 찾을 수 없습니다.")
        return volunteer

    # ============ 자원봉사자 수정 ============

    def update_volunteer(self, volunteer_id, **kwargs):
        """자원봉사자 정보 수정"""
        volunteer = self.get_volunteer_by_id(volunteer_id)

        # 유효성 검사
        if 'name' in kwargs:
            self.validate_name(kwargs['name'])

        if 'gender' in kwargs:
            self.validate_gender(kwargs['gender'])

        if 'birth_date' in kwargs:
            self.validate_birth_date(kwargs['birth_date'])

        if 'organization' in kwargs:
            self.validate_organization(kwargs['organization'])

        if 'phone_number' in kwargs:
            self.validate_phone(kwargs['phone_number'])
            if self.db.check_phone_exists(kwargs['phone_number'], exclude_id=volunteer_id):
                raise ValueError(f"'{kwargs['phone_number']}'은(는) 이미 사용 중인 번호입니다.")

        self.db.update_volunteer(volunteer_id, **kwargs)

    # ============ 자원봉사자 삭제 ============

    def delete_volunteer(self, volunteer_id):
        """자원봉사자 삭제 (비활성화)"""
        self.get_volunteer_by_id(volunteer_id)  # 존재 확인
        self.db.delete_volunteer(volunteer_id)

    # ============ 통계 ============

    def get_volunteer_stats(self, volunteer_id, start_date=None, end_date=None):
        """자원봉사자 통계 조회"""
        self.get_volunteer_by_id(volunteer_id)  # 존재 확인
        return self.db.get_volunteer_stats(volunteer_id, start_date, end_date)
