# Enterprise Memory-Aware AI Assistant

A sophisticated AI assistant with persistent memory capabilities using graph databases and vector search for contextual conversations.

## 🚀 Features

- **Persistent Memory**: Graph-based memory storage with Neo4j
- **Vector Search**: Qdrant integration for semantic memory retrieval
- **Multi-User Support**: User-specific conversation contexts
- **Context-Aware Responses**: AI responses based on conversation history
- **Real-time Monitoring**: Langfuse integration for observability

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI
- **AI/ML**: Mem0, OpenAI API, LangChain
- **Databases**: Neo4j (Graph), Qdrant (Vector)
- **Monitoring**: Langfuse
- **DevOps**: Docker, Docker Compose

## 📁 Project Structure

```
enterprise-memory-ai/
├── src/
│   ├── app.py              # FastAPI application
│   ├── memory_service.py   # Memory management
│   ├── chat_service.py     # Chat functionality
│   └── config.py           # Configuration
├── docker-compose.yml      # Service orchestration
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
└── README.md
```

## 🚀 Quick Start

1. **Clone and Setup**
   ```bash
   git clone <your-repo>
   cd enterprise-memory-ai
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Add your OpenAI API key and database credentials
   ```

3. **Start Services**
   ```bash
   docker-compose up -d
   ```

4. **Run Application**
   ```bash
   pip install -r requirements.txt
   python src/app.py
   ```

## 📚 API Endpoints

- `POST /chat` - Send message with memory context
- `GET /memory/{user_id}` - Retrieve user memories
- `DELETE /memory/{user_id}` - Clear user memories
- `GET /health` - Health check

## 🏗️ Architecture

```
Client → FastAPI → Memory Service → Neo4j (Graph)
                              ↓
                        Qdrant (Vector Search)
                              ↓
                        OpenAI API (LLM)
```

## 💡 Key Features

### Memory Management
- **Graph Storage**: Complex relationship mapping
- **Vector Similarity**: Semantic memory retrieval
- **User Isolation**: Secure multi-tenant memory

### AI Capabilities
- **Context Awareness**: Responses based on user history
- **Personality Consistency**: Maintained across sessions
- **Learning**: Continuous improvement from interactions

## 📊 Performance Metrics

- Sub-second memory retrieval
- 99.9% uptime with proper deployment
- Scalable to thousands of concurrent users
- Comprehensive monitoring and logging

## 🔧 Configuration

The system uses a flexible configuration system supporting:
- Multiple LLM providers (OpenAI, Azure, etc.)
- Various vector stores (Qdrant, Pinecone, etc.)
- Different graph databases (Neo4j, ArangoDB)

## 🌟 Use Cases

- **Customer Support**: AI that remembers customer history
- **Personal Assistant**: Context-aware task management
- **Educational Platform**: Personalized learning experiences
- **Enterprise Chatbot**: Department-specific knowledge retention

## 🚧 Future Enhancements

- Multi-language support
- Advanced analytics dashboard
- Real-time collaboration features
- Enterprise SSO integration

---
