"""
관리자 페이지
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QFileDialog, QLineEdit, QTabWidget
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from datetime import datetime
from config import current_session
from business.volunteer_service import VolunteerService
from business.attendance_service import AttendanceService
from business.export_service import ExportService
from database.db_manager import DatabaseManager


class AdminPage(QWidget):
    """관리자 페이지"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.volunteer_service = VolunteerService()
        self.attendance_service = AttendanceService()
        self.export_service = ExportService()
        self.db = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # 제목
        title = QLabel("관리자 화면")
        title.setObjectName("title")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 탭 위젯
        tabs = QTabWidget()

        # 탭 1: 자원봉사자 관리
        volunteer_tab = self.create_volunteer_tab()
        tabs.addTab(volunteer_tab, "자원봉사자 관리")

        # 탭 2: 출퇴근 기록
        attendance_tab = self.create_attendance_tab()
        tabs.addTab(attendance_tab, "출퇴근 기록")

        # 탭 3: 통계
        stats_tab = self.create_stats_tab()
        tabs.addTab(stats_tab, "통계")

        layout.addWidget(tabs)

        # 로그아웃 버튼
        logout_btn = QPushButton("로그아웃")
        logout_btn.setMinimumHeight(40)
        logout_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

    def create_volunteer_tab(self):
        """자원봉사자 관리 탭 생성"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        # 검색 바
        search_layout = QHBoxLayout()
        search_label = QLabel("검색:")
        search_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.volunteer_search = QLineEdit()
        self.volunteer_search.setPlaceholderText("이름으로 검색...")
        self.volunteer_search.setMinimumHeight(35)
        self.volunteer_search.textChanged.connect(self.filter_volunteer_table)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.volunteer_search)

        layout.addLayout(search_layout)

        # 자원봉사자 테이블
        self.volunteer_table = QTableWidget()
        self.volunteer_table.setColumnCount(8)
        self.volunteer_table.setHorizontalHeaderLabels(
            ["이름", "성별", "생년월일", "소속", "핸드폰번호", "PIN", "등록일", "활성상태"]
        )
        self.volunteer_table.setMinimumHeight(400)
        self.volunteer_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.volunteer_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.volunteer_table.setColumnWidth(0, 80)
        self.volunteer_table.setColumnWidth(1, 60)
        self.volunteer_table.setColumnWidth(2, 100)
        self.volunteer_table.setColumnWidth(3, 120)
        self.volunteer_table.setColumnWidth(4, 120)
        self.volunteer_table.setColumnWidth(5, 60)
        self.volunteer_table.setColumnWidth(6, 100)
        self.volunteer_table.setColumnWidth(7, 80)

        layout.addWidget(self.volunteer_table)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        refresh_btn = QPushButton("새로고침")
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        refresh_btn.clicked.connect(self.load_volunteers)
        button_layout.addWidget(refresh_btn)

        delete_btn = QPushButton("삭제")
        delete_btn.setMinimumHeight(40)
        delete_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        delete_btn.setObjectName("danger")
        delete_btn.clicked.connect(self.delete_volunteer)
        button_layout.addWidget(delete_btn)

        export_btn = QPushButton("엑셀로 내보내기")
        export_btn.setMinimumHeight(40)
        export_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        export_btn.setObjectName("warning")
        export_btn.clicked.connect(self.export_volunteers)
        button_layout.addWidget(export_btn)

        layout.addLayout(button_layout)

        return widget

    def create_attendance_tab(self):
        """출퇴근 기록 탭 생성"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        info_label = QLabel("전체 출퇴근 기록")
        info_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(info_label)

        # 출퇴근 테이블
        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(6)
        self.attendance_table.setHorizontalHeaderLabels(
            ["자원봉사자", "봉사처", "출근시간", "퇴근시간", "봉사시간(분)", "날짜"]
        )
        self.attendance_table.setMinimumHeight(400)
        self.attendance_table.setColumnWidth(0, 100)
        self.attendance_table.setColumnWidth(1, 120)
        self.attendance_table.setColumnWidth(2, 100)
        self.attendance_table.setColumnWidth(3, 100)
        self.attendance_table.setColumnWidth(4, 100)
        self.attendance_table.setColumnWidth(5, 100)

        layout.addWidget(self.attendance_table)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        refresh_btn = QPushButton("새로고침")
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        refresh_btn.clicked.connect(self.load_attendance_records)
        button_layout.addWidget(refresh_btn)

        export_btn = QPushButton("엑셀로 내보내기")
        export_btn.setMinimumHeight(40)
        export_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        export_btn.setObjectName("warning")
        export_btn.clicked.connect(self.export_attendance)
        button_layout.addWidget(export_btn)

        layout.addLayout(button_layout)

        return widget

    def create_stats_tab(self):
        """통계 탭 생성"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        info_label = QLabel("자원봉사자별 통계")
        info_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(info_label)

        # 통계 테이블
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(5)
        self.stats_table.setHorizontalHeaderLabels(
            ["자원봉사자", "소속", "총 봉사시간", "최근 봉사일", "봉사 횟수"]
        )
        self.stats_table.setMinimumHeight(400)
        self.stats_table.setColumnWidth(0, 100)
        self.stats_table.setColumnWidth(1, 150)
        self.stats_table.setColumnWidth(2, 120)
        self.stats_table.setColumnWidth(3, 120)
        self.stats_table.setColumnWidth(4, 100)

        layout.addWidget(self.stats_table)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        refresh_btn = QPushButton("새로고침")
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        refresh_btn.clicked.connect(self.load_stats)
        button_layout.addWidget(refresh_btn)

        export_btn = QPushButton("통합 리포트 내보내기")
        export_btn.setMinimumHeight(40)
        export_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        export_btn.setObjectName("warning")
        export_btn.clicked.connect(self.export_comprehensive)
        button_layout.addWidget(export_btn)

        layout.addLayout(button_layout)

        return widget

    # ============ 자원봉사자 관리 ============

    def load_volunteers(self):
        """자원봉사자 목록 로드"""
        try:
            volunteers = self.volunteer_service.get_all_volunteers()
            self.volunteer_table.setRowCount(len(volunteers))

            for row, volunteer in enumerate(volunteers):
                self.volunteer_table.setItem(row, 0, QTableWidgetItem(volunteer['name']))
                gender = "남" if volunteer['gender'] == 'M' else "여"
                self.volunteer_table.setItem(row, 1, QTableWidgetItem(gender))
                self.volunteer_table.setItem(row, 2, QTableWidgetItem(volunteer['birth_date']))
                self.volunteer_table.setItem(row, 3, QTableWidgetItem(volunteer['organization']))
                self.volunteer_table.setItem(row, 4, QTableWidgetItem(volunteer['phone_number']))
                self.volunteer_table.setItem(row, 5, QTableWidgetItem(volunteer['pin_number']))
                self.volunteer_table.setItem(row, 6, QTableWidgetItem(volunteer['registered_at'][:10]))

                status = "활성" if volunteer['is_active'] else "비활성"
                status_item = QTableWidgetItem(status)
                if not volunteer['is_active']:
                    status_item.setBackground(QColor("#ffcccc"))
                self.volunteer_table.setItem(row, 7, status_item)

                # 데이터 저장
                for col in range(8):
                    item = self.volunteer_table.item(row, col)
                    item.setData(Qt.ItemDataRole.UserRole, volunteer['id'])

        except Exception as e:
            QMessageBox.critical(self, "오류", f"자원봉사자 로드 실패: {str(e)}")

    def filter_volunteer_table(self):
        """자원봉사자 테이블 필터링"""
        search_text = self.volunteer_search.text().lower()

        for row in range(self.volunteer_table.rowCount()):
            show = False
            for col in range(self.volunteer_table.columnCount() - 1):
                item = self.volunteer_table.item(row, col)
                if item and search_text in item.text().lower():
                    show = True
                    break

            self.volunteer_table.setRowHidden(row, not show)

    def delete_volunteer(self):
        """자원봉사자 삭제"""
        current_row = self.volunteer_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "경고", "삭제할 자원봉사자를 선택해주세요.")
            return

        name = self.volunteer_table.item(current_row, 0).text()
        reply = QMessageBox.question(
            self,
            "삭제 확인",
            f"'{name}'을(를) 삭제하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                volunteer_id = self.volunteer_table.item(current_row, 0).data(Qt.ItemDataRole.UserRole)
                self.volunteer_service.delete_volunteer(volunteer_id)
                QMessageBox.information(self, "성공", f"'{name}'이(가) 삭제되었습니다.")
                self.load_volunteers()
            except Exception as e:
                QMessageBox.critical(self, "오류", f"삭제 실패: {str(e)}")

    def export_volunteers(self):
        """자원봉사자 목록 엑셀 내보내기"""
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "파일 저장",
            f"자원봉사자_목록_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            "Excel Files (*.xlsx)"
        )

        if filepath:
            try:
                self.export_service.export_all_volunteers(filepath)
                QMessageBox.information(self, "성공", f"파일이 저장되었습니다.\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"내보내기 실패: {str(e)}")

    # ============ 출퇴근 기록 ============

    def load_attendance_records(self):
        """출퇴근 기록 로드"""
        try:
            records = self.attendance_service.get_attendance_records()
            self.attendance_table.setRowCount(len(records))

            for row, record in enumerate(records):
                volunteer = self.db.get_volunteer_by_id(record['volunteer_id'])
                self.attendance_table.setItem(row, 0, QTableWidgetItem(volunteer['name']))

                location = self.db.get_location_by_id(record['location_id'])
                self.attendance_table.setItem(row, 1, QTableWidgetItem(location['name']))

                check_in = self.attendance_service.format_time_short(record['check_in_time'])
                self.attendance_table.setItem(row, 2, QTableWidgetItem(check_in))

                check_out = self.attendance_service.format_time_short(record['check_out_time'])
                self.attendance_table.setItem(row, 3, QTableWidgetItem(check_out))

                duration = str(record['duration_minutes']) if record['duration_minutes'] else "-"
                self.attendance_table.setItem(row, 4, QTableWidgetItem(duration))

                date = record['check_in_time'][:10] if record['check_in_time'] else "-"
                self.attendance_table.setItem(row, 5, QTableWidgetItem(date))

        except Exception as e:
            QMessageBox.critical(self, "오류", f"출퇴근 기록 로드 실패: {str(e)}")

    def export_attendance(self):
        """출퇴근 기록 엑셀 내보내기"""
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "파일 저장",
            f"출퇴근_기록_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            "Excel Files (*.xlsx)"
        )

        if filepath:
            try:
                self.export_service.export_attendance_records(filepath)
                QMessageBox.information(self, "성공", f"파일이 저장되었습니다.\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"내보내기 실패: {str(e)}")

    # ============ 통계 ============

    def load_stats(self):
        """통계 로드"""
        try:
            volunteers = self.volunteer_service.get_all_volunteers()
            self.stats_table.setRowCount(len(volunteers))

            for row, volunteer in enumerate(volunteers):
                if not volunteer['is_active']:
                    continue

                self.stats_table.setItem(row, 0, QTableWidgetItem(volunteer['name']))
                self.stats_table.setItem(row, 1, QTableWidgetItem(volunteer['organization']))

                # 통계
                stats = self.volunteer_service.get_volunteer_stats(volunteer['id'])

                if stats:
                    hours = stats['total_minutes'] // 60
                    minutes = stats['total_minutes'] % 60
                    time_str = f"{hours}시간 {minutes}분"
                    self.stats_table.setItem(row, 2, QTableWidgetItem(time_str))

                    self.stats_table.setItem(row, 3, QTableWidgetItem(stats['last_visit'][:10] if stats['last_visit'] else "-"))
                    self.stats_table.setItem(row, 4, QTableWidgetItem(str(stats['visit_count'])))
                else:
                    self.stats_table.setItem(row, 2, QTableWidgetItem("0시간"))
                    self.stats_table.setItem(row, 3, QTableWidgetItem("-"))
                    self.stats_table.setItem(row, 4, QTableWidgetItem("0"))

        except Exception as e:
            QMessageBox.critical(self, "오류", f"통계 로드 실패: {str(e)}")

    def export_comprehensive(self):
        """통합 리포트 내보내기"""
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "파일 저장",
            f"통합_리포트_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            "Excel Files (*.xlsx)"
        )

        if filepath:
            try:
                self.export_service.export_comprehensive_report(filepath)
                QMessageBox.information(self, "성공", f"파일이 저장되었습니다.\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"내보내기 실패: {str(e)}")

    def logout(self):
        """로그아웃"""
        reply = QMessageBox.question(
            self,
            "로그아웃",
            "정말 로그아웃하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            current_session['is_admin'] = False
            self.main_window.switch_to_tab(0)

    def showEvent(self, event):
        """페이지 표시 시 이벤트"""
        super().showEvent(event)
        if current_session['is_admin']:
            self.load_volunteers()
            self.load_attendance_records()
            self.load_stats()
