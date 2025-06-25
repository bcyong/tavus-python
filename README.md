# Tavus Python CLI

A Python CLI wrapper for the Tavus API that provides an interactive command-line interface for managing replicas, personas, and videos.

## Features

- **Interactive CLI**: Easy-to-use command-line interface with state machine navigation
- **Replica Management**: Create, list, rename, and delete replicas
- **Persona Management**: Manage system and user personas
- **Video Generation**: Generate videos using replicas
- **Video Management**: List, rename, and delete videos
- **API Key Management**: Secure API key handling with file-based storage


<p align="center"><img src="/img/demo.gif?raw=true"/></p>
<p align="center">(the API key is invalid)</p>

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd tavus-python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the CLI tool:
```bash
python src/main.py
```

### API Key Configuration

The tool supports API key configuration in two ways:

1. **File-based (Recommended)**: Create a `.tavus_api_key` file in your project directory:
```bash
echo "your-tavus-api-key-here" > .tavus_api_key
```

2. **Custom path**: Specify a custom path for your API key file:
```bash
python src/main.py --api-key-file /path/to/your/api_key.txt
```

3. **Interactive prompt**: If no API key file is found, the tool will prompt you to enter your API key interactively.

### Command Line Options

- `--api-key-file`, `-f`: Path to file containing the Tavus API key (default: `.tavus_api_key`)

## Features Overview

### Replica Management
- List all replicas
- Create new replicas
- Rename existing replicas
- Delete replicas
- View replica details

### Persona Management
- List system and user personas
- Create new personas
- Update persona information
- Delete personas

### Video Management
- Generate videos using replicas and personas
- List all videos
- Rename videos
- Delete videos
- View video details and status

## Project Structure

```
tavus-python/
├── src/
│   ├── main.py              # Main CLI entry point
│   ├── api_client.py        # Tavus API client implementation
│   ├── state_machine.py     # Interactive state machine
│   ├── paginated_list.py    # Paginated list display utilities
│   ├── paginated_bullet.py  # Paginated bullet point selection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── persona.py       # Persona data models
│   │   ├── replica.py       # Replica data models
│   │   └── video.py         # Video data models
│   └── .tavus_api_key       # API key file (create this)
├── img/
│   └── demo.gif             # Demo animation
├── README.md
└── requirements.txt         # Python dependencies
```

## API Key Security

- Store your API key in a `.tavus_api_key` file (default)
- The file should contain only your API key, no additional formatting
- Ensure the file has appropriate permissions (readable only by you)
- Add `.tavus_api_key` to your `.gitignore` to prevent accidental commits

## Requirements

- Python 3.7+
- `click` - Command line interface creation kit
- `bullet` - Interactive prompts
- `yaspin` - Terminal spinner for loading states
- `requests` - HTTP library for API calls

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Create an issue in this repository
- Contact Tavus support for API-related questions
