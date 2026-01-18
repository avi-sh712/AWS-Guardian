# AWS Sentinel Agent 🛡️

A secure, autonomous agent that audits AWS infrastructure for security misconfigurations. It features a **Human-in-the-Loop (HITL)** approval workflow to prevent unauthorized changes and uses the **Model Context Protocol (MCP)** to standardize tool execution.

## 🚀 Features

* **Automated Scanning**: Detects public S3 buckets and idle EC2 instances using native AWS APIs (Boto3).
* **Intelligent Analysis**: Uses LLM reasoning (GPT-4o) to distinguish between false positives and actual risks.
* **Human-in-the-Loop**: Includes a Gradio dashboard that requires user approval before applying any remediation fixes.
* **MCP Integration**: Implements a custom Model Context Protocol (MCP) server to handle AWS tool execution.
* **State Management**: Built with LangGraph to maintain conversation state and handle interrupts during the approval process.

## 🛠️ Tech Stack

* **Language**: Python 3.12
* **Orchestration**: LangGraph
* **AI Model**: OpenAI GPT-4o-mini
* **Protocol**: Model Context Protocol (MCP)
* **Infrastructure**: AWS SDK (Boto3)
* **Interface**: Gradio

## 📋 Prerequisites

* Python 3.12 or higher
* An AWS Account with valid credentials
* OpenAI API Key

## ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/sentinel-agent.git](https://github.com/yourusername/sentinel-agent.git)
    cd sentinel-agent
    ```

2.  **Install dependencies (using uv):**
    ```bash
    uv pip install -r requirements.txt
    ```
    *(Alternatively, you can use standard pip: `pip install -r requirements.txt`)*

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory:
    ```bash
    # .env
    OPENAI_API_KEY=sk-proj-your-key...
    AWS_ACCESS_KEY_ID=AKIA...
    AWS_SECRET_ACCESS_KEY=...
    AWS_REGION=us-east-1
    ```

## 🖥️ Usage

1.  **Start the Dashboard:**
    ```bash