# Cloud Task Manager

A containerized Flask application with an automated AWS CI/CD pipeline.

## What this project demonstrates

- Python and Flask application development
- Docker containerization
- GitHub Actions CI/CD
- Secure GitHub-to-AWS authentication using OIDC
- Amazon ECR image publishing
- Immutable Docker image tags for traceability and rollback
- ECR lifecycle policies for image cleanup and cost control

## CI/CD Pipeline

```text
Push to main
    ↓
GitHub Actions
    ↓
Python syntax check
    ↓
Docker image build
    ↓
GitHub OIDC authentication
    ↓
Amazon ECR login
    ↓
Push Docker image to ECR
Pull requests run the Python validation only. Pushes to the main branch run the full build-and-push workflow.
Security
This project does not store long-lived AWS access keys in GitHub.
GitHub Actions uses OpenID Connect (OIDC) to assume a dedicated AWS IAM role with short-lived credentials. The IAM role is restricted to:
- Repository: midhunpk40/cloud-task-manager
- Branch: main
- ECR repository: cloud-task-manager
Docker Images
Images are pushed to this private Amazon ECR repository:
007448416699.dkr.ecr.us-east-1.amazonaws.com/cloud-task-manager
Each successful build creates two tags:
- latest — points to the newest successful build
- Git commit SHA — immutable image version for traceability and rollback
Example:
cloud-task-manager:latest
cloud-task-manager:34a084978c01b8681ef4a9a61c7e574d3ec59896
ECR Lifecycle Policy
The ECR repository is configured to:
- Remove untagged images after 7 days
- Keep the 10 newest tagged images
This prevents unused Docker images from accumulating.
Project Structure
cloud-task-manager/
├── app.py
├── database.py
├── Dockerfile
└── .github/
    └── workflows/
        └── ci.yml
Current Status
✅ Flask application containerized
✅ Docker image stored in Amazon ECR
✅ GitHub Actions CI/CD pipeline working
✅ GitHub OIDC authentication configured
✅ No long-lived AWS credentials stored in GitHub
✅ ECR image cleanup policy configured  
ECS/Fargate deployment is intentionally not configured yet.
