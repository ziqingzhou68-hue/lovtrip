# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability within LovTrip, please send an email to the project maintainers. All security vulnerabilities will be promptly addressed.

**Please do not report security vulnerabilities through public GitHub issues.**

### Process

1. **Do not disclose publicly** — Please do not file a public issue or discuss the vulnerability in public forums.
2. **Contact privately** — Send details to the project maintainers via private channel.
3. **Response time** — We aim to acknowledge reports within 48 hours and provide a timeline for a fix within 5 business days.

## API Key Security

LovTrip uses multiple third-party API services. Please follow these guidelines:

1. **Never commit API keys** — All keys must be stored in `.streamlit/secrets.toml` (local) or Streamlit Cloud Secrets (deployment).
2. **Use `.env.example`** — Copy `.env.example` to `.env` for local development, never commit the actual `.env` file.
3. **Rotate keys regularly** — If you suspect a key has been exposed, rotate it immediately.

### Keys Required

| Service | Environment Variable | How to Get |
|---------|---------------------|------------|
| LLM API | `OPENAI_API_KEY` | TokenHub / OpenAI Platform |
| Baidu Maps | `BAIDU_MAP_AK` | [Baidu Map Console](https://lbsyun.baidu.com/apiconsole/key) |
| Pexels Images | `PEXELS_API_KEY` | [Pexels API](https://www.pexels.com/api/) |

## Supported Versions

| Version | Supported |
|---------|-----------|
| 2.x (latest) | ✅ Active |
| 1.x | ❌ Deprecated |
