# AI Asset Management Agent

An intelligent asset management system that combines traditional CRUD operations with AI-powered natural language querying. Users can manage assets through a REST API and interact with their data using conversational queries.

## Features

- **CRUD Operations**: Full create, read, update, and delete functionality for assets
- **AI Agent**: Natural language interface to query and analyze your assets
- **Short-Term Memory**: The AI agent remembers recent queries within a session for more accurate, context-aware responses.
- **RESTful API**: Built with FastAPI for high performance and automatic documentation
- **LangChain Integration**: Leverages LangChain for intelligent agent behavior
- **SQLite Database**: Lightweight, file-based storage for easy deployment
- **Docker Support**: One-command deployment with automated build script



## Quick Start

### Prerequisites

- Docker (will be installed automatically by build script if not present)
- OpenAI API Key

### Installation & Deployment

1. **Clone the repository**
```bash
git clone https://github.com/lamasalah32/asset-management-agent.git
cd asset-management-agent
```

2. **Run the deployment script**
```bash
chmod +x build.sh
./build.sh
```

The script will:
- Check for Docker installation (install if needed)
- Prompt for your OpenAI API key
- Build the Docker image
- Start the container
- Display access information

## API Endpoints

### Asset Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/assets` | Create a new asset |
| GET | `/assets` | List all assets |
| GET | `/assets/{id}` | Get asset by ID |
| PUT | `/assets/{id}` | Update an asset |
| DELETE | `/assets/{id}` | Delete an asset |

### AI Agent

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/agent/query` | Ask natural language questions about assets |

## Asset Schema

```json
{
  "name": "MacBook Pro",
  "category": "Electronics",
  "value": 2500.00,
  "purchase_date": "2024-01-15",
  "status": "Active"
}
```

## Usage Examples

### Creating an Asset

```bash
curl -X POST "http://localhost:8000/assets" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MacBook Pro",
    "category": "Electronics",
    "value": 2500.00,
    "purchase_date": "2024-01-15",
    "status": "Active"
  }'
```

### Querying with AI Agent

```bash
curl -X POST "http://localhost:8000/agent/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is my most valuable asset?"
  }'
```

**Response:**
```json
{
  "answer": "Your most valuable asset is MacBook Pro ($2500.0)",
  "sources": []
}
```

### Short-Term Memory Example

The agent can maintain context within a session.

Query assets by category

```bash
curl -X POST "http://localhost:8000/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "List all my electronics"}'
```

Follow-up query using context

```bash
curl -X POST "http://localhost:8000/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "Which of these is the most valuable?"}'
```

The agent remembers the previous list and returns an accurate answer, including the asset IDs as sources.

### Example Questions for AI Agent

- "What is my most valuable asset?"
- "List all my electronics"
- "How many assets do I have?"
- "What are my total assets worth?"


## Configuration

### Environment Variables

- `OPENAI_API_KEY` (required): Your OpenAI API key

### Switching LLM Models

To use a different OpenAI model, edit `llm.py`:

```python
def get_llm():
    return ChatOpenAI(
        model="gpt-4",  # Change model here
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
```

