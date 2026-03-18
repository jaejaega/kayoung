"""
신규 등록 페이지
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QRadioButton, QButtonGroup, QDateEdit, QPushButton
from PyQt6.QtCore import Qt, QDate, QTimer
from PyQt6.QtGui import QFont
from business.volunteer_service import VolunteerService


class RegisterPage(QWidget):
    """신규 등록 페이지"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.service = VolunteerService()
        self.init_ui()

    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        # 제목
        title = QLabel("자원봉사자 신규 등록")
        title.setObjectName("title")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 이름
        name_layout = QHBoxLayout()
        name_label = QLabel("이름:")
        name_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        name_label.setMinimumWidth(100)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("홍길동")
        self.name_input.setMinimumHeight(35)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # 성별
        gender_layout = QHBoxLayout()
        gender_label = QLabel("성별:")
        gender_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        gender_label.setMinimumWidth(100)
        gender_layout.addWidget(gender_label)

        self.gender_group = QButtonGroup()
        self.gender_male = QRadioButton("남")
        self.gender_male.setFont(QFont("Arial", 11))
        self.gender_female = QRadioButton("여")
        self.gender_female.setFont(QFont("Arial", 11))
        self.gender_group.addButton(self.gender_male, 0)
        self.gender_group.addButton(self.gender_female, 1)
        self.gender_male.setChecked(True)

        gender_layout.addWidget(self.gender_male)
        gender_layout.addWidget(self.gender_female)
        gender_layout.addStretch()

        layout.addLayout(gender_layout)

        # 생년월일
        birth_layout = QHBoxLayout()
        birth_label = QLabel("생년월일:")
        birth_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        birth_label.setMinimumWidth(100)
        self.birth_input = QDateEdit()
        self.birth_input.setDate(QDate(1990, 1, 1))
        self.birth_input.setMinimumHeight(35)
        self.birth_input.setCalendarPopup(True)
        birth_layout.addWidget(birth_label)
        birth_layout.addWidget(self.birth_input)
        birth_layout.addStretch()
        layout.addLayout(birth_layout)

        # 소속
        org_layout = QHBoxLayout()
        org_label = QLabel("소속:")
        org_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        org_label.setMinimumWidth(100)
        self.org_input = QLineEdit()
        self.org_input.setPlaceholderText("예: 회사명")
        self.org_input.setMinimumHeight(35)
        org_layout.addWidget(org_label)
        org_layout.addWidget(self.org_input)
        layout.addLayout(org_layout)

        # 핸드폰번호
        phone_layout = QHBoxLayout()
        phone_label = QLabel("핸드폰번호:")
        phone_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        phone_label.setMinimumWidth(100)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("010-1234-5678")
        self.phone_input.setMinimumHeight(35)
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_input)
        layout.addLayout(phone_layout)

        # PIN 표시
        pin_layout = QHBoxLayout()
        pin_label = QLabel("PIN (뒷4자리):")
        pin_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        pin_label.setMinimumWidth(100)
        self.pin_display = QLineEdit()
        self.pin_display.setReadOnly(True)
        self.pin_display.setMinimumHeight(35)
        self.pin_display.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.pin_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_display.setPlaceholderText("자동 생성됨")
        pin_layout.addWidget(pin_label)
        pin_layout.addWidget(self.pin_display)
        layout.addLayout(pin_layout)

        # 메시지 라벨
        self.message_label = QLabel()
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setMinimumHeight(30)
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        register_btn = QPushButton("등록")
        register_btn.setMinimumHeight(50)
        register_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        register_btn.setObjectName("success")
        register_btn.clicked.connect(self.register)
        button_layout.addWidget(register_btn)

        clear_btn = QPushButton("초기화")
        clear_btn.setMinimumHeight(50)
        clear_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(clear_btn)

        layout.addLayout(button_layout)

        layout.addStretch()

        # 전화번호 입력 변화 감시
        self.phone_input.textChanged.connect(self.update_pin_preview)

    def update_pin_preview(self):
        """핸드폰 입력에 따라 PIN 미리보기 업데이트"""
        phone = self.phone_input.text().strip()
        parts = phone.split('-')

        if len(parts) == 3 and len(parts[2]) == 4:
            self.pin_display.setText(parts[2])
        else:
            self.pin_display.clear()

    def register(self):
        """신규 등록 처리"""
        name = self.name_input.text().strip()
        gender = 'M' if self.gender_male.isChecked() else 'F'
        birth_date = self.birth_input.date().toString('yyyy-MM-dd')
        organization = self.org_input.text().strip()
        phone = self.phone_input.text().strip()

        try:
            # 서비스에서 처리
            result = self.service.register_volunteer(name, gender, birth_date, organization, phone)

            # 성공 메시지
            self.show_success(result['message'])

            # 1초 후 폼 초기화
            QTimer.singleShot(1000, self.clear_form)

        except ValueError as e:
            self.show_error(str(e))
        except Exception as e:
            self.show_error(f"오류 발생: {str(e)}")

    def clear_form(self):
        """폼 초기화"""
        self.name_input.clear()
        self.gender_male.setChecked(True)
        self.birth_input.setDate(QDate(1990, 1, 1))
        self.org_input.clear()
        self.phone_input.clear()
        self.pin_display.clear()
        self.message_label.setText("")
        self.name_input.setFocus()

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

    def showEvent(self, event):
        """페이지 표시 시 이벤트"""
        super().showEvent(event)
        self.clear_form()
