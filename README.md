# LLM Red Teaming Prompt Injection Defender

A toolkit to **detect, simulate, and defend against prompt injection attacks** in LLM applications.

## Features

- Prompt injection detection modules
- Attack simulation and coverage reports
- Automated defense strategies
- Integration with CI/CD pipelines

## Tech Stack

- **Python 3.10+**
- **Docker**
- **GitHub Actions** (CI/CD)
- **Pre-commit** (linting, formatting)

## Project Structure

```
.
├── main.py
├── defender/
│   ├── __init__.py
│   ├── detection.py
│   └── mitigation.py
├── tests/
│   ├── test_detection.py
│   └── test_mitigation.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── .github/workflows/ci.yml
```

## Getting Started

1. **Clone the repo:**  
   `git clone https://github.com/jokepool710/LLM-Red-Teaming-Prompt-Injection-Defender.git`
2. **Install dependencies:**  
   `pip install -r requirements.txt`
3. **Copy `.env.example` to `.env` and fill in variables.**
4. **Run locally:**  
   `python main.py`
5. **Or with Docker:**  
   `docker-compose up --build`

## Contributing

- Pre-commit hooks for linting/formatting
- PRs and Issues welcome!

## License

MIT