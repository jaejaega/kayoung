# PC에서 클로드 코드(Claude Code) 사용하기

Claude Code는 터미널에서 동작하는 AI 코딩 도구입니다. 자연어 명령으로 코드 작성, 설명, git 작업 등을 수행할 수 있습니다.

---

## 사전 요구사항

- **OS**: macOS 10.15+, Linux (Ubuntu 20.04+/Debian 10+), Windows 10+
- **RAM**: 최소 4GB
- **계정**: Claude Pro ($20/월) 또는 Claude Max ($100/월) — 무료 플랜은 미지원
- **인터넷 연결** 필요

---

## 설치 방법

### macOS / Linux (권장)

터미널에서 아래 명령어 실행:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### Windows — PowerShell (네이티브)

PowerShell(관리자 권한 불필요)에서 실행:

```powershell
irm https://claude.ai/install.ps1 | iex
```

### Windows — WSL (고급 사용자 권장)

WSL(Windows Subsystem for Linux)을 사용하면 Linux 환경과 동일하게 사용 가능:

```powershell
# PowerShell (관리자 권한)에서 WSL 설치
wsl --install -d Ubuntu

# Ubuntu 터미널에서 Claude Code 설치
curl -fsSL https://claude.ai/install.sh | bash
```

### macOS — Homebrew (수동 업데이트 필요)

```bash
brew install claude-code
# 업데이트 시: brew upgrade claude-code
```

### npm (레거시, 비권장)

```bash
npm install -g @anthropic-ai/claude-code
```

> Node.js 18.0+ 필요. 네이티브 인스톨러 사용을 권장합니다.

---

## 설치 후 인증

처음 실행 시 브라우저가 열립니다. Claude Pro/Max 계정으로 로그인하거나, Anthropic Console API 키를 붙여넣으면 됩니다.

```bash
claude
```

---

## 데스크톱 앱 (GUI)

터미널 없이 GUI로 사용하고 싶다면 **Claude Code 데스크톱 앱**을 설치하세요. macOS와 Windows용을 제공합니다.

---

## PATH 문제 해결

설치 후 `claude` 명령어를 찾을 수 없다면, 터미널을 완전히 닫고 다시 열어보세요.

---

## 참고 링크

- [공식 문서](https://code.claude.com/docs)
- [GitHub 저장소](https://github.com/anthropics/claude-code)
- [설치 가이드 (Bannerbear)](https://www.bannerbear.com/blog/how-to-install-claude-code-terminal-ide-web-desktop-setup/)
- [Windows/Mac 설정 가이드 (Medium)](https://medium.com/@lvalics_37568/setting-up-claude-code-on-windows-macos-449eed161e10)
