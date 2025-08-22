# 🎯 Multimodal Content Discovery Platform

A Django-based web application that enables users to search, bookmark, and receive recommendations for multimedia content. Currently implemented with anime (Jikan API) and books (OpenLibrary API).

## ✨ Features

### 🔐 User Authentication
- User registration and login
- Secure session management
- User roles (User/Administrator)
- Django admin panel

### 🔍 Content Search
- **Anime**: Search integration with Jikan API (MyAnimeList)
- **Books**: Search integration with OpenLibrary API
- Results with images, synopsis, ratings, and details
- Safe content filtering (SFW for anime)

### ⭐ Unified Favorites System
- Mark/unmark both anime and books as favorites
- Personal favorites list per user with content type indicators
- Automatic duplicate prevention
- Support for both anime and book metadata

### 🎯 Intelligent Recommendations
- **Anime Recommendations**: Based on user's favorite anime using Jikan API
- **Book Recommendations**: Based on favorite authors from user's book library
- Avoids suggesting already bookmarked content
- Rate limiting for external API calls

### 🌍 Multi-language Support (Experimental)
- Initial implementation of internationalization (i18n)
- Support for Spanish, English, French, German, and Portuguese
- *Note: Multi-language feature is in early development*

## 🏗️ Architecture

### Tech Stack
- **Backend**: Django 4.2+, PostgreSQL
- **Frontend**: Bootstrap 5, Font Awesome
- **APIs**: Jikan (MyAnimeList), OpenLibrary
- **Containerization**: Docker + Docker Compose
- **Internationalization**: Django i18n framework

### Project Structure
```
multimodal-recommendation-system/
├── app/
│   ├── models.py          # User, Favorite models (supports anime & books)
│   ├── views.py           # Search and recommendation logic for both content types
│   ├── forms.py           # User and search forms
│   ├── templates/         # Bootstrap HTML templates with i18n tags
│   └── migrations/        # Database migrations
├── locale/               # Translation files (experimental)
├── docker-compose.yml    # Services configuration
├── Dockerfile           # Application image with gettext support
├── requirements.txt     # Python dependencies
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Docker and Docker Compose installed
- Port 8080 available

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/multimodal-recommendation-system.git
   cd multimodal-recommendation-system
   ```

2. **Start with Docker**
   ```bash
   docker-compose build
   docker-compose up -d
   docker-compose run web python manage.py migrate
   ```

3. **Access the application**
   - Application: http://localhost:8080
   - Admin: http://localhost:8080/admin

## 📱 How to Use

1. **Register** an account or login
2. **Search** for anime or books by title/keywords
3. **Add to favorites** content you like (anime or books)
4. **Get recommendations** based on your favorites for both content types
5. **Manage** your unified favorites list
6. **Try language switching** (experimental feature in navbar)

## 🔧 Development Commands

```bash
# View logs
docker-compose logs web

# Access Django shell
docker-compose exec web python manage.py shell

# Compile translations (for i18n)
docker-compose exec web python manage.py compilemessages

# Stop/start services
docker-compose down
docker-compose up -d

# Django commands
docker-compose run web python manage.py [command]

# Create superuser
docker-compose run web python manage.py createsuperuser
```

## 🛠️ Current Implementation

## 🔧 Current Implementation

- **Anime search** via Jikan API (MyAnimeList database)
- **Book search** via OpenLibrary API with author information
- **PostgreSQL** for user data and unified favorites storage
- **Bootstrap 5** responsive UI with custom styling
- **Session-based** user authentication
- **Docker containerization** for easy deployment
- **Basic i18n framework** (experimental multi-language support)

## 🚧 Known Limitations

- **Multi-language feature** is in early development - translations may not work consistently
- **Book recommendations** are basic (author-based only)
- **API rate limiting** may cause delays during heavy usage

## 🌟 Future Improvements

### 🎯 Core Features
- Enhanced recommendation algorithms
- Better multi-language implementation
- Advanced search filters
- User reviews and ratings

### 📺 Additional Content Types (Planned)
- Movies & TV Shows (TVmaze API)
- Music albums and artists
- Podcasts and audiobooks

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Implement your changes
4. Test with Docker
5. Submit a Pull Request

### Areas for Contribution
- Fix i18n implementation
- Improve recommendation algorithms
- UI/UX improvements
- Unit tests
- Performance optimization
- New API integrations

## 📄 License

This project is licensed under the MIT License.

## 🌟 Planned Expansions

### 📺 Movies & TV Shows
- Integration with TVmaze API
- Search by title, genre, year

### 📚 Books  
- OpenLibrary API integration
- Search by author, title, ISBN

### 🎵 Music (Future)
- Music database APIs
- Artist and album search

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/new-api`)
3. Implement your changes
4. Test with Docker
5. Submit a Pull Request

### Areas for Contribution
- New API integrations (TVmaze, OpenLibrary)
- UI/UX improvements
- Better recommendation algorithms
- Unit tests
- Performance optimization

## 📄 License

This project is licensed under the MIT License.

## 🔗 Origin

Based on the Django skeleton from [HolaDjango](https://github.com/gabrielhuav/HolaDjango/tree/6cv4)

---

*A simple yet expandable content discovery platform built with Django and Docker.*