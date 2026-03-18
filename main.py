"""
자원봉사자 출퇴근 관리 시스템 - Flask 웹앱
"""

from flask import Flask, render_template, jsonify, request, session
from functools import wraps
from datetime import datetime, timedelta
import os
from config import ADMIN_PASSWORD, current_session
from database.db_manager import DatabaseManager
from business.volunteer_service import VolunteerService
from business.attendance_service import AttendanceService

app = Flask(__name__)
app.secret_key = 'volunteer-system-secret-key-2024'

# 데이터베이스 및 비즈니스 로직 초기화
db = DatabaseManager()
volunteer_service = VolunteerService()
attendance_service = AttendanceService()


def login_required(f):
    """로그인 체크 데코레이터"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'volunteer_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@app.route('/api/auth/login', methods=['POST'])
def login():
    """로그인"""
    data = request.json
    pin = data.get('pin', '')
    password = data.get('password', '')
    is_admin = password == ADMIN_PASSWORD if password else False

    volunteer = db.get_volunteer_by_pin(pin)

    if not volunteer:
        return jsonify({'error': '존재하지 않는 PIN입니다.'}), 400

    session['volunteer_id'] = volunteer['id']
    session['volunteer_name'] = volunteer['name']
    session['volunteer_phone'] = volunteer['phone_number']
    session['is_admin'] = is_admin

    return jsonify({
        'success': True,
        'volunteer': volunteer,
        'is_admin': is_admin
    })


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """로그아웃"""
    session.clear()
    return jsonify({'success': True})


@app.route('/api/attendance/check-in', methods=['POST'])
@login_required
def check_in():
    """출근"""
    data = request.json
    volunteer_id = session.get('volunteer_id')
    location_id = data.get('location_id')

    if not location_id:
        return jsonify({'error': '봉사처를 선택해주세요.'}), 400

    try:
        result = attendance_service.check_in(volunteer_id, location_id)
        return jsonify({
            'success': True,
            'record_id': result['record_id'],
            'check_in_time': result['check_in_time']
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/attendance/check-out', methods=['POST'])
@login_required
def check_out():
    """퇴근"""
    volunteer_id = session.get('volunteer_id')
    data = request.json
    notes = data.get('notes', '')

    try:
        result = attendance_service.check_out(volunteer_id)
        # 필요시 notes를 데이터베이스에 저장
        if notes:
            db.update_attendance_record(result['record_id'], notes=notes)
        return jsonify({'success': True})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/attendance/today', methods=['GET'])
@login_required
def get_today_attendance():
    """오늘의 출퇴근 기록"""
    volunteer_id = session.get('volunteer_id')
    record = db.get_todays_attendance(volunteer_id)

    return jsonify(record if record else {})


@app.route('/api/volunteers', methods=['GET'])
@login_required
def get_volunteers():
    """자원봉사자 목록 (관리자만)"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Forbidden'}), 403

    volunteers = db.get_all_volunteers()
    return jsonify(volunteers)


@app.route('/api/volunteers/register', methods=['POST'])
@login_required
def register_volunteer():
    """자원봉사자 등록 (관리자만)"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Forbidden'}), 403

    data = request.json
    try:
        result = volunteer_service.register_volunteer(
            name=data.get('name'),
            gender=data.get('gender'),
            birth_date=data.get('birth_date'),
            organization=data.get('organization'),
            phone_number=data.get('phone_number')
        )
        return jsonify({'success': True, 'volunteer_id': result['id'], 'pin': result['pin_number']})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/locations', methods=['GET'])
def get_locations():
    """봉사처 목록"""
    locations = db.get_all_locations()
    return jsonify(locations)


@app.route('/api/attendance/stats', methods=['GET'])
@login_required
def get_stats():
    """출퇴근 통계"""
    volunteer_id = session.get('volunteer_id')
    stats = db.get_volunteer_stats(volunteer_id)

    return jsonify(stats if stats else {
        'visit_count': 0,
        'total_minutes': 0,
        'last_visit': None
    })


@app.route('/api/session', methods=['GET'])
def get_session_info():
    """현재 세션 정보"""
    return jsonify({
        'logged_in': 'volunteer_id' in session,
        'volunteer_id': session.get('volunteer_id'),
        'volunteer_name': session.get('volunteer_name'),
        'is_admin': session.get('is_admin', False)
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
