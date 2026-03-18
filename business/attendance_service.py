"""
출퇴근 관련 비즈니스 로직
"""

from datetime import datetime, timedelta
from database.db_manager import DatabaseManager


class AttendanceService:
    """출퇴근 기록 관리 서비스"""

    def __init__(self):
        self.db = DatabaseManager()

    # ============ 출근 ============

    def check_in(self, volunteer_id, location_id):
        """출근 기록"""
        # 오늘 이미 출근했는지 확인
        todays_attendance = self.db.get_todays_attendance(volunteer_id)

        if todays_attendance and todays_attendance['check_out_time'] is None:
            raise ValueError("이미 출근하셨습니다. 먼저 퇴근해주세요.")

        # 출근 기록 추가
        check_in_time = datetime.now().isoformat()
        record_id = self.db.add_attendance_record(
            volunteer_id=volunteer_id,
            location_id=location_id,
            check_in_time=check_in_time,
            check_out_time=None,
            duration_minutes=None
        )

        return {
            'record_id': record_id,
            'check_in_time': check_in_time,
            'message': f"출근 시간이 기록되었습니다."
        }

    # ============ 퇴근 ============

    def check_out(self, volunteer_id):
        """퇴근 기록"""
        # 오늘 출근 기록 조회
        todays_attendance = self.db.get_todays_attendance(volunteer_id)

        if not todays_attendance:
            raise ValueError("출근 기록이 없습니다. 먼저 출근해주세요.")

        if todays_attendance['check_out_time'] is not None:
            raise ValueError("이미 퇴근하셨습니다.")

        # 퇴근 시간 계산
        check_in_time = datetime.fromisoformat(todays_attendance['check_in_time'])
        check_out_time = datetime.now()
        duration_minutes = int((check_out_time - check_in_time).total_seconds() / 60)

        # 퇴근 기록 업데이트
        self.db.update_attendance_record(
            todays_attendance['id'],
            check_out_time=check_out_time.isoformat(),
            duration_minutes=duration_minutes
        )

        return {
            'record_id': todays_attendance['id'],
            'check_out_time': check_out_time.isoformat(),
            'duration_minutes': duration_minutes,
            'duration_hours': round(duration_minutes / 60, 2),
            'message': f"퇴근 시간이 기록되었습니다.\n봉사시간: {self._format_duration(duration_minutes)}"
        }

    # ============ 기록 조회 ============

    def get_todays_attendance(self, volunteer_id):
        """오늘의 출퇴근 기록 조회"""
        return self.db.get_todays_attendance(volunteer_id)

    def get_attendance_records(self, volunteer_id=None, start_date=None, end_date=None):
        """출퇴근 기록 조회"""
        return self.db.get_attendance_records(volunteer_id, start_date, end_date)

    # ============ 유틸리티 ============

    @staticmethod
    def _format_duration(minutes):
        """분 단위를 시간:분 형식으로 변환"""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}시간 {mins}분"

    def format_time(self, iso_time_str):
        """ISO 형식 시간을 읽기 쉬운 형식으로 변환"""
        if not iso_time_str:
            return "-"
        try:
            dt = datetime.fromisoformat(iso_time_str)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return iso_time_str

    def format_time_short(self, iso_time_str):
        """ISO 형식 시간을 짧은 형식으로 변환 (시간:분)"""
        if not iso_time_str:
            return "-"
        try:
            dt = datetime.fromisoformat(iso_time_str)
            return dt.strftime('%H:%M')
        except:
            return iso_time_str

    # ============ 통계 ============

    def get_monthly_statistics(self, year, month):
        """월별 통계 조회"""
        start_date = f"{year}-{month:02d}-01"

        # 마지막 날짜 계산
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"

        records = self.db.get_attendance_records(start_date=start_date, end_date=end_date)

        # 자원봉사자별 통계
        stats = {}
        for record in records:
            if record['check_out_time'] is None:
                continue  # 아직 퇴근하지 않은 기록은 제외

            volunteer_id = record['volunteer_id']
            if volunteer_id not in stats:
                volunteer = self.db.get_volunteer_by_id(volunteer_id)
                stats[volunteer_id] = {
                    'name': volunteer['name'],
                    'total_minutes': 0,
                    'visit_count': 0
                }

            stats[volunteer_id]['total_minutes'] += record['duration_minutes'] or 0
            stats[volunteer_id]['visit_count'] += 1

        return stats

    def get_location_statistics(self, start_date=None, end_date=None):
        """장소별 통계 조회"""
        records = self.db.get_attendance_records(start_date=start_date, end_date=end_date)

        stats = {}
        for record in records:
            if record['check_out_time'] is None:
                continue

            location_id = record['location_id']
            if location_id not in stats:
                location = self.db.get_location_by_id(location_id)
                stats[location_id] = {
                    'name': location['name'],
                    'total_minutes': 0,
                    'visit_count': 0
                }

            stats[location_id]['total_minutes'] += record['duration_minutes'] or 0
            stats[location_id]['visit_count'] += 1

        return stats
