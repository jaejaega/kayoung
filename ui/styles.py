"""
QSS 스타일시트 정의
"""

MAIN_STYLESHEET = """
    QMainWindow {
        background-color: #f5f5f5;
    }

    QWidget {
        background-color: #f5f5f5;
    }

    /* 탭 위젯 */
    QTabWidget::pane {
        border: 1px solid #ddd;
    }

    QTabBar::tab {
        background-color: #e0e0e0;
        color: #333;
        padding: 8px 20px;
        border: 1px solid #ddd;
        border-bottom: none;
        font-size: 11pt;
    }

    QTabBar::tab:selected {
        background-color: #ffffff;
        color: #000;
        font-weight: bold;
    }

    QTabBar::tab:hover:!selected {
        background-color: #f0f0f0;
    }

    /* 라벨 */
    QLabel {
        color: #333;
        font-size: 11pt;
    }

    QLabel#title {
        font-size: 14pt;
        font-weight: bold;
        color: #1a73e8;
    }

    QLabel#subtitle {
        font-size: 12pt;
        font-weight: bold;
        color: #555;
    }

    QLabel#info {
        color: #666;
        font-size: 10pt;
    }

    QLabel#success {
        color: #0d5f0d;
        font-weight: bold;
    }

    QLabel#error {
        color: #d32f2f;
        font-weight: bold;
    }

    /* 입력 필드 */
    QLineEdit {
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 8px;
        background-color: #fff;
        color: #333;
        font-size: 11pt;
    }

    QLineEdit:focus {
        border: 2px solid #1a73e8;
        background-color: #f9f9f9;
    }

    QLineEdit:disabled {
        background-color: #f0f0f0;
        color: #999;
    }

    /* 텍스트 편집 */
    QTextEdit {
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 8px;
        background-color: #fff;
        color: #333;
        font-size: 11pt;
    }

    QTextEdit:focus {
        border: 2px solid #1a73e8;
    }

    /* 콤보박스 */
    QComboBox {
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 6px;
        background-color: #fff;
        color: #333;
        font-size: 11pt;
    }

    QComboBox:focus {
        border: 2px solid #1a73e8;
    }

    QComboBox::drop-down {
        border: none;
        background-color: #fff;
    }

    QComboBox::drop-down:on {
        top: 1px;
        left: 1px;
    }

    QComboBox QAbstractItemView {
        border: 1px solid #ddd;
        background-color: #fff;
        selection-background-color: #1a73e8;
        color: #333;
    }

    /* 날짜 선택 */
    QDateEdit {
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 6px;
        background-color: #fff;
        color: #333;
        font-size: 11pt;
    }

    QDateEdit:focus {
        border: 2px solid #1a73e8;
    }

    /* 스핀박스 */
    QSpinBox, QDoubleSpinBox {
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 6px;
        background-color: #fff;
        color: #333;
    }

    /* 버튼 */
    QPushButton {
        background-color: #1a73e8;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        font-size: 11pt;
        font-weight: bold;
        cursor: pointer;
    }

    QPushButton:hover {
        background-color: #1557b0;
    }

    QPushButton:pressed {
        background-color: #0d47a1;
    }

    QPushButton:disabled {
        background-color: #ccc;
        color: #999;
    }

    /* 버튼 변형 */
    QPushButton#primary {
        background-color: #1a73e8;
    }

    QPushButton#primary:hover {
        background-color: #1557b0;
    }

    QPushButton#success {
        background-color: #0d5f0d;
    }

    QPushButton#success:hover {
        background-color: #0a4a0a;
    }

    QPushButton#danger {
        background-color: #d32f2f;
    }

    QPushButton#danger:hover {
        background-color: #c62828;
    }

    QPushButton#warning {
        background-color: #f57c00;
    }

    QPushButton#warning:hover {
        background-color: #e65100;
    }

    /* 테이블 위젯 */
    QTableWidget {
        background-color: #fff;
        alternate-background-color: #f9f9f9;
        gridline-color: #e0e0e0;
        border: 1px solid #ddd;
        border-radius: 4px;
    }

    QTableWidget::item {
        padding: 6px;
        border: none;
    }

    QTableWidget::item:selected {
        background-color: #1a73e8;
        color: white;
    }

    QHeaderView::section {
        background-color: #366092;
        color: white;
        padding: 6px;
        border: 1px solid #ddd;
        font-weight: bold;
    }

    /* 스크롤바 */
    QScrollBar:vertical {
        background-color: #f5f5f5;
        width: 12px;
        margin: 0px 0px 0px 0px;
        border: 1px solid #ddd;
    }

    QScrollBar::handle:vertical {
        background-color: #999;
        border-radius: 6px;
        min-height: 20px;
    }

    QScrollBar::handle:vertical:hover {
        background-color: #666;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;
        border: none;
    }

    QScrollBar:horizontal {
        background-color: #f5f5f5;
        height: 12px;
        margin: 0px 0px 0px 0px;
        border: 1px solid #ddd;
    }

    QScrollBar::handle:horizontal {
        background-color: #999;
        border-radius: 6px;
        min-width: 20px;
    }

    QScrollBar::handle:horizontal:hover {
        background-color: #666;
    }

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        background: none;
        border: none;
    }

    /* 메시지 박스 */
    QMessageBox {
        background-color: #f5f5f5;
    }

    QMessageBox QLabel {
        color: #333;
    }

    /* 프레임 */
    QFrame {
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 4px;
    }

    QFrame#noBorder {
        border: none;
    }

    /* 대화상자 */
    QDialog {
        background-color: #f5f5f5;
    }

    /* 체크박스 */
    QCheckBox {
        color: #333;
        spacing: 5px;
    }

    QCheckBox::indicator {
        width: 18px;
        height: 18px;
    }

    QCheckBox::indicator:unchecked {
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 3px;
    }

    QCheckBox::indicator:checked {
        background-color: #1a73e8;
        border: 1px solid #1a73e8;
        border-radius: 3px;
    }

    /* 라디오버튼 */
    QRadioButton {
        color: #333;
        spacing: 5px;
    }

    QRadioButton::indicator {
        width: 18px;
        height: 18px;
    }

    QRadioButton::indicator:unchecked {
        background-color: #fff;
        border: 2px solid #ddd;
        border-radius: 9px;
    }

    QRadioButton::indicator:checked {
        background-color: #1a73e8;
        border: 2px solid #1a73e8;
        border-radius: 9px;
    }
"""
