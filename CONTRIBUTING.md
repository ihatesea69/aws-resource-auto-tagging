# Contributing to AutoTag

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/ihatesea69/aws-resource-auto-tagging.git
cd aws-resource-auto-tagging

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r tests/requirements.txt
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Adding a New Service Handler

1. Add a handler function in `src/handlers/` (or extend an existing file)
2. Add a resource extractor in `src/resource_extractors.py`
3. Register the `(eventSource, eventName)` mapping in `src/config.py`
4. Add the event to the EventBridge rule in `template.yaml`
5. Add the required IAM permission to the Lambda role in `template.yaml`
6. Add tests for the new extractor in `tests/`
7. Update the supported services table in `README.md`

## Pull Request Process

1. Fork the repo and create a feature branch from `main`
2. Write tests for any new functionality
3. Ensure all tests pass: `python -m pytest tests/ -v`
4. Update documentation if needed
5. Submit a PR with a clear description of the change

## Code Style

- Follow PEP 8
- Use type hints where practical
- Add docstrings to public functions
- Keep handlers focused — one handler per event type

## Reporting Issues

Open an issue with:
- A clear title and description
- Steps to reproduce (if applicable)
- Expected vs actual behavior
- CloudWatch log snippets (redact account IDs and sensitive info)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
