# 🛡️ Sentinel: Autonomous Cloud Security Agent

> **An intelligent, human-in-the-loop AI agent that audits, detects, and actively remediates AWS cloud security vulnerabilities.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Powered by LangGraph](https://img.shields.io/badge/LangGraph-Agentic-orange)](https://langchain-ai.github.io/langgraph/)

---

## 🎥 Demo
**[Watch the 60-Second Walkthrough Video Here]** *(Add your Loom link here)*

![Dashboard Screenshot](https://via.placeholder.com/800x400?text=Sentinel+Dashboard+Preview)
*(The agent detecting a public S3 bucket and requesting permission to fix it.)*

---

## 🚀 Overview

Sentinel is not just a monitoring dashboard—it is an **Agentic System**. Unlike traditional tools that merely log errors, Sentinel uses **Large Language Models (GPT-4o)** to reason about security findings and take action.

It connects directly to your AWS environment, identifies high-risk misconfigurations (e.g., Public S3 Buckets, Unused EC2 Instances), and engages in a **Human-in-the-Loop** workflow to fix them.

### **Key Capabilities**
* **🔍 Autonomous Scanning:** proactively audits AWS S3, IAM, and EC2 resources.
* **🧠 Intelligent Reasoning:** Uses LangGraph to determine if a configuration is a feature or a bug.
* **🛡️ Active Remediation:** Can fix vulnerabilities (e.g., `BlockPublicAccess`) upon user approval.
* **💬 Natural Language Interface:** Chat with your cloud infrastructure to ask questions like *"Why is my bill high?"*

---

## 🏗️ Architecture

Sentinel is built on a modern, containerized AI stack designed for security and scalability.

```mermaid
graph TD
    User[User via Web UI] <-->|Gradio| Frontend
    Frontend <-->|API| Agent[LangGraph Agent]
    Agent <-->|Reasoning| LLM[OpenAI GPT-4o]
    Agent <-->|Boto3| AWS[AWS Cloud Environment]
    
    subgraph "Docker Container"
        Frontend
        Agent
    end