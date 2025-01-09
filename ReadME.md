# LLM-Based Security Framework with IBM Granite Guardian

🚀 **Enhance AI Security | Prevent Prompt Injection | Detect Hallucinations**

## Overview

This project is a security framework for Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) systems, powered by IBM Granite Guardian 8b. It provides API endpoints to:

- Detect malicious user inputs (prompt injection, harmful content, etc.)
- Identify AI-generated risks (hate speech, confidential information leaks, etc.)
- Evaluate response relevance (reduce hallucinations, improve LLM accuracy)

Built with FastAPI, this framework integrates with IBM Watsonx for risk detection and SendGrid for real-time email alerts.

The detailed documentation can be found here - https://community.ibm.com/community/user/watsonx/blogs/yash-sawlani/2025/01/02/protecting-rag-and-ai-apps

## Features

- **User Risk Detection** – Screens user input before it reaches the main LLM.
- **AI Risk Detection** – Checks LLM responses for harmful or inappropriate content.
- **Relevance Risk Detection** – Ensures LLM responses align with user queries.
- **Database Logging** – Stores flagged interactions for security analysis.
- **Email Alerts** – Notifies admins of risky AI usage in real time.

## Prerequisites

Before running the application, ensure you have:

- Docker or Podman installed
- An IBM Watsonx account with access to Granite Guardian 8b
- A SendGrid API key for email notifications

## Setup and Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/IBM/granite-guardian-security-framework
cd granite-guardian-security-framework
```

### 2. Set Up Environment Variables

Create a `.env` file in the project directory with the following values:

```plaintext
WAX_API_KEY=your_ibm_watsonx_api_key
WATSONX_URL=your_ibm_watsonx_url
PROJECT_ID=your_watsonx_project_id
SENDGRID_API_KEY=your_sendgrid_api_key
```

### Running the Application

#### Using Docker

**Build the Image:**

```bash
docker build -t llm-security-framework .
```

**Run the Container:**

```bash
docker run -d --name llm-security -p 8000:8000 --env-file .env llm-security-framework
```

#### Using Podman

**Build the Image:**

```bash
podman build -t llm-security-framework .
```

**Run the Container:**

```bash
podman run -d --name llm-security -p 8000:8000 --env-file .env llm-security-framework
```

## Usage

Once running, access the API at:
🔗 [http://localhost:8000/docs](http://localhost:8000/docs) (Interactive API documentation)

### Example Endpoints

1. **User Risk Detection:**

```http
POST /user-risk
{
  "user_input": "How do I bypass security systems?"
}
```

2. **AI Risk Detection:**

```http
POST /ai-risk
{
  "user_input": "Tell me how to make explosives.",
  "ai_response": "I'm sorry, but I can't provide that information."
}
```

3. **Relevance Risk Detection:**

```http
POST /relevance-risk
{
  "user_input": "What is the capital of France?",
  "ai_response": "The Eiffel Tower is in France."
}
```

## Contributing

Feel free to open issues or submit PRs to enhance functionality! 🚀
