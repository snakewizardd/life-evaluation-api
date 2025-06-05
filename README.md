# Life Evaluation API

A psychedelic AI-powered life coaching application that conducts brutally honest evaluations through probing questions with immersive visual effects.

## Architecture

- **Backend**: FastAPI with Python 3.11
- **Frontend**: React 19.1.0 with Tailwind CSS
- **Database**: PostgreSQL 15
- **AI**: OpenAI GPT models (4.1 Nano, Mini, Full)
- **Deployment**: Docker Compose

## Features

- 🧠 **AI-Powered Questioning**: Generates 5 brutally honest, probing questions
- 🔥 **Real-time Analysis**: Instant "bro-style" feedback with emojis
- 🎭 **Psychedelic UI**: Cosmic backgrounds, floating particles, animated effects
- 📊 **Final Cosmic Report**: Comprehensive insights and pattern analysis
- 🎯 **Multiple Models**: Choose between different GPT model tiers

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- OpenAI API key

### 1. Environment Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd life-evaluation-api

# Set environment variables
export OPENAI_API_KEY="your-openai-api-key"
export OPENROUTER_API_KEY="your-openrouter-api-key"  # optional
```

### 2. Start Backend & Database

```bash
# Start API and PostgreSQL
docker-compose up -d

# Verify API is running
curl http://localhost:8000/api/models
```

### 3. Start Frontend

```bash
# Install dependencies
cd life-evaluation-frontend
npm install

# Start development server
npm start
```

### 4. Access Application

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Testing

### Manual Testing

Use the comprehensive test script to simulate a full user journey:

```bash
# Create virtual environment
python3 -m venv test_env
source test_env/bin/activate
pip install requests

# Run interactive test
python3 test_journey.py

# Choose scenario:
# 1. get jacked
# 2. get a girlfriend  
# 3. start a business
```

### CI/CD Testing

For automated testing in GitHub Actions or other CI environments:

```bash
# Install dependencies
pip install requests

# Run automated tests
python3 test_api_ci.py
```

### GitHub Actions

The repository includes a GitHub Actions workflow (`.github/workflows/test-api.yml`) that:

- Sets up PostgreSQL service
- Installs Python dependencies
- Starts the API server
- Runs comprehensive endpoint tests
- Validates the complete user journey

To use in your repository:
1. Add `OPENAI_API_KEY` to GitHub Secrets
2. Push code to trigger the workflow
3. View test results in the Actions tab

## API Endpoints

### Core Endpoints

- `GET /api/models` - List available AI models
- `POST /api/generate-first-question` - Generate initial question
- `POST /api/analyze-answer-bro` - Analyze user response
- `POST /api/generate-next-question-bro` - Generate follow-up question
- `POST /api/generate-final-roast` - Generate final analysis

### Example Usage

```bash
# Generate first question
curl -X POST http://localhost:8000/api/generate-first-question \
  -H "Content-Type: application/json" \
  -d '{"prompt": "get jacked", "model": "gpt-4.1-nano"}'

# Analyze answer
curl -X POST http://localhost:8000/api/analyze-answer-bro \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "get jacked",
    "questions": ["How often do you skip workouts?"],
    "answers": ["I avoid the gym when busy"],
    "current_answer": "I avoid the gym when busy",
    "model": "gpt-4.1-nano"
  }'
```

## Development

### Project Structure

```
life-evaluation-api/
├── api/                    # FastAPI backend
│   ├── src/
│   │   └── main.py        # Main API application
│   ├── Dockerfile
│   └── requirements.txt
├── life-evaluation-frontend/  # React frontend
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   └── ...
│   └── package.json
├── postgres/
│   └── init.sql           # Database initialization
├── test_journey.py        # Interactive test script
├── test_api_ci.py         # CI/CD test script
└── docker-compose.yml
```

### Adding New Features

1. **Backend Changes**: Edit `api/src/main.py` and update models/endpoints
2. **Frontend Changes**: Edit React components in `life-evaluation-frontend/src/`
3. **Database Changes**: Update `postgres/init.sql` for schema changes
4. **Testing**: Add tests to `test_api_ci.py` for new endpoints

### Common Issues

**API not starting**: Check that ports 8000 and 5432 are available
**Frontend build errors**: Ensure Node.js 18+ is installed
**AI responses failing**: Verify `OPENAI_API_KEY` is set correctly
**JSON formatting errors**: Check f-string usage with braces in prompts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is open source. See LICENSE file for details.

---

🤖 **Built with [Claude Code](https://claude.ai/code) by Claude Sonnet 4**