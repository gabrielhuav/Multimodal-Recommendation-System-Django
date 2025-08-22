# 🎯 Multimodal Recommendation System

A Django-based web application that enables users to search, bookmark, and receive personalized recommendations for multimedia content. Currently implemented with anime (Jikan API) and designed to expand to movies, books, and other content types.

## ✨ Features

### 🔐 Authentication System
- User registration and login
- Secure session management
- User roles (User/Administrator)
- Django admin panel

### 🔍 Content Search
- **Anime**: Integrated search with Jikan API (MyAnimeList)
- Results with images, synopsis, ratings, and details
- Safe content filtering (SFW)
- *Ready for*: Movies (TMDB), Books (OpenLibrary), Music (Spotify), etc.

### ⭐ Favorites System
- Mark/unmark content as favorite
- Personalized favorites list per user
- Automatic duplicate prevention

### 🎯 Smart Recommendations
- Recommendations based on user favorites
- Algorithm that avoids suggesting already bookmarked content
- Rate limiting for external APIs
- *Future*: Machine Learning for better recommendations

## 🏗️ Architecture

### Tech Stack
- **Backend**: Django 4.2+, PostgreSQL
- **Frontend**: Bootstrap 5, Font Awesome
- **APIs**: Jikan (MyAnimeList), ready for TMDB, OpenLibrary
- **Containerization**: Docker + Docker Compose

### Project Structure
```
multimodal-recommendation-system/
├── app/
│   ├── models.py          # User, Favorite models
│   ├── views.py           # Search and recommendation logic
│   ├── forms.py           # User and search forms
│   ├── templates/         # HTML templates with Bootstrap
│   └── migrations/        # Database migrations
├── docker-compose.yml     # Services configuration
├── Dockerfile            # Application image
├── requirements.txt      # Python dependencies
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Docker and Docker Compose installed
- Port 8080 available

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/multimodal-recommendation-system.git
   cd multimodal-recommendation-system
   ```

2. **Build containers**
   ```bash
   docker-compose build
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **Run migrations**
   ```bash
   docker-compose run web python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   docker-compose run web python manage.py createsuperuser
   ```

6. **Access the application**
   - Application: http://localhost:8080
   - Admin: http://localhost:8080/admin

## 📱 System Usage

### For Users
1. **Registration**: Create account with email and password
2. **Search**: Search anime by title or keywords
3. **Favorites**: Bookmark content of interest
4. **Recommendations**: Receive personalized suggestions

### For Developers
- **Admin Panel**: Complete management of users and favorites
- **API Ready**: Structure prepared for multiple APIs
- **Extensible**: Easy to add new content types

## 🔧 Useful Commands

```bash
# View application logs
docker-compose logs web

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Run Django commands
docker-compose run web python manage.py [command]

# Interactive shell
docker-compose run web python manage.py shell
```

## 🌟 Roadmap & Planned Expansions

### 📺 Movies & TV Shows
- TMDB (The Movie Database) integration
- Search by genre, year, director
- Trailers and detailed information

### 📚 Books
- OpenLibrary API integration
- Search by author, genre, ISBN
- Reviews and ratings

### 🎵 Music
- Spotify API integration
- Search artists, albums, playlists
- Genre-based recommendations

### 🧠 AI & Machine Learning
- Sentiment analysis on reviews
- Similar user clustering
- Advanced recommendation algorithms
- Natural language processing for better search

### 📊 Analytics & Metrics
- User statistics dashboard
- Content popularity metrics
- A/B testing for recommendation algorithms

## 🛡️ Security & Considerations

- Input validation on all forms
- Rate limiting for external APIs
- Secure sessions with configurable timeouts
- External API data sanitization
- Production-ready HTTPS support

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

### Areas Needing Contribution
- New API implementations (TMDB, OpenLibrary, Spotify)
- Recommendation algorithm improvements
- Unit and integration tests
- Performance optimization
- UI/UX improvements

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 📞 Contact & Support

- **Issues**: Report bugs or request features on GitHub Issues
- **Documentation**: Repository Wiki for detailed guides
- **API Docs**: Endpoint documentation at `/docs/` (coming soon)

---

*System developed with ❤️ using Django, PostgreSQL, and Docker. Ready to scale to multiple multimedia content types.*