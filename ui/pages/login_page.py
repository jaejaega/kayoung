"""
로그인 페이지
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIntValidator
from config import current_session
from business.volunteer_service import VolunteerService


class LoginPage(QWidget):
    """로그인 페이지"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.service = VolunteerService()
        self.init_ui()
        self.focus_timer = QTimer()
        self.focus_timer.timeout.connect(self.set_focus_to_pin)
        self.focus_timer.start(100)

    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # 제목
        title = QLabel("자원봉사자 로그인")
        title.setObjectName("title")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # PIN 입력 섹션
        pin_layout = QVBoxLayout()
        pin_label = QLabel("4자리 번호를 입력하세요")
        pin_label.setObjectName("subtitle")
        pin_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        pin_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pin_layout.addWidget(pin_label)

        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("예: 1234")
        self.pin_input.setMaxLength(4)
        self.pin_input.setValidator(QIntValidator(0, 9999))
        self.pin_input.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.setMinimumHeight(60)
        self.pin_input.returnPressed.connect(self.login)
        pin_layout.addWidget(self.pin_input)

        layout.addLayout(pin_layout)

        # 메시지 라벨
        self.message_label = QLabel()
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setMinimumHeight(30)
        layout.addWidget(self.message_label)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        login_btn = QPushButton("로그인")
        login_btn.setMinimumHeight(50)
        login_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        login_btn.setObjectName("success")
        login_btn.clicked.connect(self.login)
        button_layout.addWidget(login_btn)

        admin_btn = QPushButton("관리자")
        admin_btn.setMinimumHeight(50)
        admin_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        admin_btn.clicked.connect(self.admin_login)
        button_layout.addWidget(admin_btn)

        layout.addLayout(button_layout)

        layout.addStretch()

    def set_focus_to_pin(self):
        """PIN 입력 필드에 포커스 설정"""
        if self.pin_input and not self.pin_input.hasFocus():
            self.pin_input.setFocus()
        self.focus_timer.stop()

    def login(self):
        """로그인 처리"""
        pin = self.pin_input.text().strip()

        if not pin:
            self.show_error("4자리 번호를 입력해주세요.")
            return

        if len(pin) != 4:
            self.show_error("4자리 번호를 입력해주세요.")
            return

        try:
            volunteer = self.service.login_by_pin(pin)

            # 세션 저장
            current_session['volunteer_id'] = volunteer['id']
            current_session['volunteer_name'] = volunteer['name']
            current_session['volunteer_phone'] = volunteer['phone_number']
            current_session['is_admin'] = False

            # 출퇴근 페이지로 이동
            self.show_success(f"{volunteer['name']} 자원봉사자 로그인 성공!")

            # 0.5초 후 출퇴근 탭으로 이동
            QTimer.singleShot(500, lambda: self.main_window.switch_to_tab(1))

            # PIN 입력 필드 초기화
            QTimer.singleShot(600, lambda: self.clear_input())

        except ValueError as e:
            self.show_error(str(e))

    def admin_login(self):
        """관리자 로그인"""
        from config import ADMIN_PASSWORD
        password, ok = QMessageBox.getText(
            self,
            "관리자 로그인",
            "관리자 암호를 입력하세요:",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )

        if not ok:
            return

        if password == ADMIN_PASSWORD:
            current_session['is_admin'] = True
            current_session['volunteer_id'] = None
            current_session['volunteer_name'] = None
            self.main_window.switch_to_tab(3)
        else:
            self.show_error("암호가 올바르지 않습니다.")

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

    def clear_input(self):
        """입력 필드 초기화"""
        self.pin_input.clear()
        self.message_label.setText("")
        self.pin_input.setFocus()

    def showEvent(self, event):
        """페이지 표시 시 이벤트"""
        super().showEvent(event)
        self.clear_input()
        self.pin_input.setFocus()
