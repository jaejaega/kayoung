"""
데이터베이스 테이블 정의 및 SQL 스키마
"""

# 자원봉사자 테이블 생성 SQL
CREATE_VOLUNTEERS_TABLE = """
CREATE TABLE IF NOT EXISTS volunteers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gender TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    organization TEXT NOT NULL,
    phone_number TEXT UNIQUE NOT NULL,
    pin_number TEXT UNIQUE NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER DEFAULT 1
);
"""

# 봉사처 테이블 생성 SQL
CREATE_LOCATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    address TEXT,
    phone TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# 출퇴근 기록 테이블 생성 SQL
CREATE_ATTENDANCE_RECORDS_TABLE = """
CREATE TABLE IF NOT EXISTS attendance_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    volunteer_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    check_in_time TIMESTAMP,
    check_out_time TIMESTAMP,
    duration_minutes INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (volunteer_id) REFERENCES volunteers(id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);
"""

# 인덱스 생성 SQL
CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_volunteer_pin ON volunteers(pin_number);",
    "CREATE INDEX IF NOT EXISTS idx_volunteer_phone ON volunteers(phone_number);",
    "CREATE INDEX IF NOT EXISTS idx_attendance_volunteer ON attendance_records(volunteer_id);",
    "CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance_records(check_in_time);",
    "CREATE INDEX IF NOT EXISTS idx_attendance_location ON attendance_records(location_id);"
]
