# AI Bidding Document Generator

This project automatically generates professional bid documents based on tender files using the DeepSeek API. It supports both PDF and text input files, and generates a complete Word document as output.

## Features

- Automatic analysis of tender documents to extract requirements
- Intelligent section generation based on industry standards
- Support for PDF and text input files
- Automatic conversion to Word format with proper formatting
- Professional document structure with proper headers, footers, and styling
- Support for tables, images, and diagrams
- Quality checks and optimization of generated content

## System Requirements

- Python 3.8 or higher
- Node.js 16.0 or higher (for Mermaid diagram support)
- Mermaid CLI (for diagram generation)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd ai_bidding
```

2. Create and activate a virtual environment:
```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Mermaid CLI (for diagram generation):
```bash
# Using npm
npm install -g @mermaid-js/mermaid-cli

# Using yarn
yarn global add @mermaid-js/mermaid-cli
```

5. Create a `.env` file in the project root with your API configuration:
```
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_API_BASE=your_api_base_url_here
```

6. Create a `config/config.yaml` file with the following structure:
```yaml
api:
  api_key: ${DEEPSEEK_API_KEY}
  base_url: ${DEEPSEEK_API_BASE}
  model: "deepseek-chat"
  temperature: 0.7
  max_tokens: 2000
  top_p: 0.9

paths:
  input_dir: "data/input"
  output_dir: "data/output"
```

## Usage

1. Prepare your project structure:
```bash
mkdir -p data/input data/output
```

2. Place your tender files (PDF or text) in the `data/input` directory.

3. Run the generator:
```bash
# From the project root directory
python src/main.py
```

4. The generated bid documents will be saved in the `data/output` directory, organized by tender name.

## Output Structure

The generated bid document includes:

- Cover page with project details
- Table of contents
- Bid letter
- Technical proposal
- Implementation plan
- Service and maintenance plan
- Commercial proposal
- Pricing section
- Required attachments
- Format attachments

## Software Versions

The project has been tested with the following versions:

### Python Dependencies
- openai==1.12.0
- python-dotenv==1.0.0
- PyPDF2==3.0.1
- tqdm==4.66.1
- markdown==3.4.3
- python-docx==0.8.11
- PyYAML==6.0.1

### System Requirements
- Python 3.8.10 or higher
- Node.js 16.20.0 or higher
- Mermaid CLI 10.6.1 or higher

## Troubleshooting

1. If you encounter issues with Mermaid diagrams:
   - Ensure Mermaid CLI is properly installed
   - Check if the `mmdc` command is available in your PATH
   - Verify Node.js version is compatible

2. For PDF processing issues:
   - Ensure PyPDF2 is properly installed
   - Check if the PDF file is not password protected
   - Verify the PDF file is not corrupted

3. For API connection issues:
   - Verify your API key and base URL in the `.env` file
   - Check your internet connection
   - Ensure the API endpoint is accessible

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 