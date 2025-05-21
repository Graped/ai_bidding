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
- Markdown to Word conversion with formatting preservation
- Support for bold text, tables, and lists
- Dynamic project name in headers and footers

## System Requirements

- Python 3.8 or higher
- Node.js 16.0 or higher (for Mermaid flowchart support)
- Mermaid CLI (for flowchart generation)
- UV (Python package installer and resolver)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Graped/ai_bidding.git
cd ai_bidding
```

2. Install UV if not already installed:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Create and activate a virtual environment using UV:
```bash
# Create virtual environment
uv venv

# Activate virtual environment
# Windows
.venv/Scripts/activate

# macOS/Linux
source .venv/bin/activate
```

4. Install Python dependencies using UV:
```bash
uv pip install -r requirements.txt
```

5. Install Mermaid CLI (for flowchart generation):
```bash
# Using npm
npm install -g @mermaid-js/mermaid-cli

# Using yarn
yarn global add @mermaid-js/mermaid-cli
```

6. Create the `config/config.yaml` configuration file:
```yaml
api:
  api_key: "your-api-key-here"  # Replace with your actual API key
  base_url: "https://api.deepseek.com/v1"
  model: "deepseek-chat"
  temperature: 0.7
  max_tokens: 2000
  top_p: 0.9

paths:
  input_dir: "data/input"
  output_dir: "data/output"
```

> **Important**: The `config.yaml` file contains sensitive information and is ignored by git. You need to create your own `config.yaml` file in the `config` directory and replace the API key with your actual key.

## Project Structure

```
ai_bidding/
├── config/
│   └── config.yaml          # Configuration file
├── data/
│   ├── input/              # Input tender files
│   └── output/             # Generated bid documents
├── src/
│   ├── main.py            # Main program entry
│   ├── deepseek_client.py # DeepSeek API client
│   └── md_to_word.py      # Markdown to Word converter
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```

## Implementation Principles

### 1. Document Processing Flow
1. **Input Processing**
   - Read tender files (PDF/TXT) from the input directory
   - Extract text content using PyPDF2 for PDF files
   - Support UTF-8 encoded text files

2. **Content Analysis**
   - Use DeepSeek API to analyze tender requirements
   - Extract key requirements and evaluation criteria
   - Identify implicit expectations and focus points

3. **Content Generation**
   - Generate bid document sections based on analysis
   - Ensure compliance with tender requirements
   - Maintain professional language and formatting

4. **Quality Control**
   - Perform content quality checks
   - Verify requirement coverage
   - Optimize content based on feedback

### 2. Core Components
1. **DeepSeekClient (`deepseek_client.py`)**
   - Handles API communication with DeepSeek
   - Manages content generation and optimization
   - Implements retry mechanism for API calls

2. **Document Converter (`md_to_word.py`)**
   - Converts Markdown to Word format
   - Maintains professional formatting
   - Supports tables, images, and flowcharts
   - Handles headers, footers, and page numbers

3. **Main Program (`main.py`)**
   - Orchestrates the document generation process
   - Manages file operations and directory structure
   - Handles concurrent processing of sections

### 3. Key Features Implementation
1. **Table Support**
   - Automatic conversion of Markdown tables to Word format
   - Maintains table structure and formatting
   - Supports merged cells and custom styles

2. **Image and Flowchart Handling**
   - Converts Mermaid diagrams to images
   - Embeds images in Word documents
   - Maintains image quality and positioning

3. **Formatting Preservation**
   - Maintains consistent font styles (SimSun/SimHei)
   - Preserves heading levels and hierarchy
   - Handles lists and indentation properly

4. **Dynamic Headers/Footers**
   - Extracts project name from directory structure
   - Updates headers with project information
   - Maintains consistent page numbering

### 4. Error Handling
1. **API Communication**
   - Implements retry mechanism for failed API calls
   - Handles rate limiting and timeouts
   - Provides meaningful error messages

2. **File Operations**
   - Validates input file formats
   - Handles file encoding issues
   - Manages temporary files and cleanup

3. **Content Generation**
   - Validates generated content
   - Handles partial generation failures
   - Provides fallback options

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

### Document Formatting

The generated Word document includes:

1. Professional Formatting
   - Consistent font styles (SimSun for body text, SimHei for headings)
   - Proper line spacing and paragraph spacing
   - Centered alignment for titles
   - Proper indentation for lists

2. Table Support
   - Automatic table conversion from Markdown
   - Centered alignment for table cells
   - Bold headers with SimHei font
   - Grid style for better readability

3. Text Formatting
   - Support for bold text using `**text**` in Markdown
   - Proper handling of bullet points and numbered lists
   - Consistent font sizes for different heading levels

4. Headers and Footers
   - Dynamic project name in headers
   - Page numbers in footers
   - Professional layout and spacing

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
   - Store API keys in config.yaml
   - Do not commit the config.yaml file to version control
   - Use placeholders in examples

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
config/config.yaml
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
   - Check API key and base URL in config.yaml
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