# Anki Card Agent

基于 Claude Agent SDK 的智能 Anki 学习卡片生成器。

## 功能特性

- 🤖 **AI 驱动**：使用 Claude/GLM 模型自动生成高质量学习卡片
- 📚 **多种卡片类型**：支持问答 (Q&A)、填空 和选择题 (MCQ)
- 🔍 **网络搜索**：内置网页搜索和内容抓取能力，获取权威学习资料
- 🌐 **Web 界面**：提供友好的 Web 界面，实时显示生成进度
- 💻 **CLI 模式**：支持命令行快速生成
- 📦 **一键导出**：生成标准的 .apkg 文件，可直接导入 Anki

## 技术栈

- **Python 3.13+**
- **Claude Agent SDK**：AI Agent 核心框架
- **FastAPI**：Web 服务器
- **Genanki**：Anki 卡片包生成

## 安装

```bash
# 克隆项目
git clone <repository-url>
cd anki-card-agent

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -e .
```

## 使用方式

### Web 模式（推荐）

```bash
uvicorn web:app --host 127.0.0.1 --port 8000
```

然后在浏览器中访问 `http://localhost:8000`

### CLI 模式

```bash
python cli.py "小学一年级英语单词" --verbose
```

参数说明：
- `prompt`：您希望生成卡片的主题或问题
- `--verbose`：显示详细的工具调用日志

## 卡片格式

Agent 支持以下卡片格式：

### 问答卡片 (Q&A)
```
问题||答案
```

### 填空卡片
```
Python 是{{c1::一种编程语言}}，由{{c2::Guido van Rossum}}创建。
```

### 选择题
```
问题||选项 A|选项 B|选项 C|选项 D||正确答案
```



## 项目结构

```
anki-card-agent/
├── agent.py          # Claude Agent 示例
├── core.py           # 核心逻辑
├── web.py            # Web 服务器
├── cli.py            # 命令行接口
├── tools.py          # MCP 工具定义
├── prompt.txt        # 系统提示词
├── static/           # Web 静态文件
└── tests/            # 测试文件
```

## License

MIT