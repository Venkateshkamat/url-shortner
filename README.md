# URL Shortener

A fast and simple URL shortener API built with FastAPI. Convert long URLs into short, shareable links with click tracking and analytics.

## Features

- **URL Shortening**: Convert long URLs into short 6-character codes
- **Click Analytics**: Track how many times each shortened URL has been accessed
- **Database Support**: SQLite (default) and PostgreSQL ready
- **Auto-generated API Docs**: Interactive Swagger UI and ReDoc
- **Tested**: Test suite with pytest

## Tech Stack

- **Framework**: FastAPI 0.128.0
- **Database**: SQLite (default), PostgreSQL support
- **ORM**: SQLAlchemy 2.0.45
- **Validation**: Pydantic 2.12.5
- **Testing**: pytest, httpx
- **Server**: Uvicorn

## Installation

### Prerequisites

- Python 3.9+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd url-shortner
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (optional)**
   
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=sqlite:///./test.db
   ```
   
   For PostgreSQL:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```

## Running the Application

### Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Production Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### 1. Shorten a URL

**POST** `/shorten`

Create a shortened URL from a long URL.

**Request Body:**
```json
{
  "original_url": "https://github.com/yourusername"
}
```

**Response:**
```json
{
  "short_code": "abc123"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/shorten" \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://github.com/yourusername"}'
```

### 2. Redirect to Original URL

**GET** `/{short_code}`

Redirects to the original URL and increments the click counter.

**Example:**
```bash
curl http://localhost:8000/abc123
# Redirects to the original URL
```

### 3. Get URL Statistics

**GET** `/stats/{short_code}`

Get detailed statistics for a shortened URL.

**Response:**
```json
{
  "id": 1,
  "original_url": "https://github.com/yourusername",
  "short_code": "abc123",
  "created_at": "2024-01-15T10:30:00",
  "expires_at": null,
  "clicks": 42
}
```

**Example:**
```bash
curl http://localhost:8000/stats/abc123
```

## Testing

Run the test suite:

```bash
pytest tests/test_urls.py -v
```

Run all tests:
```bash
pytest tests/ -v
```

The test suite includes:
- Database table creation/cleanup
- URL shortening functionality
- Response validation

## Project Structure

```
url-shortner/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   └── urls.py      # URL endpoints
│   │   └── router.py        # API router
│   ├── core/
│   │   └── config.py        # Configuration settings
│   ├── db/
│   │   ├── base.py         # SQLAlchemy base
│   │   ├── models.py       # Database models
│   │   └── session.py       # Database session
│   ├── schemas/
│   │   └── url.py          # Pydantic schemas
│   ├── services/
│   │   └── shortener.py    # Short code generation
│   └── main.py             # FastAPI application
├── tests/
│   ├── conftest.py         # Pytest configuration
│   └── test_urls.py        # Test cases
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Database Schema

### URLs Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| original_url | String | The original long URL |
| short_code | String | Unique 6-character short code |
| created_at | DateTime | Timestamp when created |
| expires_at | DateTime | Optional expiration date |
| clicks | Integer | Number of times accessed |

## Configuration

The application uses environment variables for configuration. Create a `.env` file:

```env
DATABASE_URL=sqlite:///./test.db
```

For PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Development

### Code Style

The project follows Python PEP 8 standards.

### Adding New Features

1. Create database models in `app/db/models.py`
2. Add Pydantic schemas in `app/schemas/`
3. Create routes in `app/api/routes/`
4. Register routes in `app/api/router.py`
5. Write tests in `tests/`

## License

See [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Future Improvements

- [ ] Custom short code support
- [ ] URL expiration functionality
- [ ] User authentication
- [ ] Bulk URL shortening
- [ ] QR code generation
- [ ] Rate limiting
- [ ] Docker deployment
- [ ] Frontend interface

## Support

For issues and questions, please open an issue on GitHub.
