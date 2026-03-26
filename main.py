import json
import requests
import datetime
from typing import Dict, Any, List

class IntelligentRecruitmentAssistant:
    """智能招聘助手核心类"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1/chat/completions"):
        """
        初始化助手
        :param api_key: 大模型API密钥
        :param base_url: API基础URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def parse_document(self, document_text: str, doc_type: str) -> Dict[str, Any]:
        """
        解析文档（JD或简历），提取关键信息
        :param document_text: 文档文本内容
        :param doc_type: 文档类型 ('jd' 或 'resume')
        :return: 解析后的结构化信息
        """
        prompt = ""
        if doc_type == "jd":
            prompt = f"请从以下招聘需求中提取关键信息，包括职位名称、技能要求、经验要求、学历要求等，以JSON格式返回:\n{document_text}"
        else:
            prompt = f"请从以下简历中提取关键信息，包括姓名、技能、工作经验、教育背景等，以JSON格式返回:\n{document_text}"
        
        response = self._call_llm(prompt)
        
        try:
            # 尝试解析返回的JSON
            parsed_data = json.loads(response)
        except json.JSONDecodeError:
            # 如果返回的不是标准JSON，返回原始文本
            parsed_data = {"raw_text": response, "doc_type": doc_type}
        
        return parsed_data
    
    def calculate_match_score(self, jd_data: Dict[str, Any], resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算JD与简历的匹配度
        :param jd_data: JD解析数据
        :param resume_data: 简历解析数据
        :return: 匹配度评估结果
        """
        prompt = f"""
        请评估以下职位需求与候选人简历的匹配度：
        
        职位需求：
        {json.dumps(jd_data, ensure_ascii=False, indent=2)}
        
        候选人简历：
        {json.dumps(resume_data, ensure_ascii=False, indent=2)}
        
        请从以下维度进行评估（总分100分）：
        1. 技能匹配度（0-40分）
        2. 经验匹配度（0-30分）
        3. 教育背景匹配度（0-20分）
        4. 综合潜力（0-10分）
        
        请以JSON格式返回，包含：total_score（总分）、dimension_scores（各维度分数）、strengths（优势）、weaknesses（不足）、recommendation（推荐意见）。
        """
        
        response = self._call_llm(prompt)
        
        try:
            match_result = json.loads(response)
        except json.JSONDecodeError:
            match_result = {
                "total_score": 0,
                "dimension_scores": {},
                "strengths": ["无法解析评估结果"],
                "weaknesses": ["数据格式异常"],
                "recommendation": "请手动评估"
            }
        
        return match_result
    
    def generate_report(self, jd_text: str, resume_text: str, match_result: Dict[str, Any]) -> str:
        """
        生成评估报告
        :param jd_text: JD原始文本
        :param resume_text: 简历原始文本
        :param match_result: 匹配度结果
        :return: 完整的评估报告
        """
        report_date = datetime.datetime.now().strftime("%Y年%m月%d日")
        
        report = f"""
        ========== 智能招聘评估报告 ==========
        
        生成时间：{report_date}
        评估工具：智能招聘助手Demo v1.0
        
        【职位需求摘要】
        {jd_text[:500]}...
        
        【候选人简历摘要】
        {resume_text[:500]}...
        
        【匹配度评估结果】
        总分：{match_result.get('total_score', 0)}/100
        
        各维度得分：
        {json.dumps(match_result.get('dimension_scores', {}), ensure_ascii=False, indent=2)}
        
        【优势分析】
        {chr(10).join(f'- {item}' for item in match_result.get('strengths', []))}
        
        【不足分析】
        {chr(10).join(f'- {item}' for item in match_result.get('weaknesses', []))}
        
        【推荐意见】
        {match_result.get('recommendation', '暂无推荐意见')}
        
        ========== 报告结束 ==========
        """
        
        return report
    
    def _call_llm(self, prompt: str) -> str:
        """
        调用大模型API
        :param prompt: 提示词
        :return: 模型响应文本
        """
        # 注意：这里使用模拟响应，实际使用时需要替换为真实API调用
        # 实际API调用代码示例（注释状态）：
        """
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"API调用失败: {str(e)}"
        """
        
        # 模拟响应（用于演示）
        if "提取关键信息" in prompt:
            if "招聘需求" in prompt:
                return json.dumps({
                    "position": "Python开发工程师",
                    "skills": ["Python", "Django", "MySQL", "Redis"],
                    "experience": "3年以上",
                    "education": "本科及以上",
                    "requirements": "熟悉Web开发，有AI项目经验者优先"
                }, ensure_ascii=False)
            else:
                return json.dumps({
                    "name": "张三",
                    "skills": ["Python", "Django", "MySQL"],
                    "experience": "2年Python开发经验",
                    "education": "计算机科学本科",
                    "projects": ["电商系统开发", "数据分析平台"]
                }, ensure_ascii=False)
        else:
            return json.dumps({
                "total_score": 78,
                "dimension_scores": {
                    "技能匹配度": 32,
                    "经验匹配度": 25,
                    "教育背景匹配度": 16,
                    "综合潜力": 5
                },
                "strengths": ["Python技能匹配度高", "有相关项目经验", "教育背景符合要求"],
                "weaknesses": ["经验年限略不足", "缺少Redis使用经验"],
                "recommendation": "建议进入面试环节，重点关注项目经验和学习能力"
            }, ensure_ascii=False)

def main():
    """主函数：演示智能招聘助手核心功能"""
    
    print("🚀 智能招聘助手Demo启动...")
    print("=" * 50)
    
    # 初始化助手（使用模拟API，实际需要替换为真实API密钥）
    assistant = IntelligentRecruitmentAssistant(api_key="sk-mock-api-key-for-demo")
    
    # 示例数据
    jd_text = """
    职位：Python开发工程师
    要求：
    1. 3年以上Python开发经验
    2. 熟悉Django/Flask框架
    3. 掌握MySQL、Redis等数据库
    4. 有AI项目经验者优先
    5. 本科及以上学历，计算机相关专业
    """
    
    resume_text = """
    姓名：张三
    教育背景：计算机科学本科，XX大学
    工作经验：2年Python开发工程师，参与过电商系统和数据分析平台开发
    技能：Python, Django, MySQL, JavaScript
    项目经验：
    1. 电商系统后端开发（使用Django）
    2. 数据分析平台（Python数据处理）
    """
    
    print("📋 正在解析职位需求...")
    jd_data = assistant.parse_document(jd_text, "jd")
    print(f"职位需求解析完成: {jd_data.get('position', '未知职位')}")
    
    print("\n📄 正在解析候选人简历...")
    resume_data = assistant.parse_document(resume_text, "resume")
    print(f"简历解析完成: {resume_data.get('name', '未知候选人')}")
    
    print("\n🔍 正在计算匹配度...")
    match_result = assistant.calculate_match_score(jd_data, resume_data)
    print(f"匹配度计算完成，总分: {match_result.get('total_score', 0)}/100")
    
    print("\n📊 正在生成评估报告...")
    report = assistant.generate_report(jd_text, resume_text, match_result)
    
    print("\n" + "=" * 50)
    print("✅ 评估报告生成完成！")
    print("=" * 50)
    print(report)
    
    # 保存报告到文件
    with open("recruitment_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n💾 报告已保存至: recruitment_report.txt")

if __name__ == "__main__":
    main()