"""
출퇴근 기록 페이지
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from config import current_session
from business.volunteer_service import VolunteerService
from business.attendance_service import AttendanceService
from database.db_manager import DatabaseManager


class AttendancePage(QWidget):
    """출퇴근 기록 페이지"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.volunteer_service = VolunteerService()
        self.attendance_service = AttendanceService()
        self.db = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # 제목
        title = QLabel("출퇴근 기록")
        title.setObjectName("title")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 사용자 정보
        self.user_info_label = QLabel()
        self.user_info_label.setObjectName("subtitle")
        self.user_info_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.user_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.user_info_label)

        # 봉사처 선택
        location_layout = QHBoxLayout()
        location_label = QLabel("봉사처 선택:")
        location_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        location_label.setMinimumWidth(100)
        location_layout.addWidget(location_label)

        self.location_combo = QComboBox()
        self.location_combo.setFont(QFont("Arial", 11))
        self.location_combo.setMinimumHeight(40)
        location_layout.addWidget(self.location_combo)

        layout.addLayout(location_layout)

        # 현황 정보
        self.status_label = QLabel()
        self.status_label.setFont(QFont("Arial", 11))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        self.check_in_btn = QPushButton("출근")
        self.check_in_btn.setMinimumHeight(60)
        self.check_in_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.check_in_btn.setObjectName("success")
        self.check_in_btn.clicked.connect(self.check_in)
        button_layout.addWidget(self.check_in_btn)

        self.check_out_btn = QPushButton("퇴근")
        self.check_out_btn.setMinimumHeight(60)
        self.check_out_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.check_out_btn.setObjectName("danger")
        self.check_out_btn.clicked.connect(self.check_out)
        button_layout.addWidget(self.check_out_btn)

        layout.addLayout(button_layout)

        # 메시지 라벨
        self.message_label = QLabel()
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setMinimumHeight(40)
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)

        # 로그아웃 버튼
        logout_btn = QPushButton("로그아웃")
        logout_btn.setMinimumHeight(40)
        logout_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

        layout.addStretch()

    def showEvent(self, event):
        """페이지 표시 시 이벤트"""
        super().showEvent(event)
        if current_session['volunteer_id']:
            self.load_volunteer_info()
            self.load_locations()
            self.update_status()

    def load_volunteer_info(self):
        """자원봉사자 정보 로드"""
        try:
            volunteer = self.volunteer_service.get_volunteer_by_id(current_session['volunteer_id'])
            self.user_info_label.setText(f"{volunteer['name']} 자원봉사자")
        except:
            self.user_info_label.setText("정보 로드 실패")

    def load_locations(self):
        """봉사처 목록 로드"""
        try:
            locations = self.db.get_all_locations()
            self.location_combo.clear()
            for location in locations:
                self.location_combo.addItem(location['name'], location['id'])
        except Exception as e:
            self.show_error(f"봉사처 로드 실패: {str(e)}")

    def update_status(self):
        """출퇴근 상태 업데이트"""
        try:
            attendance = self.attendance_service.get_todays_attendance(current_session['volunteer_id'])

            if not attendance:
                self.status_label.setText("오늘 아직 출근하지 않았습니다.")
                self.check_in_btn.setEnabled(True)
                self.check_out_btn.setEnabled(False)
            elif not attendance['check_out_time']:
                # 출근한 상태
                check_in_time = self.attendance_service.format_time_short(attendance['check_in_time'])
                self.status_label.setText(f"✓ {check_in_time}에 출근했습니다.")
                self.check_in_btn.setEnabled(False)
                self.check_out_btn.setEnabled(True)
            else:
                # 퇴근한 상태
                duration = self.attendance_service._format_duration(attendance['duration_minutes'])
                self.status_label.setText(f"✓ 오늘 봉사를 완료했습니다. ({duration})")
                self.check_in_btn.setEnabled(True)
                self.check_out_btn.setEnabled(False)
        except Exception as e:
            self.show_error(f"상태 조회 실패: {str(e)}")

    def check_in(self):
        """출근 처리"""
        if not self.location_combo.currentData():
            self.show_error("봉사처를 선택해주세요.")
            return

        try:
            result = self.attendance_service.check_in(
                volunteer_id=current_session['volunteer_id'],
                location_id=self.location_combo.currentData()
            )

            self.show_success(f"{result['message']}")

            # 상태 업데이트
            QTimer.singleShot(500, self.update_status)

        except ValueError as e:
            self.show_error(str(e))

    def check_out(self):
        """퇴근 처리"""
        try:
            result = self.attendance_service.check_out(
                volunteer_id=current_session['volunteer_id']
            )

            self.show_success(f"{result['message']}")

            # 상태 업데이트
            QTimer.singleShot(500, self.update_status)

        except ValueError as e:
            self.show_error(str(e))

    def logout(self):
        """로그아웃"""
        reply = QMessageBox.question(
            self,
            "로그아웃",
            "정말 로그아웃하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            current_session['volunteer_id'] = None
            current_session['volunteer_name'] = None
            current_session['volunteer_phone'] = None
            self.main_window.switch_to_tab(0)

    def show_success(self, message):
        """성공 메시지 표시"""
        self.message_label.setText(message)
        self.message_label.setObjectName("success")
        self.message_label.style().unpolish(self.message_label)
        self.message_label.style().polish(self.message_label)

    def show_error(self, message):
        """오류 메시지 표시"""
        self.message_label.setText(message)
        self.message_label.setObjectName("error")
        self.message_label.style().unpolish(self.message_label)
        self.message_label.style().polish(self.message_label)
