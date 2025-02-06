# 🐳 Docker Deployment Guide

## 📌 Overview
Docker simplifies deployment by packaging the **Streamlit app** and its dependencies into a container. This ensures that the project runs consistently across different environments without requiring manual dependency installation.

---

## 🚀 How to Build and Run the Docker Container

### 1️⃣ **Build the Docker Image** 🏗️
Run the following command in the project root directory:
```bash
docker build -t spotify-etl .
```
✅ This will create a **Docker image** named spotify-etl.

### 2️⃣ **Run the Container** 🚀
```bash
docker run -p 8501:8501 spotify-etl
```
✅ This starts the Streamlit app inside a **Docker container**, accessible at http://localhost:8501

---

## 🔧 Customizing the Docker Setup

### 📌 **Passing Environment Variables** (e.g., Spotify API credentials)
To securely pass environment variables **without storing them in the container**, use:
```bash
docker run --env-file .env -p 8501:8501 spotify-etl
```
✅ This ensures **API keys remain private** while still being accessible inside the container.

### 📌 **Rebuilding the Image** (After Code Changes)
If you modify the project and need to update the container, rebuild the image:
```bash
docker build --no-cache -t spotify-etl .
```
---

## 🔹 Troubleshooting
### ❌ Port Already in Use?
If you get an error that **port 8501 is already in use**, stop any existing containers:
```bash
docker ps  # List running containers
docker stop <container_id>  # Stop the conflicting container
```
### ❌ Permission Issues?
If Docker commands require sudo, consider adding your user to the Docker group:
```bash
sudo usermod -aG docker $USERThen restart your session:bash
newgrp docker
```