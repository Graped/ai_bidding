# AI 标书生成系统

[English](README.md) | [中文](README_CN.md)

本项目基于 DeepSeek API 自动生成专业标书文档。支持 PDF 和文本格式的招标文件输入，并生成完整的 Word 格式标书。

## 功能特点

- 自动分析招标文件并提取要求
- 基于行业标准智能生成章节内容
- 支持 PDF 和文本格式的招标文件
- 自动转换为 Word 格式并保持专业排版
- 专业的文档结构，包含页眉页脚和样式
- 支持表格、图片和流程图
- 内容质量检查和优化

## 系统要求

- Python 3.8 或更高版本
- Node.js 16.0 或更高版本（用于 Mermaid 流程图支持）
- Mermaid CLI（用于流程图生成）

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/Graped/ai_bidding.git
cd ai_bidding
```

2. 创建并激活虚拟环境：
```bash
# Windows 系统
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux 系统
python -m venv venv
source venv/bin/activate
```

3. 安装 Python 依赖：
```bash
pip install -r requirements.txt
```

4. 安装 Mermaid CLI（用于流程图生成）：
```bash
# 使用 npm
npm install -g @mermaid-js/mermaid-cli

# 使用 yarn
yarn global add @mermaid-js/mermaid-cli
```

5. 在项目根目录创建 `.env` 文件，配置 API 信息：
```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
```

6. 创建 `config/config.yaml` 配置文件：
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

## 使用方法

1. 准备项目目录结构：
```bash
mkdir -p data/input data/output
```

2. 将招标文件（PDF 或文本格式）放入 `data/input` 目录。

3. 运行生成器：
```bash
# 在项目根目录下执行
python src/main.py
```

4. 生成的标书将保存在 `data/output` 目录中，按招标项目名称分类。

## 输出结构

生成的标书包含以下内容：

- 封面（包含项目详情）
- 目录
- 投标函
- 技术方案
- 实施方案
- 售后服务方案
- 商务部分
- 报价部分
- 必要附件
- 格式附件

## 软件版本

项目已测试的版本信息：

### Python 依赖包
- openai==1.12.0
- python-dotenv==1.0.0
- PyPDF2==3.0.1
- tqdm==4.66.1
- markdown==3.4.3
- python-docx==0.8.11
- PyYAML==6.0.1

### 系统要求
- Python 3.8.10 或更高版本
- Node.js 16.20.0 或更高版本
- Mermaid CLI 10.6.1 或更高版本

## 数据安全

### 敏感信息处理
1. API 密钥
   - 使用环境变量存储 API 密钥
   - 不要将 `.env` 文件提交到版本控制系统
   - 在示例中使用占位符（如 `sk-xxxxxxxx`）

2. 招标文件
   - 示例文件中的敏感信息已脱敏
   - 项目名称、金额等关键信息已替换为示例数据
   - 建议在使用时替换为实际项目信息

3. 生成的标书
   - 输出文件中的敏感信息已脱敏
   - 公司信息、联系方式等已替换为示例数据
   - 建议在使用时更新为实际信息

### 安全建议
1. 使用 `.gitignore` 排除敏感文件：
```
.env
data/input/*
data/output/*
*.log
__pycache__/
```

2. 定期更新 API 密钥
3. 不要将包含实际项目信息的文件提交到仓库
4. 使用加密存储敏感信息

## 常见问题解决

1. Mermaid 流程图相关问题：
   - 确保 Mermaid CLI 正确安装
   - 检查 `mmdc` 命令是否在系统路径中
   - 验证 Node.js 版本是否兼容

2. PDF 处理问题：
   - 确保 PyPDF2 正确安装
   - 检查 PDF 文件是否加密
   - 验证 PDF 文件是否损坏

3. API 连接问题：
   - 检查 `.env` 文件中的 API 密钥和基础 URL
   - 检查网络连接
   - 确保 API 端点可访问

## 注意事项

1. 请确保招标文件为 UTF-8 编码
2. 生成的标书内容仅供参考，建议人工审核后再使用
3. 请妥善保管 API 密钥，不要泄露给他人
4. 建议定期备份生成的标书文件
5. 使用前请确保已阅读并同意开源协议

## 开源协议

本项目采用 MIT 许可证。详情请查看 [LICENSE](LICENSE) 文件。

MIT 许可证的主要条款：
- 允许任何人自由使用、修改和分发本软件
- 要求保留原始版权声明和许可证
- 不提供任何明示或暗示的保证
- 作者不对使用本软件造成的任何损失负责

## 贡献指南

1. Fork 本仓库
2. 创建新的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 贡献规范
- 遵循 PEP 8 编码规范
- 添加适当的注释和文档
- 确保所有测试通过
- 更新相关文档

## 致谢

- [DeepSeek](https://deepseek.com) - 提供 AI API 服务
- [Mermaid](https://mermaid.js.org/) - 提供流程图生成功能
- 所有为本项目做出贡献的开发者 