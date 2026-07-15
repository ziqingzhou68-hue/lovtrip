# Changelog

All notable changes to LovTrip will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] — 2025-07

### Added
- 🎨 Premium UI design with LovTrip visual theme
- 🗺️ Interactive Leaflet map (free, no API key needed)
- 🌤️ Real-time weather via Open-Meteo (free API)
- 🏨 Hotel recommendations via Baidu Maps API
- 🎯 Tourist spot discovery with photos
- 🍜 Local food & restaurant finder
- 📸 Pexels real travel photos integration
- 📥 Downloadable trip plan (TXT)
- 🎉 Celebration animation on plan completion
- 📱 Responsive design for mobile/desktop
- 🔧 Modular project structure (config/services/components)

### Changed
- Replaced Baidu Maps JS API with free Leaflet (no domain restrictions)
- Migrated from inline CSS to modular styles component
- Improved config management with env var fallback

### Security
- All API keys moved to environment variables
- `.env.example` template for configuration
- Enhanced `.gitignore` for sensitive files
- No keys in git history

## [1.0.0] — Initial Release

### Added
- AI-powered travel planning via LLM
- Basic Streamlit interface
- Baidu Maps integration for geocoding & POI search
- Weather information display
- Multi-city support
