# Task Management SaaS - Showcase Projekt

Ein vollständiges Task-Management-SaaS-System, das moderne Software-Engineering-Praktiken demonstriert. Dieses Projekt wurde als Portfolio-Showcase entwickelt und zeigt Best Practices in Fullstack-Entwicklung mit Vue 3, TypeScript, FastAPI und Microservices-Architektur.

## 🏗️ Architektur-Übersicht

Das Projekt folgt einer **Clean Architecture** mit **Domain-Driven Design (DDD)** Prinzipien und ist als **Microservices-Architektur** aufgebaut.

### Projekt-Struktur

```
python-fast-api/
├── frontend/                    # Vue 3 + TypeScript Frontend
│   ├── src/
│   │   ├── domain/              # DDD Domain Models (TypeScript Interfaces)
│   │   ├── application/         # Use Cases & Pinia Stores
│   │   ├── infrastructure/      # API Clients, HTTP Services
│   │   └── presentation/         # Vue Components, Router
│   ├── tests/                   # Frontend Tests
│   └── Dockerfile
├── backend/                     # FastAPI Microservices
│   ├── services/
│   │   ├── user-service/        # User Management Service
│   │   │   ├── src/
│   │   │   │   ├── domain/      # DDD Domain Layer (Entities, Value Objects)
│   │   │   │   ├── application/ # Use Cases (Business Logic)
│   │   │   │   ├── infrastructure/ # Repositories, Database Models
│   │   │   │   └── api/         # FastAPI Routes
│   │   │   └── tests/           # Service Tests
│   │   ├── task-service/        # Task Management Service
│   │   └── notification-service/ # Notification Service
│   └── shared/                  # Shared Libraries (DTOs, Events, Database Utils)
├── docker-compose.yml           # Multi-Service Orchestration
└── README.md
```

### Architektur-Prinzipien

#### Clean Architecture / DDD
- **Domain Layer**: Enthält Geschäftslogik, Entities und Value Objects (unabhängig von Frameworks)
- **Application Layer**: Use Cases orchestrieren die Domain-Logik
- **Infrastructure Layer**: Implementiert technische Details (Datenbank, APIs)
- **Presentation Layer**: UI-Komponenten und Routing

#### SOLID Principles
- **Single Responsibility**: Jede Klasse/Modul hat eine klare Verantwortung
- **Open/Closed**: Erweiterbar durch Interfaces, nicht durch Modifikation
- **Liskov Substitution**: Repository-Interfaces können ausgetauscht werden
- **Interface Segregation**: Spezifische Interfaces statt monolithischer
- **Dependency Inversion**: Abhängigkeiten von Abstraktionen, nicht Implementierungen

#### Microservices
- **User Service**: Authentifizierung, Benutzerverwaltung
- **Task Service**: Task- und Projektverwaltung
- **Notification Service**: Benachrichtigungen mit WebSocket-Support

## 🚀 Technologie-Stack

### Frontend
- **Vue 3.4+** mit Composition API
- **TypeScript 5+** (strict mode)
- **Pinia** für State Management
- **Vue Router** für Navigation
- **Axios** für HTTP-Requests
- **TailwindCSS** für Styling
- **Vitest** für Testing

### Backend
- **FastAPI** für REST APIs
- **SQLAlchemy** für ORM
- **PostgreSQL** als Datenbank
- **Pydantic** für Datenvalidierung
- **JWT** für Authentication
- **WebSockets** für Real-time Notifications
- **pytest** für Testing

### DevOps
- **Docker** & **Docker Compose** für Containerisierung
- **GitHub Actions** für CI/CD
- **Nginx** für Frontend-Serving

## 📋 Voraussetzungen

- Docker & Docker Compose
- Node.js 20+ (für lokale Frontend-Entwicklung)
- Python 3.11+ (für lokale Backend-Entwicklung)
- PostgreSQL 15+ (optional, wenn nicht Docker verwendet)

## 🛠️ Setup & Installation

### Mit Docker (Empfohlen)

1. **Repository klonen**
```bash
git clone <repository-url>
cd python-fast-api
```

2. **Umgebungsvariablen setzen** (optional)
```bash
cp .env.example .env
# Bearbeiten Sie .env nach Bedarf
```

3. **Services starten**
```bash
docker-compose up -d
```

4. **Services sind verfügbar unter:**
   - Frontend: http://localhost:3000
   - User Service: http://localhost:8001
   - Task Service: http://localhost:8002
   - Notification Service: http://localhost:8003
   - PostgreSQL: localhost:5432

### Lokale Entwicklung

#### Backend Setup

1. **Virtual Environment erstellen**
```bash
cd backend/services/user-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Dependencies installieren**
```bash
pip install -r requirements.txt
```

3. **Umgebungsvariablen setzen**
```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/taskdb"
export SECRET_KEY="your-secret-key"
```

4. **Service starten**
```bash
cd src
uvicorn main:app --reload --port 8001
```

#### Frontend Setup

1. **Dependencies installieren**
```bash
cd frontend
npm install
```

2. **Development Server starten**
```bash
npm run dev
```

3. **Frontend ist verfügbar unter:** http://localhost:3000

## 🧪 Testing

### Backend Tests

```bash
cd backend/services/user-service
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## 📚 API-Dokumentation

Nach dem Start der Services ist die automatisch generierte API-Dokumentation verfügbar:

- **User Service**: http://localhost:8001/docs
- **Task Service**: http://localhost:8002/docs
- **Notification Service**: http://localhost:8003/docs

## 🔑 Features

### Implementiert
- ✅ User Management (Registrierung, Login, JWT Authentication)
- ✅ Task Management (CRUD, Status-Management, Prioritäten)
- ✅ Project Management (Projekte erstellen, Tasks zuordnen)
- ✅ Real-time Notifications (WebSocket)
- ✅ Responsive Design (Mobile-friendly)
- ✅ Clean Architecture / DDD
- ✅ Microservices-Architektur
- ✅ Docker-Containerisierung
- ✅ Unit Tests
- ✅ CI/CD Pipeline

### Architektur-Highlights
- **Domain-Driven Design**: Klare Trennung von Domain-Logik und Infrastruktur
- **Repository Pattern**: Abstraktion der Datenzugriffsschicht
- **Use Case Pattern**: Geschäftslogik in Use Cases gekapselt
- **Dependency Injection**: Lose Kopplung durch Interfaces
- **Type Safety**: TypeScript strict mode + Python type hints

## 🏛️ Code-Qualität

### TypeScript
- Strict mode aktiviert
- ESLint für Code-Qualität
- Type-safe API-Clients

### Python
- Type hints mit mypy
- Pydantic für Datenvalidierung
- Ruff für Linting (empfohlen)

## 📖 Verwendung

### 1. Benutzer registrieren
```bash
POST http://localhost:8001/api/v1/auth/register
{
  "email": "user@example.com",
  "full_name": "Max Mustermann",
  "password": "securepassword123"
}
```

### 2. Anmelden
```bash
POST http://localhost:8001/api/v1/auth/login
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### 3. Task erstellen
```bash
POST http://localhost:8002/api/v1/tasks
Authorization: Bearer <token>
{
  "title": "Neue Aufgabe",
  "description": "Beschreibung",
  "priority": "high"
}
```

## 🔧 Entwicklung

### Code-Struktur befolgen

**Backend:**
- Domain-Logik in `domain/`
- Use Cases in `application/`
- Datenbank-Zugriff in `infrastructure/`
- API-Routes in `api/`

**Frontend:**
- Domain-Models in `domain/`
- Use Cases in `application/`
- API-Clients in `infrastructure/`
- Vue-Components in `presentation/`

### Neue Features hinzufügen

1. Domain-Model definieren (Domain Layer)
2. Use Case implementieren (Application Layer)
3. Repository-Interface definieren (Domain Layer)
4. Repository implementieren (Infrastructure Layer)
5. API-Route erstellen (API Layer)
6. Tests schreiben

## 📝 Lizenz

Dieses Projekt wurde als Showcase für Portfolio-Zwecke erstellt.

## 👤 Autor

Erstellt als Portfolio-Showcase für Fullstack-Entwicklung mit Vue 3, TypeScript, FastAPI und Microservices-Architektur.

## 🙏 Danksagungen

Dieses Projekt demonstriert moderne Software-Engineering-Praktiken und Best Practices für:
- Clean Architecture
- Domain-Driven Design
- Microservices-Architektur
- SOLID Principles
- Test-Driven Development
- DevOps-Praktiken
