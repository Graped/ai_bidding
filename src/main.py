import os
from pathlib import Path
from deepseek_client import DeepSeekClient
from tqdm import tqdm
import PyPDF2
import re
from openai import OpenAI
from md_to_word import convert_md_to_word
import logging
import asyncio
import concurrent.futures

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BidGenerator:
    def __init__(self):
        self.client = DeepSeekClient()
        self.config = self.client.config
        self.openai_client = OpenAI(
            api_key=self.config["api"]["api_key"],
            base_url=self.config["api"]["base_url"]
        )
        
    async def read_tender_file(self, file_path):
        """读取招标文件内容"""
        file_path = Path(file_path)
        try:
            if file_path.suffix.lower() == '.pdf':
                return await self._read_pdf(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            logging.error(f"读取文件 {file_path} 时出错: {e}")
            return None
    
    async def _read_pdf(self, file_path):
        """读取PDF文件内容"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logging.error(f"读取PDF文件 {file_path} 时出错: {e}")
            return None
    
    async def extract_sections(self, tender_content):
        """
        利用大模型自动分析招标文件，优先根据"投标文件编制要求"或类似要求，推理应包含的全部章节目录。
        """
        # 第一步：分析招标文件中的明确要求
        requirements_prompt = (
            "请仔细分析以下招标文件内容，找出所有关于'投标文件编制要求'、'标书结构要求'、"
            "'投标文件组成'等相关内容。重点关注：\n"
            "1. 明确要求的章节和内容\n"
            "2. 必须包含的文件和材料\n"
            "3. 特殊的格式或结构要求\n"
            "4. 评分标准中提到的重点内容\n\n"
            "招标文件内容：\n" + tender_content[:4000]
        )
        
        requirements = await self._get_openai_response(requirements_prompt, "你是一个专业的标书结构分析专家，擅长提取招标文件中的编制要求。")
        
        # 第二步：根据行业特点和招标内容补充必要章节
        industry_prompt = (
            f"基于以下招标文件要求和行业经验，请补充必要的章节：\n\n"
            f"招标文件要求：\n{requirements}\n\n"
            "请考虑：\n"
            "1. 技术方案相关章节\n"
            "2. 商务相关章节\n"
            "3. 资质证明相关章节\n"
            "4. 项目管理相关章节\n"
            "5. 其他必要的补充章节\n\n"
            "请列出所有必要的章节，并说明每个章节的必要性。"
        )
        
        industry_suggestions = await self._get_openai_response(industry_prompt, "你是一个专业的标书结构设计专家，擅长根据行业特点设计完整的标书结构。")
        
        # 第三步：整合和优化章节结构
        final_prompt = (
            f"请根据以下信息，整理出最终的标书章节结构：\n\n"
            f"招标文件要求：\n{requirements}\n\n"
            f"行业建议：\n{industry_suggestions}\n\n"
            "请：\n"
            "1. 合并重复的章节\n"
            "2. 按照逻辑顺序排列章节\n"
            "3. 确保章节名称规范统一\n"
            "4. 只返回最终的章节名称列表，每行一个章节名\n"
        )
        
        final_response = await self._get_openai_response(final_prompt, "你是一个专业的标书结构优化专家，擅长整合和优化标书章节结构。")
        
        raw = final_response
        # 解析章节名
        sections = [re.sub(r'^[0-9一二三四五六七八九十\.\、\s]+', '', line).strip() for line in raw.splitlines() if line.strip()]
        return [s for s in sections if s]
    
    async def _get_openai_response(self, prompt, system_content):
        """获取OpenAI API的响应"""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.config["api"]["model"],
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1000,
                top_p=0.9
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"调用OpenAI API时出错: {e}")
            return None
    
    def save_bid_section(self, content, section_name, output_dir, tender_name):
        """保存生成的标书章节"""
        output_path = Path(output_dir) / tender_name / f"{section_name}.txt"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            logging.error(f"保存章节 {section_name} 时出错: {e}")
    
    def merge_sections(self, output_dir, tender_name, sections):
        """合并所有章节内容为一个完整的文档"""
        sections_dir = Path(output_dir) / tender_name
        if not sections_dir.exists():
            logging.error(f"目录 {sections_dir} 不存在！")
            return
        
        # 获取所有章节文件
        section_files = list(sections_dir.glob("*.txt"))
        if not section_files:
            logging.error(f"在 {sections_dir} 目录下未找到章节文件！")
            return
        
        # 创建合并后的文档
        merged_content = ["# 投标文件\n\n"] + [
            f"## {section_name}\n\n{content}\n\n"
            for section_name in sections
            if (section_file := sections_dir / f"{section_name}.txt").exists()
            for content in [section_file.read_text(encoding='utf-8')]
        ]
        
        # 保存合并后的文档
        output_file = sections_dir / f"{tender_name}_完整投标文件.md"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(merged_content))
            logging.info(f"已生成完整投标文件：{output_file}")
            return output_file
        except Exception as e:
            logging.error(f"保存合并文件时出错: {e}")
            return None

    async def generate_bid_document(self, tender_file):
        """生成完整的标书"""
        tender_name = Path(tender_file).stem
        markdown_file = Path(self.config["paths"]["output_dir"]) / tender_name / f"{tender_name}_完整投标文件.md"
        if markdown_file.exists():
            logging.info(f"已存在生成的 Markdown 文件，直接调用转换函数。")
            convert_md_to_word(markdown_file)
            return
        # 读取招标文件
        tender_content = await self.read_tender_file(tender_file)
        if tender_content is None:
            logging.error(f"无法读取招标文件 {tender_file}。")
            return
        
        # 自动提取章节
        sections = await self.extract_sections(tender_content)
        if not sections:
            logging.error(f"未能自动识别到章节，请检查招标文件格式。")
            return
        logging.info(f"自动识别到以下章节：{sections}")
        
        # 生成每个章节
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.client.generate_bid_document, tender_content, section) for section in sections]
            retry_count = 0
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(sections), desc=f"正在进行标书章节生成 - {tender_name}"):
                try:
                    content = future.result()
                    self.save_bid_section(
                        content,
                        sections[futures.index(future)],
                        self.config["paths"]["output_dir"],
                        tender_name
                    )
                    logging.info(f"正在生成章节：{sections[futures.index(future)]}，进度：{futures.index(future) + 1}/{len(sections)} ({((futures.index(future) + 1) / len(sections) * 100):.2f}%)")
                except Exception as e:
                    retry_count += 1
                    logging.error(f"生成章节时出错：{e}，重试次数：{retry_count}")
                    if retry_count >= 10:
                        logging.error("重试次数超过10次，退出程序。")
                        return
        
        # 合并所有章节
        merged_file = self.merge_sections(self.config["paths"]["output_dir"], tender_name, sections)
        
        # 转换为Word文档
        if merged_file:
            # 检查是否已经存在生成的 Markdown 文件
            markdown_file = Path(self.config["paths"]["output_dir"]) / tender_name / f"{tender_name}_完整投标文件.md"
            if markdown_file.exists():
                logging.info(f"已存在生成的 Markdown 文件，直接调用转换函数。")
                convert_md_to_word(markdown_file)
            else:
                convert_md_to_word(markdown_file)
        
        logging.info(f"标书生成完成！输出目录：{self.config['paths']['output_dir']}/{tender_name}")

async def main():
    generator = BidGenerator()
    
    # 获取输入目录中的所有招标文件
    input_dir = Path(generator.config["paths"]["input_dir"])
    tender_files = list(input_dir.glob("*.pdf")) + list(input_dir.glob("*.txt"))
    
    if not tender_files:
        logging.error(f"在 {input_dir} 目录下未找到招标文件！")
        return
    
    # 处理每个招标文件
    for tender_file in tender_files:
        logging.info(f"\n处理招标文件：{tender_file.name}")
        await generator.generate_bid_document(tender_file)

if __name__ == "__main__":
    asyncio.run(main()) 