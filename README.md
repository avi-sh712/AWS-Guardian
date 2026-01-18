# 🛡️ Guardian: Autonomous Cloud Security Agent

> **An intelligent, human-in-the-loop AI agent that audits, detects, and actively remediates AWS cloud security vulnerabilities using the Model Context Protocol (MCP).**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Powered by LangGraph](https://img.shields.io/badge/LangGraph-Agentic-orange)](https://langchain-ai.github.io/langgraph/)
[![MCP Ready](https://img.shields.io/badge/MCP-Protocol-green)](https://modelcontextprotocol.io/)

---

## 🎥 Demo
**[Watch the 60-Second Walkthrough Video Here]** *(Add your Loom link here)*

![Dashboard Screenshot](https://via.placeholder.com/800x400?text=Guardian+Dashboard+Preview)
*(The agent detecting a public S3 bucket and requesting permission to fix it.)*

---

## 🚀 Overview

Guardian is a next-generation **Agentic Security System** built on the **Model Context Protocol (MCP)**. Unlike traditional scripts that hardcode API calls, Guardian decouples the "Brain" (AI) from the "Tools" (AWS).

It connects to a dedicated **AWS MCP Server**, identifies high-risk misconfigurations (e.g., Public S3 Buckets, Unused EC2 Instances), and engages in a **Human-in-the-Loop** workflow to fix them.

### **Key Capabilities**
* **🔌 MCP Architecture:** Uses the Model Context Protocol to standardize tool usage, making the agent modular and secure.
* **🔍 Autonomous Scanning:** Proactively audits AWS S3, IAM, and EC2 resources via the MCP Server.
* **🧠 Intelligent Reasoning:** Uses LangGraph to determine if a configuration is a feature or a bug.
* **🛡️ Active Remediation:** Can fix vulnerabilities (e.g., `BlockPublicAccess`) upon user approval.
* **💬 Natural Language Interface:** Chat with your infrastructure (e.g., *"Why is my bill high?"*)

---

## 🏗️ Architecture

Guardian uses a decoupled architecture where the Agent communicates with AWS tools strictly through the **MCP Protocol**. This ensures the AI reasoning layer is isolated from direct API implementation details.

```mermaid
graph TD
    User[User via Web UI] <-->|Gradio| Frontend
    Frontend <-->|API| Agent[LangGraph Agent]
    
    subgraph "Reasoning Layer"
        Agent <-->|Context| LLM[OpenAI GPT-4o]
    end

    subgraph "Tool Execution Layer (MCP)"
        Agent <==>|MCP Protocol| MCPServer[AWS MCP Server]
        MCPServer <-->|Boto3| AWS[AWS Cloud Resources]
    end