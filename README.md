# LangGraph Human-in-the-Loop Support Agent

A stateful AI support assistant built with **LangGraph, LangChain, Groq, and MongoDB** that can recognize when a user needs human assistance, pause the workflow, persist its state, and resume the conversation after a human support agent provides a response.

The main goal of this project was to understand how **stateful AI workflows and human-in-the-loop systems** can be built using LangGraph rather than treating an LLM as a simple chatbot.

---

## 🚀 What This Project Does

The assistant can handle normal conversations using an LLM.

When a user explicitly asks to speak with a human or contact support, the assistant can:

1. Detect the request using LLM tool calling.
2. Call a `human_assistance_tool`.
3. Pause execution using LangGraph's `interrupt()`.
4. Save the current graph state to MongoDB.
5. Allow a separate support process to inspect the pending request.
6. Accept a response from a human support agent.
7. Resume the interrupted workflow using `Command(resume=...)`.

This creates a simple but realistic **AI → Human → AI** workflow.

---

## 🧠 Architecture

```text
                         ┌──────────────────┐
                         │      User        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ LangGraph Chatbot│
                         │      + LLM       │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
              Normal request             Human support
                    │                           │
                    ▼                           ▼
              LLM Response           human_assistance_tool
                                                │
                                                ▼
                                           interrupt()
                                                │
                                                ▼
                                      MongoDB Checkpoint
                                                │
                                                ▼
                                         support.py
                                                │
                                      Human Support Agent
                                                │
                                                ▼
                                      Command(resume=...)
                                                │
                                                ▼
                                      LangGraph resumes
                                                │
                                                ▼
                                           AI Response
```

---

## 🛠️ Tech Stack

- **Python**
- **LangGraph** – stateful workflow orchestration
- **LangChain** – LLM and tool integration
- **Groq** – LLM inference
- **MongoDB** – persistent graph checkpoints
- **Docker / Docker Compose** – local MongoDB setup

---

## 🔑 Key Concepts

### 1. LLM Tool Calling

The model is given access to a custom tool:

```python
human_assistance_tool(query)
```

The LLM decides when the tool should be used based on the user's request.

For example:

> "I'm having trouble signing in. Can you connect me with support?"

The model can generate a tool call instead of simply giving generic troubleshooting instructions.

---

### 2. Human-in-the-Loop

The tool uses LangGraph's `interrupt()`:

```python
human_response = interrupt({"query": query})
```

At this point, the graph pauses execution.

The workflow does not continue until a human provides a response.

---

### 3. Persistent Checkpointing

The graph uses MongoDB for checkpoint persistence:

```python
MongoDBSaver.from_conn_string(MONGODB_URI)
```

This means the graph state can survive outside the current function execution and can be accessed by another process.

---

### 4. Resuming the Workflow

The support process can resume the interrupted graph using:

```python
Command(resume={"data": ans})
```

The human response becomes the result of the interrupted tool and the graph continues from where it stopped.

---

## 📂 Project Structure

```text
LangGraph/
│
├── app/
│   ├── graph.py
│   ├── main.py
│   ├── support.py
│   └── docker-compose.yml
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### `graph.py`

Contains the LangGraph workflow, chatbot node, human assistance tool, tool routing, and graph definition.

### `main.py`

Runs the main user-facing chatbot.

### `support.py`

Acts as the human support interface. It reads the pending checkpoint and resumes the graph after the support agent provides a response.

### `docker-compose.yml`

Starts MongoDB locally for checkpoint persistence.

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd LangGraph
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`:

```env
GROQ_API_KEY=your_groq_api_key
```

**Do not commit the `.env` file to GitHub.**

---

## 🗄️ Start MongoDB

From the project directory:

```bash
docker compose -f app/docker-compose.yml up -d
```

Check that MongoDB is running:

```bash
docker ps
```

---

## ▶️ Run the Application

Start the chatbot:

```bash
python -m app.main
```

Example:

```text
> Hello
AI: Hello! How can I help you?

> I am having trouble signing in. Can you connect me with support?
```

The graph detects the human-support request and pauses.

You can then run the support process:

```bash
python -m app.support
```

The support agent can provide a response:

```text
Resolution> Please send your troubleshooting details to our support team.
```

The graph then resumes using the human-provided response.

---

## 🔄 Example Workflow

### User

```text
I am having trouble signing in.
Can you connect me with support?
```

### AI

```text
Tool Call:
human_assistance_tool
```

### Graph

```text
interrupt()
```

### MongoDB

```text
Graph state saved
```

### Support Agent

```text
Resolution>

Please send your troubleshooting details to our support team.
```

### Resume

```python
Command(resume={"data": response})
```

The workflow continues from the interrupted point.

---

## 🎯 Why I Built This

I built this project to go beyond a basic LLM chatbot and understand how **agentic workflows maintain state, call tools, pause execution, and continue later**.

The project helped me understand several important concepts:

- Stateful AI applications
- LangGraph graph execution
- Tool calling
- Conditional routing
- Human-in-the-loop workflows
- Interrupt and resume patterns
- Persistent checkpoints
- MongoDB-backed state
- Running different parts of an AI workflow as separate processes

---

## 🔮 Possible Improvements

Some ideas for extending the project:

- Add multiple support conversations.
- Give each conversation a unique thread ID.
- Build a web interface for the support agent.
- Add authentication for support agents.
- Store support tickets separately from graph checkpoints.
- Add email notifications when human assistance is requested.
- Add conversation history and ticket status.
- Deploy the application using Docker.
- Add observability and tracing.

---

## 📌 Current Status

This is a learning and portfolio project focused on understanding **LangGraph state management and human-in-the-loop workflows**.

The core workflow of:

```text
User → AI → Tool → Interrupt → MongoDB → Human → Resume → AI
```

is implemented and working locally.

---

## 👨‍💻 Author

**Puneet Kumar**

B.Tech Computer Science

Interested in **Software Engineering, AI Engineering, Generative AI, and backend systems**.
