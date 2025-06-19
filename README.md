# 🔧 HVAC AI Diagnostic

AI-powered diagnostic and troubleshooting application for HVAC systems that helps technicians quickly identify issues, predict maintenance needs, and optimize system performance.

## 🚀 Features

- **Smart Diagnostics**: AI-powered symptom analysis and equipment troubleshooting
- **Predictive Maintenance**: Machine learning algorithms predict equipment failures
- **Mobile-First Design**: Progressive Web App optimized for field technicians
- **Equipment Database**: Comprehensive HVAC equipment specifications and compatibility
- **Real-time Monitoring**: Live sensor data integration and anomaly detection
- **Maintenance Scheduling**: Automated service reminders and work order management
- **Energy Optimization**: AI recommendations for improving system efficiency

## 🛠️ Tech Stack

### Backend
- **Python 3.11+** with FastAPI
- **PostgreSQL** with TimescaleDB for time-series data
- **Redis** for caching and session management
- **Celery** for background task processing

### AI/ML
- **scikit-learn** for traditional ML algorithms
- **TensorFlow** for deep learning models
- **Pandas/NumPy** for data processing
- **Hugging Face** for pre-trained models

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **PWA** support for mobile devices
- **Redux Toolkit** for state management

### Infrastructure
- **Docker** for containerization
- **GitHub Actions** for CI/CD
- **AWS/Azure** for cloud deployment

## 📋 Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Docker & Docker Compose**
- **Git**

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/mundster53/hvac-ai-diagnostic.git
cd hvac-ai-diagnostic
```

### 2. Set Up Environment
```bash
# Copy environment variables
cp .env.example .env

# Start with Docker Compose
docker-compose up -d
```

### 3. Install Dependencies
```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies
cd src/frontend
npm install
```

### 4. Run Development Servers
```bash
# Backend (from root directory)
uvicorn src.backend.main:app --reload --port 8000

# Frontend (from src/frontend directory)
npm run dev
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
hvac-ai-diagnostic/
├── src/
│   ├── backend/          # FastAPI backend
│   ├── ai/              # Machine learning models
│   ├── frontend/        # React frontend
│   └── shared/          # Shared utilities
├── data/                # Training data and models
├── tests/               # Test suites
├── docs/                # Documentation
├── scripts/             # Utility scripts
└── deployment/          # Deployment configurations
```

## 🧪 Testing

```bash
# Run backend tests
pytest tests/

# Run frontend tests
cd src/frontend
npm test

# Run all tests
./scripts/test.sh
```

## 🐳 Docker Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📚 Documentation

- [API Reference](docs/api-reference.md)
- [User Guide](docs/user-guide.md)
- [Developer Guide](docs/developer-guide.md)
- [Deployment Guide](docs/deployment.md)
- [HVAC Specifications](docs/hvac-specifications/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/hvac-ai-diagnostic/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/hvac-ai-diagnostic/discussions)
- **Documentation**: [Project Wiki](https://github.com/yourusername/hvac-ai-diagnostic/wiki)

## 🎯 Roadmap

- [ ] Basic diagnostic engine
- [ ] Equipment database integration
- [ ] Mobile PWA deployment
- [ ] Real-time sensor integration
- [ ] Advanced ML models
- [ ] Multi-language support
- [ ] IoT device connectivity

---

**Built with ❤️ for HVAC professionals**