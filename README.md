# LLM-Based Internal Q&A System

## Project Overview

This project is developed as part of the **LinkAja AI Engineer Assessment** to build an internal Q&A chatbot. The chatbot leverages **Large Language Models (LLMs)** to extract relevant information from the **LinkAja FAQ database**, significantly enhancing internal knowledge accessibility and response efficiency.

### Deployment

🚀 **Live Service:** [LinkAja Internal Q&A Chatbot - Andrey Purwanto](http://a0882a19159c84b88b77c3f0811a93f5-2017565724.ap-southeast-1.elb.amazonaws.com)

⚠️ **Service Shutdown Date:** **11/02/2024** (for cost-saving purposes). If you encounter DNS resolution issues, try accessing it in incognito mode.

---

## System Architecture

The system is composed of multiple components designed for reliability, scalability, and accuracy:

1. **User Interface (Streamlit):** Provides an intuitive and interactive chat experience.
2. **API Layer (FastAPI):** Manages communication between the frontend and backend services.
3. **LLM Integration:** Utilizes **Retrieval-Augmented Generation (RAG) with ChromaDB** to retrieve contextually relevant data, then passes this context to an **LLM model using OpenAI and LangChain** for generating responses.
4. **Database (MySQL on AWS RDS):** Stores chat history, model interactions, and user feedback for continuous improvements.
5. **Deployment (AWS EKS):** Ensures high availability and scalability using Kubernetes for orchestration.

### Technology Stack

| Component        | Technology                              |
|-----------------|----------------------------------------|
| **Language**     | Python                                |
| **Frameworks**   | FastAPI (Backend), Streamlit (Frontend) |
| **Database**     | MySQL (AWS RDS)                        |
| **Vector Store** | ChromaDB                               |
| **LLM Model**    | OpenAI API + LangChain                 |
| **Deployment**   | AWS EKS, Docker, Kubernetes            |

---

## Installation & Setup

### Prerequisites

Ensure you have the following installed:

- **Python 3.12+**
- **Docker**
- **MySQL Database** (AWS RDS or local instance; refer to `init_ddl.sql` for setup instructions)
- **Environment Variables Configuration**

### Environment Configuration

Before running the project, create a `.env` file and configure the following variables:

```ini
OPENAI_API_KEY=
DB_HOST=
DB_NAME=llm_chatbot_example
DB_PASSWORD=
DB_PORT=3306
DB_USERNAME=
WEB_USER_AUTH=
WEB_PASS_AUTH=
WEB_URL=
WEB_AUTH=Basic base64encode(WEB_USER_AUTH:WEB_PASS_AUTH)
```

### Running Locally

#### 1. Clone the Repository

```bash
git clone <repo-url>
cd llm_chatbot_example
```

#### 2. Create a Virtual Environment & Install Dependencies

#### 3. Run FastAPI Backend

```bash
gunicorn --bind 0.0.0.0:8000 main:app --workers 1 --worker-class uvicorn.workers.UvicornH11Worker --preload
```

#### 4. Run Streamlit Frontend

```bash
streamlit run main_streamlit.py
```

#### 5. Access the UI

🔗 Open your browser and go to: `http://localhost:8501`

---

## Running with Docker

#### 1. Set Up Database & `.env` File

Ensure that your database is running and environment variables are correctly configured.

#### 2. Run Docker Compose

```bash
docker-compose up
```

#### 3. Access the UI

🔗 `http://localhost:8501`

---

## Deployment

### Dockerization

#### 1. Build Docker Images

- **Backend (FastAPI):**
  ```bash
  docker build -t llm-chatbot-backend -f Dockerfile_web .
  ```
- **Frontend (Streamlit):**
  ```bash
  docker build -t llm-chatbot-frontend -f Dockerfile_streamlit .
  ```

### Kubernetes Deployment (AWS EKS)

#### 1. Set Up AWS CLI, `eksctl`, and `kubectl`

Ensure AWS credentials are properly configured and required CLI tools are installed.

#### 2. Create an Elastic Container Registry (ECR) & Push Images

- Create ECR repositories for both backend and frontend.
- Push the built Docker images to ECR.

#### 3. Set Up VPC & EKS Cluster

- Configure a VPC with private subnets.
- Deploy an EKS cluster with worker nodes.

#### 4. Deploy Kubernetes Resources

- Apply Kubernetes deployment and service manifests.
- Verify the deployment and service status.

---

## Screenshots & Demo

**Screenshots** are available in the `docs/screenshots/` directory.  
**Video Demo:** [Watch Here](https://drive.google.com/file/d/1ohnHyVNMelEIcX6HWPRHn4R_Nq9-3EQt/view?usp=sharing).

---

## Future Improvements

**Planned Enhancements:**

- **Integrate Additional LLMs** to improve accuracy and diversity of responses.
- **Implement Caching Mechanisms** to reduce latency and enhance performance.
- **Enhance Deployment Strategy** by leveraging AWS Route 53 and refining Kubernetes configurations.

