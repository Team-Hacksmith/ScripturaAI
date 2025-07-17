# ScripturaAI

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-15.0+-black.svg)](https://nextjs.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com)

An intelligent documentation generation platform that leverages AI to automatically create comprehensive documentation, docstrings, algorithm explanations, guides, and visual diagrams from your codebase.

## Features

### Core Capabilities
- **Smart Docstring Generation**: Automatically generate professional docstrings/documentation for your code
- **Algorithm Explanation**: Convert complex code into clear, step-by-step algorithm explanations
- **Guide Creation**: Generate comprehensive guides and tutorials from your codebase
- **Mermaid Diagrams**: Create visual flowcharts and diagrams to illustrate code logic
- **GitHub Integration**: Clone and process entire repositories for documentation
- **Web Interface**: Beautiful, modern web interface for easy interaction
- **VS Code Extension**: Generate documentation directly from your editor with `Ctrl+D`

### Multiple Input Methods
- **Single Code Input**: Paste code directly into the web interface
- **File Upload**: Upload multiple code files for batch processing
- **GitHub Repository**: Process entire repositories by providing a GitHub URL
- **VS Code Integration**: Generate documentation without leaving your editor

### Output Formats
- **Enhanced Code**: Original code with added docstrings and comments
- **Markdown Documentation**: Professional documentation in Markdown format
- **Algorithm Explanations**: Step-by-step breakdowns of code logic
- **Mermaid Diagrams**: Visual representations of code flow
- **MkDocs Integration**: Generate static documentation websites

## Architecture

ScripturaAI consists of three main components:

```
                    ┌─────────────────────┐
                    │      Frontend       │
                    │      (Next.js)      │
                    └──────────┬──────────┘
                               │
                               │ HTTP/REST
                               │
                    ┌──────────▼──────────┐
                    │      Backend        │
                    │    (Flask API)      │
                    └─────────┬───────────┘
                              │
                              │ API Calls
                              │
                    ┌─────────▼───────────┐
                    │    AI Engine        │
                    │  (OpenAI/LangChain) │
                    └─────────────────────┘

    Additional Components:
    
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │  VS Code    │    │   GitHub    │    │   MkDocs    │
    │ Extension   │───►│ Integration │───►│  Generator  │
    └─────────────┘    └─────────────┘    └─────────────┘
           │                   │                   │
           └───────────────────┼───────────────────┘
                               │
                        ┌──────▼──────┐
                        │   Backend   │
                        │ (Flask API) │
                        └─────────────┘
```

### Technology Stack

**Frontend:**
- Next.js 15 with TypeScript
- Tailwind CSS for modern UI
- Radix UI components
- Monaco Editor for code editing
- Dark/Light theme support

**Backend:**
- Python 3.12+ with Flask
- LangChain for AI orchestration
- OpenAI GPT-4 for code analysis
- File processing and Git integration
- MkDocs for documentation generation

**VS Code Extension:**
- JavaScript-based extension
- Keyboard shortcuts (`Ctrl+D`)
- Real-time integration with backend

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- pnpm (recommended) or npm
- OpenAI API Key

### 1. Clone the Repository
```bash
git clone https://github.com/Team-Hacksmith/ScripturaAI.git
cd ScripturaAI
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies using Poetry
pip install poetry
poetry install

# Or use pip
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
pnpm install
# or npm install

# Start development server
pnpm dev
# or npm run dev
```

### 4. VS Code Extension Setup
```bash
cd hacksmith-vsce

# Install dependencies
pnpm install

# Package the extension (optional)
npx vsce package
```

### 5. Environment Configuration

Create a `.env` file in the backend directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Web Interface

1. **Start the Backend:**
   ```bash
   cd backend
   poetry run python main.py
   # or python main.py
   ```

2. **Start the Frontend:**
   ```bash
   cd frontend
   pnpm dev
   ```

3. **Open your browser** to `http://localhost:3000`

### Available Generation Types

#### Code Documentation
- Adds professional docstrings to functions and classes
- Supports Python, JavaScript, C/C++, and more
- Preserves original code structure

#### Algorithm Explanation
- Converts code into step-by-step explanations
- Perfect for educational content
- Outputs in Markdown format

#### Guide Generation
- Creates comprehensive tutorials
- Explains code purpose and usage
- Ideal for project documentation

#### Diagram Creation
- Generates Mermaid flowcharts
- Visualizes code logic and flow
- Great for architecture documentation

### VS Code Extension

1. Install the extension from the `hacksmith-vsce` folder
2. Select code in VS Code
3. Press `Ctrl+D` or run "hacksmith" command
4. Get AI-generated documentation instantly

### API Endpoints

```http
POST /upload          # Upload files for processing
POST /single          # Process single code snippet
POST /github/clone    # Clone and process GitHub repository
POST /github/docs     # Generate documentation website
GET  /docs/{repo}     # Access generated documentation
```

