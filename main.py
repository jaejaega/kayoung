"""
자원봉사자 출퇴근 관리 시스템 메인 프로그램
"""

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """메인 함수"""
    app = QApplication(sys.argv)

    # 메인 윈도우 생성 및 표시
    window = MainWindow()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
