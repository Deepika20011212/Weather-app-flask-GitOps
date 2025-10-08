# 🌤️ Weather and Air Quality Check App

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey?logo=flask)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Containerized-Docker-blue?logo=docker)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Orchestrated_on-Kubernetes-326ce5?logo=kubernetes)](https://kubernetes.io/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-623CE4?logo=terraform)](https://www.terraform.io/)
[![ArgoCD](https://img.shields.io/badge/GitOps-ArgoCD-orange?logo=argo)](https://argo-cd.readthedocs.io/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=githubactions)](https://docs.github.com/en/actions)
[![AWS](https://img.shields.io/badge/Cloud-AWS-FF9900?logo=amazon-aws)](https://aws.amazon.com/)
[![Redis](https://img.shields.io/badge/Cache-Redis-DC382D?logo=redis)](https://redis.io/)
[![SonarQube](https://img.shields.io/badge/Code_Quality-SonarQube-4E9BCD?logo=sonarqube)](https://www.sonarqube.org/)
[![Trivy](https://img.shields.io/badge/Security-Scanned_with_Trivy-0F9D58?logo=aqua)](https://aquasecurity.github.io/trivy/)

The **Weather and Air Quality Check App** is a Python Flask-based microservices application that provides real-time weather and air quality information using the OpenWeather API. The project is built using a modern DevOps toolchain, containerized with Docker, orchestrated using Kubernetes (EKS), deployed via Argo CD using a GitOps model, and provisioned on AWS with Terraform. It also integrates a complete CI/CD pipeline using GitHub Actions that automates build, test, scan, and deployment processes.

The application consists of multiple microservices communicating via REST APIs: a frontend service (port 5000), a weather service (port 5001) that fetches weather details from the OpenWeather API, an air check service (port 5002) for air quality information, and a Redis caching service (port 6379) to enhance performance. The services are containerized using Docker and orchestrated locally with Docker Compose for development and testing.

The infrastructure is defined as code using Terraform, which provisions AWS components such as VPC, EKS Cluster, ECR (for image storage), and S3 (for Terraform remote state management). Deployment manifests are managed through Helm charts (Deployments, Services, and NGINX Ingress), and Argo CD is configured for automated GitOps-based synchronization between the GitHub repository and the Kubernetes cluster. A custom DNS mapping has been configured using a free domain name for external access.

The CI/CD pipeline is built using GitHub Actions with three main stages. The first stage handles build and test — installing dependencies, running tests, and performing static code analysis using SonarQube. The second stage performs image scanning using Trivy for vulnerabilities, builds Docker images, and pushes them to AWS ECR. The final stage updates Helm chart versions and triggers automatic deployment via Argo CD sync to the EKS cluster. This ensures a complete end-to-end continuous integration and deployment flow.

To run the application locally, clone the repository and use Docker Compose:

```bash
git clone https://github.com/Deepika20011212/Weather-app-flask-GitOps.git
cd Weather-app-flask-GitOps
docker-compose up --build
```
The frontend will be accessible at http://localhost:5000, the weather API at http://localhost:5001, the air check API at http://localhost:5002, and Redis at localhost:6379.

For Kubernetes deployment, ensure you have an EKS cluster and Helm installed. Navigate to the Helm chart directory and install or upgrade the release using:
cd helm/weather-air
helm upgrade --install weather-app .
kubectl get pods,svc,ingress

Terraform manages infrastructure creation:
cd terraform/
terraform init
terraform plan
terraform apply -auto-approve
🧠 Install Argo CD in EKS Cluster

Once your EKS cluster is ready, you can deploy Argo CD to manage continuous delivery via GitOps. Follow these steps:
# Step 1: Configure kubectl for EKS
aws eks update-kubeconfig --name <your-eks-cluster-name> --region <aws-region>

# Step 2: Create namespace for Argo CD
kubectl create namespace argocd

# Step 3: Add the Argo Helm repo
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

# Step 4: Install Argo CD using Helm
helm install argocd argo/argo-cd -n argocd

# Step 5: Verify installation
kubectl get pods -n argocd
Access the Argo CD UI at https://localhost:8080
.
Get the initial admin password:
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
You can then log in using username admin and the retrieved password, connect your GitHub repository, and enable automated sync to deploy the application via GitOps.

