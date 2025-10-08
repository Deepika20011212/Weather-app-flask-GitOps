# 🌦️ Weather and Air Quality Check App

## Overview
A **Python Flask**-based microservices application that displays real-time **weather and air quality data** using the **OpenWeather API**.  
The project is containerized with **Docker**, orchestrated on **AWS EKS**, and deployed through a **GitOps workflow using Argo CD**.  
Infrastructure is provisioned using **Terraform**, and the CI/CD pipeline is implemented via **GitHub Actions**.

---

## 🧩 Tech Stack

**Language & Framework:** Python (Flask)  
**Services:**
- Frontend (Port: `5000`)
- Weather Service (Port: `5001`)
- Air Quality Service (Port: `5002`)
- Redis Cache (Port: `6379`)

**DevOps & Cloud:**
- Docker & Docker Compose  
- Kubernetes (AWS EKS)
- Terraform (VPC, ECR, EKS, S3 for tfstate)
- Helm (Deployments, Services, Ingress - NGINX)
- Argo CD (GitOps Deployment)
- GitHub Actions (CI/CD)
- AWS S3, ECR
- Trivy & SonarQube Integration

---

## 🏗️ Architecture Summary
1. **Flask microservices** fetch weather and air quality data from the OpenWeather API.  
2. **Redis** caches results for better performance.  
3. **Docker Compose** used for local setup.  
4. **Terraform** provisions AWS infra (VPC, EKS, ECR, S3).  
5. **Helm charts** deploy the app to EKS with **Ingress via NGINX**.  
6. **Argo CD** handles GitOps-style continuous delivery.  
7. **GitHub Actions** pipeline automates build, test, scan, push to ECR, and ArgoCD sync.  

---

## ⚙️ Local Setup
```bash
git clone https://github.com/Deepika20011212/Weather-app-flask-GitOps.git
cd Weather-app-flask-GitOps
docker-compose up --build
```
### Local URLs:

1.Frontend → http://localhost:500
2.Weather API → http://localhost:5001
3.Air Check API → http://localhost:5002
4.Redis → localhost:6379

## ☁️ Deploy on AWS EKS

1. Provision Infrastructure with Terraform
```
cd terraform/
terraform init
terraform apply
``` 
Creates:
-VPC
-EKS Cluster
-ECR Repository
-S3 Bucket (Terraform state)

2. Deploy Helm Chart
```
cd helm/weather-air
helm upgrade --install weather-app.
```
Check deployment:
```kubectl get pods,svc,ingress```
## 🚀 Install Argo CD on EKS
1.Create namespace
kubectl create namespace argocd

2.Add Helm repo & install Argo CD
```helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm install argocd argo/argo-cd -n argocd
```
# Verify pods
```kubectl get pods -n argocd```
Login: 
```kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d```
## 🔄 CI/CD Workflow (GitHub Actions)
Stages:
-Build & Test – Install dependencies, run pytest, perform SonarQube scan.
-Security Scan & Push – Trivy image scan, build and push image to ECR.
-Deploy – Update Helm values and trigger ArgoCD sync to EKS.
-Workflow file: .github/workflows/ci-cd.yml
