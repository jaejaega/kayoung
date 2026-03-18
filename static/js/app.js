// 전역 상태
const state = {
    currentPage: 'login',
    isLoggedIn: false,
    isAdmin: false,
    volunteerId: null,
    volunteerName: '',
    checkedIn: false,
    currentRecordId: null,
    checkInTime: null,
    locations: [],
    volunteers: []
};

// 페이지 관리
function showPage(pageName) {
    document.querySelectorAll('.page').forEach(page => {
        page.style.display = 'none';
    });
    const page = document.getElementById(`${pageName}-page`);
    if (page) {
        page.style.display = 'block';
    }
    state.currentPage = pageName;
}

// API 호출 헬퍼
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(endpoint, options);
        if (response.status === 401) {
            logout();
            return null;
        }
        return await response.json();
    } catch (error) {
        console.error('API 오류:', error);
        showError('네트워크 오류가 발생했습니다.');
        return null;
    }
}

// 에러 표시
function showError(message) {
    const errorEl = document.getElementById('login-error');
    if (errorEl) {
        errorEl.textContent = message;
        errorEl.classList.add('show');
    }
}

// 로그인 페이지 이벤트
document.getElementById('login-btn').addEventListener('click', async () => {
    const pin = document.getElementById('pin').value.trim();
    const password = document.getElementById('password').value;

    if (!pin) {
        showError('PIN 번호를 입력하세요.');
        return;
    }

    const result = await apiCall('/api/auth/login', 'POST', {
        pin,
        password
    });

    if (!result) return;

    if (result.error) {
        showError(result.error);
        return;
    }

    if (result.success) {
        state.volunteerId = result.volunteer.id;
        state.volunteerName = result.volunteer.name;
        state.isLoggedIn = true;
        state.isAdmin = result.is_admin;

        document.getElementById('pin').value = '';
        document.getElementById('password').value = '';
        document.getElementById('login-error').classList.remove('show');

        if (state.isAdmin) {
            showPage('admin');
            initAdminPage();
        } else {
            showPage('user');
            initUserPage();
        }
    }
});

// 로그아웃
async function logout() {
    await apiCall('/api/auth/logout', 'POST');
    state.isLoggedIn = false;
    state.isAdmin = false;
    state.checkedIn = false;
    showPage('login');
}

document.getElementById('logout-btn').addEventListener('click', logout);
document.getElementById('admin-logout-btn').addEventListener('click', logout);

// 사용자 페이지 초기화
async function initUserPage() {
    document.getElementById('user-name').textContent = state.volunteerName;

    // 봉사처 로드
    const locations = await apiCall('/api/locations');
    if (locations) {
        state.locations = locations;
        const select = document.getElementById('location');
        select.innerHTML = '<option value="">봉사처를 선택하세요</option>';
        locations.forEach(loc => {
            const option = document.createElement('option');
            option.value = loc.id;
            option.textContent = loc.name;
            select.appendChild(option);
        });
    }

    // 오늘의 출퇴근 상태 확인
    await updateAttendanceStatus();

    // 통계 로드
    await loadStats();
}

// 출퇴근 상태 업데이트
async function updateAttendanceStatus() {
    const record = await apiCall('/api/attendance/today');

    if (record && record.check_in_time && !record.check_out_time) {
        state.checkedIn = true;
        state.currentRecordId = record.id;
        state.checkInTime = new Date(record.check_in_time);

        document.getElementById('status-text').textContent = '상태: 출근';
        document.getElementById('check-in-time').textContent =
            `출근 시간: ${formatTime(state.checkInTime)}`;
        document.getElementById('check-in-btn').disabled = true;
        document.getElementById('check-out-btn').disabled = false;

        // 경과 시간 업데이트
        startElapsedTimeUpdate();
    } else {
        state.checkedIn = false;
        document.getElementById('status-text').textContent = '상태: 퇴근';
        document.getElementById('check-in-time').textContent = '출근 시간: -';
        document.getElementById('elapsed-time').textContent = '경과 시간: -';
        document.getElementById('check-in-btn').disabled = false;
        document.getElementById('check-out-btn').disabled = true;
    }
}

// 경과 시간 업데이트
function startElapsedTimeUpdate() {
    setInterval(() => {
        if (state.checkedIn && state.checkInTime) {
            const elapsed = Math.floor((Date.now() - state.checkInTime) / 60000);
            const hours = Math.floor(elapsed / 60);
            const minutes = elapsed % 60;
            document.getElementById('elapsed-time').textContent =
                `경과 시간: ${hours}시간 ${minutes}분`;
        }
    }, 60000); // 1분마다 업데이트
}

// 출근
document.getElementById('check-in-btn').addEventListener('click', async () => {
    const locationId = document.getElementById('location').value;

    if (!locationId) {
        alert('봉사처를 선택하세요.');
        return;
    }

    const result = await apiCall('/api/attendance/check-in', 'POST', {
        location_id: parseInt(locationId)
    });

    if (result && result.success) {
        state.checkedIn = true;
        state.currentRecordId = result.record_id;
        state.checkInTime = new Date();

        alert('출근되었습니다.');
        await updateAttendanceStatus();
    }
});

// 퇴근
document.getElementById('check-out-btn').addEventListener('click', async () => {
    const notes = document.getElementById('notes').value;

    const result = await apiCall('/api/attendance/check-out', 'POST', {
        notes
    });

    if (result && result.success) {
        state.checkedIn = false;
        alert('퇴근되었습니다.');
        document.getElementById('notes').value = '';
        await updateAttendanceStatus();
        await loadStats();
    }
});

// 통계 로드
async function loadStats() {
    const stats = await apiCall('/api/attendance/stats');

    if (stats) {
        document.getElementById('visit-count').textContent = stats.visit_count || 0;
        const hours = Math.floor((stats.total_minutes || 0) / 60);
        const minutes = (stats.total_minutes || 0) % 60;
        document.getElementById('total-hours').textContent =
            `${hours}시간 ${minutes}분`;
        document.getElementById('last-visit').textContent =
            stats.last_visit ? formatDateTime(new Date(stats.last_visit)) : '-';
    }
}

// 관리자 페이지 초기화
async function initAdminPage() {
    // 탭 버튼 이벤트
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            e.target.classList.add('active');
            const tabName = e.target.dataset.tab;
            document.getElementById(`${tabName}-tab`).classList.add('active');
        });
    });

    // 자원봉사자 목록 로드
    await loadVolunteers();

    // 등록 폼
    document.getElementById('register-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await registerVolunteer();
    });
}

// 자원봉사자 목록 로드
async function loadVolunteers() {
    const volunteers = await apiCall('/api/volunteers');

    if (!volunteers) return;

    state.volunteers = volunteers;
    const tbody = document.getElementById('volunteers-tbody');
    tbody.innerHTML = '';

    volunteers.forEach(vol => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${vol.name}</td>
            <td>${vol.phone_number}</td>
            <td>${vol.organization}</td>
            <td>${formatDate(new Date(vol.registered_at))}</td>
            <td>${vol.is_active ? '활성' : '비활성'}</td>
        `;
        tbody.appendChild(row);
    });
}

// 자원봉사자 등록
async function registerVolunteer() {
    const genderValue = document.getElementById('reg-gender').value;
    const genderMap = { '남': 'M', '여': 'F' };

    const data = {
        name: document.getElementById('reg-name').value,
        gender: genderMap[genderValue] || genderValue,
        birth_date: document.getElementById('reg-birth').value,
        organization: document.getElementById('reg-organization').value,
        phone_number: document.getElementById('reg-phone').value
    };

    const result = await apiCall('/api/volunteers/register', 'POST', data);
    const messageEl = document.getElementById('register-message');

    if (result) {
        if (result.error) {
            messageEl.textContent = result.error;
            messageEl.classList.remove('success');
        } else if (result.success) {
            messageEl.textContent = '자원봉사자가 등록되었습니다.';
            messageEl.classList.add('success');
            document.getElementById('register-form').reset();
            setTimeout(() => {
                messageEl.textContent = '';
                messageEl.classList.remove('success');
            }, 3000);
            await loadVolunteers();
        }
    }

    messageEl.classList.add('show');
    setTimeout(() => {
        messageEl.classList.remove('show');
    }, 5000);
}

// 시간 포맷팅 헬퍼
function formatTime(date) {
    if (!date) return '-';
    return date.toLocaleTimeString('ko-KR', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatDate(date) {
    if (!date) return '-';
    return date.toLocaleDateString('ko-KR');
}

function formatDateTime(date) {
    if (!date) return '-';
    return date.toLocaleString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// 초기 로드
window.addEventListener('load', async () => {
    const sessionInfo = await apiCall('/api/session');

    if (sessionInfo && sessionInfo.logged_in) {
        state.volunteerId = sessionInfo.volunteer_id;
        state.volunteerName = sessionInfo.volunteer_name;
        state.isLoggedIn = true;
        state.isAdmin = sessionInfo.is_admin;

        if (state.isAdmin) {
            showPage('admin');
            initAdminPage();
        } else {
            showPage('user');
            initUserPage();
        }
    } else {
        showPage('login');
    }
});
