#!/bin/bash

echo "🚀 Setting up Recipe Box with Docker and PostgreSQL..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://recipe_user:recipe_password@localhost:5432/recipe_box

# MinIO Configuration
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123
MINIO_BUCKET=recipe-photos

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
EOF
    echo "✅ .env file created"
else
    echo "✅ .env file already exists"
fi

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Initialize database
echo "🗄️ Initializing database..."
docker-compose exec -T recipe-backend python init_db.py

# Check service status
echo "📊 Service status:"
docker-compose ps

echo ""
echo "🎉 Setup complete! Services are running:"
echo "   📊 PostgreSQL: localhost:5432"
echo "   🗄️  MinIO API: localhost:9000"
echo "   🖥️  MinIO Console: localhost:9001"
echo "   🔧 Backend API: localhost:8000"
echo "   🌐 Frontend: localhost:3000"
echo ""
echo "📖 Next steps:"
echo "   1. Open MinIO console at http://localhost:9001"
echo "      Login: minioadmin / minioadmin123"
echo "      Create bucket: recipe-photos"
echo "   2. Access the application at http://localhost:3000"
echo "   3. View API docs at http://localhost:8000/docs"
echo ""
echo "🛑 To stop services: docker-compose down"
echo "🔄 To restart: docker-compose up -d" 