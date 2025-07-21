# Recipe Box - Docker Setup

This guide will help you set up the Recipe Box application using Docker with PostgreSQL database and MinIO for file storage.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (to clone the repository)

### 1. Automated Setup
```bash
# Make the setup script executable and run it
chmod +x setup-docker.sh
./setup-docker.sh
```

### 2. Manual Setup
If you prefer to set up manually:

```bash
# 1. Create environment file
cp .env.example .env

# 2. Build and start services
docker-compose up --build -d

# 3. Wait for services to be ready (about 30 seconds)
# 4. Initialize database
docker-compose exec recipe-backend python init_db.py
```

## 📊 Services Overview

| Service | Port | Description |
|---------|------|-------------|
| **PostgreSQL** | 5432 | Database server |
| **MinIO API** | 9000 | S3-compatible storage API |
| **MinIO Console** | 9001 | Web-based management console |
| **Backend API** | 8000 | FastAPI application |
| **Frontend** | 3000 | React application |

## 🔧 Configuration

### Environment Variables
The application uses the following environment variables (set in `.env`):

```bash
# Database
DATABASE_URL=postgresql://recipe_user:recipe_password@localhost:5432/recipe_box

# MinIO Storage
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123
MINIO_BUCKET=recipe-photos

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

### Database Credentials
- **Username**: `recipe_user`
- **Password**: `recipe_password`
- **Database**: `recipe_box`

### MinIO Credentials
- **Username**: `minioadmin`
- **Password**: `minioadmin123`

## 🗄️ Database Setup

### Initial Setup
The database is automatically initialized with:
- Recipes table schema
- Sample recipe data (Spaghetti Carbonara, Chicken Tikka Masala)

### Manual Database Operations

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U recipe_user -d recipe_box

# View tables
\dt

# View sample data
SELECT * FROM recipes;

# Exit PostgreSQL
\q
```

### Database Backup/Restore

```bash
# Create backup
docker-compose exec postgres pg_dump -U recipe_user recipe_box > backup.sql

# Restore from backup
docker-compose exec -T postgres psql -U recipe_user recipe_box < backup.sql
```

## 📁 MinIO Setup

### Access MinIO Console
1. Open http://localhost:9001
2. Login with `minioadmin` / `minioadmin123`
3. Create a bucket named `recipe-photos`

### MinIO Operations

```bash
# List buckets
docker-compose exec minio mc ls local

# Create bucket
docker-compose exec minio mc mb local/recipe-photos

# Upload file
docker-compose exec minio mc cp /path/to/file local/recipe-photos/
```

## 🛠️ Development

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs recipe-backend
docker-compose logs recipe-frontend

# Follow logs in real-time
docker-compose logs -f recipe-backend
```

### Restart Services
```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart recipe-backend
```

### Update Code
```bash
# Rebuild and restart after code changes
docker-compose up --build -d
```

### Access Services
```bash
# Access backend container
docker-compose exec recipe-backend bash

# Access frontend container
docker-compose exec recipe-frontend sh

# Access database
docker-compose exec postgres psql -U recipe_user -d recipe_box
```

## 🧪 Testing

### API Testing
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Health Checks
```bash
# Check all services
docker-compose ps

# Test API health
curl http://localhost:8000/

# Test database connection
docker-compose exec recipe-backend python -c "
from database import engine
with engine.connect() as conn:
    result = conn.execute('SELECT 1')
    print('Database connection successful')
"
```

## 🧹 Cleanup

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ This will delete all data)
docker-compose down -v
```

### Remove Everything
```bash
# Remove containers, networks, volumes, and images
docker-compose down -v --rmi all
```

## 🔍 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Check what's using the port
lsof -i :8000

# Kill the process or change the port in docker-compose.yml
```

**2. Database Connection Failed**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

**3. MinIO Not Accessible**
```bash
# Check MinIO status
docker-compose ps minio

# Check MinIO logs
docker-compose logs minio

# Restart MinIO
docker-compose restart minio
```

**4. Frontend Can't Connect to Backend**
- Ensure backend is running: `docker-compose ps recipe-backend`
- Check CORS configuration in backend
- Verify `REACT_APP_API_URL` in frontend environment

### Reset Everything
```bash
# Complete reset (⚠️ This will delete all data)
docker-compose down -v --rmi all
docker system prune -a
./setup-docker.sh
```

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MinIO Documentation](https://docs.min.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Contributing

When making changes:
1. Update the appropriate Dockerfile if needed
2. Test the changes with `docker-compose up --build`
3. Update this documentation if configuration changes
4. Ensure all services start correctly

---

**Happy Cooking! 🍳** 