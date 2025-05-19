import os
from pathlib import Path
from deepseek_client import DeepSeekClient
from tqdm import tqdm
import PyPDF2
import re
import openai
from md_to_word import convert_md_to_word

class BidGenerator:
    def __init__(self):
        self.client = DeepSeekClient()
        self.config = self.client.config
        
    def read_tender_file(self, file_path):
        """读取招标文件内容"""
        file_path = Path(file_path)
        if file_path.suffix.lower() == '.pdf':
            return self._read_pdf(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    
    def _read_pdf(self, file_path):
        """读取PDF文件内容"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def extract_sections(self, tender_content):
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
        
        requirements_response = openai.ChatCompletion.create(
            model=self.client.config["api"]["model"],
            messages=[
                {"role": "system", "content": "你是一个专业的标书结构分析专家，擅长提取招标文件中的编制要求。"},
                {"role": "user", "content": requirements_prompt}
            ],
            temperature=0.2,
            max_tokens=1000,
            top_p=0.9
        )
        requirements = requirements_response["choices"][0]["message"]["content"]
        
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
        
        industry_response = openai.ChatCompletion.create(
            model=self.client.config["api"]["model"],
            messages=[
                {"role": "system", "content": "你是一个专业的标书结构设计专家，擅长根据行业特点设计完整的标书结构。"},
                {"role": "user", "content": industry_prompt}
            ],
            temperature=0.3,
            max_tokens=1000,
            top_p=0.9
        )
        
        industry_suggestions = industry_response["choices"][0]["message"]["content"]
        
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
        
        final_response = openai.ChatCompletion.create(
            model=self.client.config["api"]["model"],
            messages=[
                {"role": "system", "content": "你是一个专业的标书结构优化专家，擅长整合和优化标书章节结构。"},
                {"role": "user", "content": final_prompt}
            ],
            temperature=0.2,
            max_tokens=1000,
            top_p=0.9
        )
        
        raw = final_response["choices"][0]["message"]["content"]
        # 解析章节名
        sections = [re.sub(r'^[0-9一二三四五六七八九十\.\、\s]+', '', line).strip() for line in raw.splitlines() if line.strip()]
        return [s for s in sections if s]
    
    def save_bid_section(self, content, section_name, output_dir, tender_name):
        """保存生成的标书章节"""
        output_path = Path(output_dir) / tender_name / f"{section_name}.txt"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def merge_sections(self, output_dir, tender_name):
        """合并所有章节内容为一个完整的文档"""
        sections_dir = Path(output_dir) / tender_name
        if not sections_dir.exists():
            print(f"目录 {sections_dir} 不存在！")
            return
        
        # 获取所有章节文件
        section_files = list(sections_dir.glob("*.txt"))
        if not section_files:
            print(f"在 {sections_dir} 目录下未找到章节文件！")
            return
        
        # 按章节顺序排序
        section_order = [
            "封面与目录",
            "投标函部分",
            "技术方案",
            "实施方案",
            "售后服务方案",
            "商务部分",
            "报价部分",
            "其他必要文件",
            "格式附件"
        ]
        
        # 创建合并后的文档
        merged_content = []
        merged_content.append("# 智慧工程项目管理平台智能化软件、硬件系统投标文件\n\n")
        
        # 按顺序合并章节
        for section_name in section_order:
            section_file = sections_dir / f"{section_name}.txt"
            if section_file.exists():
                with open(section_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    merged_content.append(f"## {section_name}\n\n")
                    merged_content.append(content)
                    merged_content.append("\n\n")
        
        # 保存合并后的文档
        output_file = sections_dir / f"{tender_name}_完整投标文件.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(merged_content))
        
        print(f"已生成完整投标文件：{output_file}")
        return output_file

    def generate_bid_document(self, tender_file):
        """生成完整的标书"""
        # 读取招标文件
        tender_content = self.read_tender_file(tender_file)
        tender_name = Path(tender_file).stem
        
        # 自动提取章节
        sections = self.extract_sections(tender_content)
        if not sections:
            print(f"未能自动识别到章节，请检查招标文件格式。")
            return
        print(f"自动识别到以下章节：{sections}")
        
        # 生成每个章节
        for section in tqdm(sections, desc=f"生成标书章节 - {tender_name}"):
            content = self.client.generate_bid_document(tender_content, section)
            self.save_bid_section(
                content,
                section,
                self.config["paths"]["output_dir"],
                tender_name
            )
        
        # 合并所有章节
        merged_file = self.merge_sections(self.config["paths"]["output_dir"], tender_name)
        
        # 转换为Word文档
        if merged_file:
            convert_md_to_word()
        
        print(f"标书生成完成！输出目录：{self.config['paths']['output_dir']}/{tender_name}")

def main():
    generator = BidGenerator()
    
    # 获取输入目录中的所有招标文件
    input_dir = Path(generator.config["paths"]["input_dir"])
    tender_files = list(input_dir.glob("*.pdf")) + list(input_dir.glob("*.txt"))
    
    if not tender_files:
        print(f"在 {input_dir} 目录下未找到招标文件！")
        return
    
    # 处理每个招标文件
    for tender_file in tender_files:
        print(f"\n处理招标文件：{tender_file.name}")
        generator.generate_bid_document(tender_file)

if __name__ == "__main__":
    main() 