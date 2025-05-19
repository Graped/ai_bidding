from pathlib import Path

def merge_sections():
    # 设置目录路径
    base_dir = Path("data/output/智慧工程项目管理平台智能化软件、硬件系统招标文件")
    
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
        section_file = base_dir / f"{section_name}.txt"
        if section_file.exists():
            with open(section_file, 'r', encoding='utf-8') as f:
                content = f.read()
                merged_content.append(f"## {section_name}\n\n")
                merged_content.append(content)
                merged_content.append("\n\n")
    
    # 保存合并后的文档
    output_file = base_dir / "完整投标文件.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(merged_content))
    
    print(f"已生成完整投标文件：{output_file}")

if __name__ == "__main__":
    merge_sections() 