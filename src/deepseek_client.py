import os
import yaml
import openai
from pathlib import Path
from dotenv import load_dotenv

class DeepSeekClient:
    def __init__(self, config_path="config/config.yaml"):
        self.config = self._load_config(config_path)
        openai.api_key = self.config["api"]["api_key"]
        openai.api_base = self.config["api"]["base_url"]
        
    def _load_config(self, config_path):
        config_file = Path(__file__).parent.parent / config_path
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def generate_bid_document(self, tender_content, section_name):
        """
        根据招标文件内容生成标书特定章节
        
        Args:
            tender_content (str): 招标文件内容
            section_name (str): 需要生成的章节名称
            
        Returns:
            str: 生成的标书章节内容
        """
        # 首先分析招标文件中的相关要求
        analysis_prompt = f"""请仔细分析以下招标文件中与"{section_name}"相关的要求和重点：
1. 找出所有明确的要求和标准
2. 识别隐含的期望和关注点
3. 总结关键的技术指标和参数
4. 列出需要特别注意的要点

招标文件内容：
{tender_content[:4000]}  # 限制长度以避免超出token限制
"""
        
        try:
            # 分析招标文件要求
            analysis_response = openai.ChatCompletion.create(
                model=self.config["api"]["model"],
                messages=[
                    {"role": "system", "content": "你是一个专业的标书分析专家，擅长提取招标文件中的关键要求。"},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.2,
                max_tokens=1000,
                top_p=0.9
            )
            
            requirements = analysis_response["choices"][0]["message"]["content"]
            
            # 生成章节内容
            generation_prompt = f"""基于以下招标文件要求和分析，生成标书的{section_name}章节：

招标文件要求分析：
{requirements}

生成要求：
1. 内容必须严格符合招标文件的要求
2. 语言要专业、规范、准确
3. 格式要清晰、层次分明
4. 突出我们的优势和特点
5. 确保所有关键要求都得到响应
6. 使用具体的数据和案例支持论述

请生成完整的章节内容。
"""
            
            response = openai.ChatCompletion.create(
                model=self.config["api"]["model"],
                messages=[
                    {"role": "system", "content": "你是一个专业的标书撰写专家，擅长根据招标文件生成高质量的标书内容。"},
                    {"role": "user", "content": generation_prompt}
                ],
                temperature=self.config["generation"]["temperature"],
                max_tokens=self.config["generation"]["max_tokens"],
                top_p=self.config["generation"]["top_p"]
            )
            
            content = response["choices"][0]["message"]["content"]
            
            # 内容质量检查
            check_prompt = f"""请检查以下生成的标书章节内容是否符合要求：

章节名称：{section_name}
生成内容：
{content}

请检查：
1. 是否完整响应了招标文件的要求
2. 内容是否专业、规范
3. 格式是否清晰
4. 是否有遗漏的重要信息

如果发现问题，请指出具体问题并提供改进建议。
"""
            
            check_response = openai.ChatCompletion.create(
                model=self.config["api"]["model"],
                messages=[
                    {"role": "system", "content": "你是一个专业的标书质量检查专家。"},
                    {"role": "user", "content": check_prompt}
                ],
                temperature=0.2,
                max_tokens=1000,
                top_p=0.9
            )
            
            quality_check = check_response["choices"][0]["message"]["content"]
            
            # 如果发现问题，进行优化
            if "问题" in quality_check or "建议" in quality_check:
                optimization_prompt = f"""根据以下质量检查结果，优化标书章节内容：

原始内容：
{content}

质量检查结果：
{quality_check}

请根据检查结果优化内容，确保符合所有要求。
"""
                
                optimization_response = openai.ChatCompletion.create(
                    model=self.config["api"]["model"],
                    messages=[
                        {"role": "system", "content": "你是一个专业的标书优化专家。"},
                        {"role": "user", "content": optimization_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=self.config["generation"]["max_tokens"],
                    top_p=0.9
                )
                
                content = optimization_response["choices"][0]["message"]["content"]
            
            return content
            
        except Exception as e:
            print(f"生成标书章节时出错: {str(e)}")
            return f"生成{section_name}章节时出错，请检查API配置和网络连接。"

    def generate_content(self, prompt, max_tokens=2000):
        try:
            response = openai.ChatCompletion.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的标书撰写专家，擅长根据招标文件生成高质量的投标文件。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return None 