"""
메인 윈도우
"""

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtCore import Qt
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from ui.styles import MAIN_STYLESHEET
from ui.pages.login_page import LoginPage
from ui.pages.attendance_page import AttendancePage
from ui.pages.register_page import RegisterPage
from ui.pages.admin_page import AdminPage


class MainWindow(QMainWindow):
    """메인 윈도우 클래스"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """UI 초기화"""
        # 윈도우 설정
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)

        # 스타일시트 적용
        self.setStyleSheet(MAIN_STYLESHEET)

        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 레이아웃
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 탭 위젯
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # 페이지 생성
        self.login_page = LoginPage(self)
        self.attendance_page = AttendancePage(self)
        self.register_page = RegisterPage(self)
        self.admin_page = AdminPage(self)

        # 탭에 페이지 추가
        self.tabs.addTab(self.login_page, "로그인")
        self.tabs.addTab(self.attendance_page, "출퇴근")
        self.tabs.addTab(self.register_page, "신규등록")
        self.tabs.addTab(self.admin_page, "관리자")

        # 초기 탭 설정
        self.tabs.setCurrentIndex(0)

        # 윈도우 활성화
        self.show()

    def switch_to_tab(self, tab_index):
        """탭 전환"""
        self.tabs.setCurrentIndex(tab_index)

    def closeEvent(self, event):
        """윈도우 종료 이벤트"""
        event.accept()
