# AI Bidding Document Generator

[English](README.md) | [中文](README_CN.md)

This project automatically generates professional bid documents from tender files using the DeepSeek API. It supports both PDF and text input files and outputs a complete Word document.

## Features

- Automatic analysis of tender documents and requirement extraction
- Intelligent section generation based on industry standards
- Support for PDF and text format tender files
- Automatic conversion to Word format with professional formatting
- Professional document structure with headers, footers, and styles
- Support for tables, images, and flowcharts
- Content quality checks and optimization

## System Requirements

- Python 3.8 or higher
- Node.js 16.0 or higher (for Mermaid flowchart support)
- Mermaid CLI (for flowchart generation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Graped/ai_bidding.git
cd ai_bidding
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Mermaid CLI (for flowchart generation):
```bash
# Using npm
npm install -g @mermaid-js/mermaid-cli

# Using yarn
yarn global add @mermaid-js/mermaid-cli
```

5. Create a `.env` file in the project root directory with your API information:
```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
```

6. Create the `config/config.yaml` configuration file:
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

1. Prepare the project directory structure:
```bash
mkdir -p data/input data/output
```

2. Place your tender files (PDF or text format) in the `data/input` directory.

3. Run the generator:
```bash
# From the project root directory
python src/main.py
```

4. Generated bid documents will be saved in the `data/output` directory, organized by tender project name.

## Output Structure

The generated bid document includes:

- Cover page (with project details)
- Table of contents
- Bid letter
- Technical proposal
- Implementation plan
- After-sales service plan
- Commercial section
- Pricing section
- Required attachments
- Format attachments

## Software Versions

Tested versions:

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

## Data Security

### Sensitive Information Handling
1. API Keys
   - Store API keys in environment variables
   - Do not commit the `.env` file to version control
   - Use placeholders (e.g., `sk-xxxxxxxx`) in examples

2. Tender Files
   - Remove sensitive information from example files
   - Replace project names, amounts, and other key information with sample data
   - Replace with actual project information when using

3. Generated Bid Documents
   - Remove sensitive information from output files
   - Replace company information and contact details with sample data
   - Update with actual information when using

### Security Recommendations
1. Use `.gitignore` to exclude sensitive files:
```
.env
data/input/*
data/output/*
*.log
__pycache__/
```

2. Regularly update API keys
3. Do not commit files containing actual project information
4. Use encrypted storage for sensitive information

## Troubleshooting

1. Mermaid Flowchart Issues:
   - Ensure Mermaid CLI is properly installed
   - Check if `mmdc` command is in system path
   - Verify Node.js version compatibility

2. PDF Processing Issues:
   - Ensure PyPDF2 is properly installed
   - Check if PDF file is encrypted
   - Verify PDF file integrity

3. API Connection Issues:
   - Check API key and base URL in `.env` file
   - Check network connection
   - Ensure API endpoint is accessible

## Important Notes

1. Ensure tender files are UTF-8 encoded
2. Generated bid content is for reference only, please review manually before use
3. Keep API keys secure and do not share with others
4. Regularly backup generated bid documents
5. Please read and agree to the open source license before use

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Main terms of the MIT License:
- Allows anyone to freely use, modify, and distribute the software
- Requires retention of original copyright notice and license
- Provides no express or implied warranties
- Author is not liable for any damages from using the software

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines
- Follow PEP 8 coding standards
- Add appropriate comments and documentation
- Ensure all tests pass
- Update relevant documentation

## Acknowledgments

- [DeepSeek](https://deepseek.com) - For providing the AI API service
- [Mermaid](https://mermaid.js.org/) - For providing flowchart generation functionality
- All developers who have contributed to this project 