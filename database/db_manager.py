"""
데이터베이스 관리 클래스
SQLite 데이터베이스 연결 및 기본 CRUD 작업 처리
"""

import sqlite3
import os
from datetime import datetime
from config import DB_PATH, INITIAL_LOCATIONS
from database.models import (
    CREATE_VOLUNTEERS_TABLE,
    CREATE_LOCATIONS_TABLE,
    CREATE_ATTENDANCE_RECORDS_TABLE,
    CREATE_INDEXES
)


class DatabaseManager:
    """SQLite 데이터베이스 관리 클래스"""

    def __init__(self):
        self.db_path = DB_PATH
        self._ensure_db_dir()
        self.init_database()

    def _ensure_db_dir(self):
        """데이터베이스 디렉토리 생성"""
        db_dir = os.path.dirname(self.db_path)
        os.makedirs(db_dir, exist_ok=True)

    def get_connection(self):
        """데이터베이스 연결 반환"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """데이터베이스 초기화 (테이블 생성)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # 테이블 생성
            cursor.execute(CREATE_VOLUNTEERS_TABLE)
            cursor.execute(CREATE_LOCATIONS_TABLE)
            cursor.execute(CREATE_ATTENDANCE_RECORDS_TABLE)

            # 인덱스 생성
            for index_sql in CREATE_INDEXES:
                cursor.execute(index_sql)

            conn.commit()

            # 초기 데이터 로드 (봉사처)
            self._load_initial_locations(cursor, conn)

        finally:
            conn.close()

    def _load_initial_locations(self, cursor, conn):
        """초기 봉사처 데이터 로드"""
        try:
            cursor.execute("SELECT COUNT(*) as count FROM locations")
            if cursor.fetchone()['count'] == 0:
                for location in INITIAL_LOCATIONS:
                    cursor.execute(
                        "INSERT INTO locations (name) VALUES (?)",
                        (location,)
                    )
                conn.commit()
        except sqlite3.IntegrityError:
            pass

    # ============ 자원봉사자 관련 메서드 ============

    def add_volunteer(self, name, gender, birth_date, organization, phone_number, pin_number):
        """자원봉사자 추가"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO volunteers (name, gender, birth_date, organization, phone_number, pin_number)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, gender, birth_date, organization, phone_number, pin_number))
            conn.commit()
            volunteer_id = cursor.lastrowid
            return volunteer_id
        except sqlite3.IntegrityError as e:
            raise ValueError(f"등록 실패: {str(e)}")
        finally:
            conn.close()

    def get_volunteer_by_pin(self, pin_number):
        """PIN으로 자원봉사자 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT * FROM volunteers WHERE pin_number = ? AND is_active = 1",
                (pin_number,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def get_all_volunteers(self):
        """모든 자원봉사자 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM volunteers ORDER BY registered_at DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_volunteer_by_id(self, volunteer_id):
        """ID로 자원봉사자 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM volunteers WHERE id = ?", (volunteer_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def update_volunteer(self, volunteer_id, **kwargs):
        """자원봉사자 정보 수정"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            allowed_fields = ['name', 'gender', 'birth_date', 'organization', 'phone_number']
            updates = {k: v for k, v in kwargs.items() if k in allowed_fields}

            if not updates:
                return

            updates['updated_at'] = datetime.now().isoformat()

            set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [volunteer_id]

            cursor.execute(f"UPDATE volunteers SET {set_clause} WHERE id = ?", values)
            conn.commit()
        finally:
            conn.close()

    def delete_volunteer(self, volunteer_id):
        """자원봉사자 삭제 (soft delete)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE volunteers SET is_active = 0 WHERE id = ?", (volunteer_id,))
            conn.commit()
        finally:
            conn.close()

    def check_phone_exists(self, phone_number, exclude_id=None):
        """핸드폰 번호 중복 확인"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            if exclude_id:
                cursor.execute(
                    "SELECT COUNT(*) as count FROM volunteers WHERE phone_number = ? AND id != ?",
                    (phone_number, exclude_id)
                )
            else:
                cursor.execute(
                    "SELECT COUNT(*) as count FROM volunteers WHERE phone_number = ?",
                    (phone_number,)
                )

            return cursor.fetchone()['count'] > 0
        finally:
            conn.close()

    def check_pin_exists(self, pin_number, exclude_id=None):
        """PIN 중복 확인"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            if exclude_id:
                cursor.execute(
                    "SELECT COUNT(*) as count FROM volunteers WHERE pin_number = ? AND id != ?",
                    (pin_number, exclude_id)
                )
            else:
                cursor.execute(
                    "SELECT COUNT(*) as count FROM volunteers WHERE pin_number = ?",
                    (pin_number,)
                )

            return cursor.fetchone()['count'] > 0
        finally:
            conn.close()

    # ============ 봉사처 관련 메서드 ============

    def get_all_locations(self):
        """모든 봉사처 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM locations ORDER BY name")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_location_by_id(self, location_id):
        """ID로 봉사처 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM locations WHERE id = ?", (location_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def add_location(self, name, address=None, phone=None, description=None):
        """봉사처 추가"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO locations (name, address, phone, description)
                VALUES (?, ?, ?, ?)
            """, (name, address, phone, description))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"'{name}'은(는) 이미 존재합니다.")
        finally:
            conn.close()

    # ============ 출퇴근 기록 관련 메서드 ============

    def add_attendance_record(self, volunteer_id, location_id, check_in_time, check_out_time=None, duration_minutes=None, notes=None):
        """출퇴근 기록 추가"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO attendance_records (volunteer_id, location_id, check_in_time, check_out_time, duration_minutes, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (volunteer_id, location_id, check_in_time, check_out_time, duration_minutes, notes))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def get_todays_attendance(self, volunteer_id):
        """오늘의 출퇴근 기록 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT * FROM attendance_records
                WHERE volunteer_id = ?
                AND DATE(check_in_time) = DATE('now', 'localtime')
                ORDER BY check_in_time DESC
                LIMIT 1
            """, (volunteer_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def update_attendance_record(self, record_id, **kwargs):
        """출퇴근 기록 수정"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            allowed_fields = ['check_out_time', 'duration_minutes', 'notes']
            updates = {k: v for k, v in kwargs.items() if k in allowed_fields}

            if not updates:
                return

            set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [record_id]

            cursor.execute(f"UPDATE attendance_records SET {set_clause} WHERE id = ?", values)
            conn.commit()
        finally:
            conn.close()

    def get_attendance_records(self, volunteer_id=None, start_date=None, end_date=None):
        """출퇴근 기록 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            query = "SELECT * FROM attendance_records WHERE 1=1"
            params = []

            if volunteer_id:
                query += " AND volunteer_id = ?"
                params.append(volunteer_id)

            if start_date:
                query += " AND DATE(check_in_time) >= ?"
                params.append(start_date)

            if end_date:
                query += " AND DATE(check_in_time) <= ?"
                params.append(end_date)

            query += " ORDER BY check_in_time DESC"

            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_volunteer_stats(self, volunteer_id, start_date=None, end_date=None):
        """자원봉사자 통계 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            query = """
                SELECT
                    COUNT(*) as visit_count,
                    COALESCE(SUM(duration_minutes), 0) as total_minutes,
                    MAX(check_in_time) as last_visit
                FROM attendance_records
                WHERE volunteer_id = ? AND check_out_time IS NOT NULL
            """
            params = [volunteer_id]

            if start_date:
                query += " AND DATE(check_in_time) >= ?"
                params.append(start_date)

            if end_date:
                query += " AND DATE(check_in_time) <= ?"
                params.append(end_date)

            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
