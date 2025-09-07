# Resume Roast 🍖

> An AI-powered resume feedback system that gives you honest, humorous feedback on your resume using scalable RAG (Retrieval-Augmented Generation) technology.

## 🎥 Demo

[![Watch Demo ↗](https://ik.imagekit.io/5wegcvcxp/Resume-ResumeRoast/ResumeRoast-Thumbnail.png?updatedAt=1757272540003)](https://ik.imagekit.io/5wegcvcxp/Resume-ResumeRoast/ResumeRoast-DemoVideo.mov/ik-video.mp4?updatedAt=1757271720473)

**Resume used in the video:** [Check here ↗](https://drive.google.com/file/d/1_jqvRGyrVAbpvjsjW9YJ2wFI6kYQZPtU/view?usp=sharing)

> **Note:** Text-to-speech is powered by Puter.js (free API that may occasionally have connectivity issues)

## ✨ Features

- 📄 **Upload Resume** - Support for PDF files
- 🤖 **AI Feedback** - Honest, humorous resume analysis
- ⚡ **Fast Processing** - Redis queue for instant responses
- 🔄 **Auto-scaling** - Handles high traffic with multiple workers
- 🎯 **RAG Technology** - Context-aware feedback generation

## 🏗️ Architecture

#### Problem with Traditional RAG

![Traditional RAG Issues](https://ik.imagekit.io/5wegcvcxp/Resume-ResumeRoast/Problem.png?updatedAt=1757268603074)

#### Our Solution with Redis Queue

![Redis Queue Solution](https://ik.imagekit.io/5wegcvcxp/Resume-ResumeRoast/Solution.png?updatedAt=1757268602820)

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API Key

### Setup

1. Create `.env` file in `resumeRoast-backend/` based on `.env.local`
2. Add your OpenAI API key to the `.env` file

### Run the Application

```bash
# Start everything
sh start.sh

# Stop everything
sh stop.sh
```

### Access URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

## 🔧 Manual Setup

```bash
# Backend (API + Workers)
cd resumeRoast-backend
docker-compose up -d

# Frontend (Web App)
cd resumeRoast-frontend
docker-compose up -d
```

## 🛠️ Tech Stack

### Backend

- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **LangGraph** - RAG workflow orchestration
- **OpenAI** - AI model integration
- **MongoDB** - Document database
- **Valkey** - Redis-compatible in-memory store
- **RQ** - Redis Queue for background tasks
- **PDF2Image** - Resume processing

### Frontend & Infrastructure

- **Vite** - Using Vanilla Javascript with no additional library
- **Docker** - Containerization
- **Nginx** - Web server (production)
