## KMS HACKATHON 2025


### TOPIC: KMS HACKATHON 2025


#### AGENTS
- **Generate Questions Agent**: This agent generates questions/sample answers based on CV + JD + Role
- **Feedback Agent**: This agent provides feedback on the Recoding of interviewings



#### INFRASTRUCTURE
- **AWS SAM**: AWS Serverless Application Model (SAM) is used to deploy the application.


- **UV Python Package Manager**: A lightweight package manager for Python projects, designed to simplify dependency management and packaging.

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```


### Additional Knowledge

# Strands Agents Framework - Hướng Dẫn Toàn Diện

## 1. Khái Niệm Cơ Bản

### Strands Agents là gì?
Strands Agents là một Python SDK mạnh mẽ để xây dựng các AI agent thông minh. Framework này cho phép tạo ra các agent có khả năng suy luận, sử dụng
công cụ và tương tác với môi trường bên ngoài.

### Các Thành Phần Cốt Lõi

#### 1. Agent (Tác nhân AI)
• Là thực thể trung tâm được định nghĩa bởi 3 yếu tố chính:
  • **Model**: Mô hình AI (Claude, GPT-4, v.v.)
  • **Tools**: Công cụ để mở rộng khả năng
  • **Prompts**: Hướng dẫn và ngữ cảnh

#### 2. Model (Mô hình AI)
• Hỗ trợ nhiều nhà cung cấp: Amazon Bedrock, Anthropic, OpenAI
• Mặc định: Claude 3.7 Sonnet trên Amazon Bedrock
• Có khả năng suy luận và sử dụng công cụ

#### 3. Tools (Công cụ)
• Cơ chế chính để mở rộng khả năng agent
• Cho phép tương tác với hệ thống bên ngoài
• Agent tự động quyết định khi nào sử dụng công cụ

#### 4. Prompts (Lời nhắc)
• System prompt và user messages
• Cách chính để giao tiếp với AI models

## 2. Cài Đặt và Thiết Lập

### Cài đặt packages
bash
pip install strands-agents>=0.1.0
pip install strands-agents-tools>=0.1.0


### Cấu trúc project cơ bản
my_agent/
├── __init__.py
├── agent.py
└── requirements.txt


## 3. Tạo Agent Đầu Tiên

### Agent cơ bản
python
from strands import Agent, tool
from strands_tools import calculator, current_time

# Định nghĩa công cụ tùy chỉnh
@tool
def letter_counter(word: str, letter: str) -> int:
    """
    Đếm số lần xuất hiện của một chữ cái trong từ.
    """
    return word.lower().count(letter.lower())

# Tạo agent
agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[calculator, current_time, letter_counter],
    system_prompt="Bạn là một trợ lý AI hữu ích"
)

# Sử dụng agent
agent("Tính 25 * 48 và cho biết thời gian hiện tại")


## 4. Multi-Agent Architecture (Kiến Trúc Đa Agent)

### Khái Niệm Multi-Agent
Multi-agent architecture là mô hình kiến trúc nơi nhiều agent chuyên biệt làm việc cùng nhau để giải quyết các vấn đề phức tạp.

### Ưu Điểm của Multi-Agent Architecture

#### **Modularity (Tính Mô-đun)**
• Mỗi agent có trách nhiệm riêng biệt
• Dễ phát triển, kiểm thử và bảo trì độc lập
• Có thể tái sử dụng trong các tình huống khác nhau

#### **Scalability (Khả Năng Mở Rộng)**
• Có thể scale từng agent riêng lẻ
• Phân phối tải công việc hiệu quả
• Thêm agent mới mà không ảnh hưởng hệ thống

#### **Specialization (Chuyên Môn Hóa)**
• Mỗi agent tối ưu cho một nhiệm vụ cụ thể
• Sử dụng model và tools phù hợp nhất
• Chất lượng đầu ra cao hơn

### Các Công Cụ Multi-Agent trong Strands

#### 1. Agent Graph
Tạo và quản lý đồ thị các agent:

python
from strands_tools import agent_graph

# Tạo workflow với nhiều agent
workflow_agent = Agent(
    tools=[agent_graph],
    system_prompt="Điều phối workflow giữa các agent"
)

# Định nghĩa luồng công việc
workflow_definition = """
1. Agent A phân tích dữ liệu đầu vào
2. Agent B xử lý kết quả từ Agent A
3. Agent C tạo báo cáo cuối cùng
"""

workflow_agent(f"Tạo workflow: {workflow_definition}")


#### 2. Swarm (Đàn Agent)
Điều phối nhiều AI agent trong một mạng lưới:

python
from strands_tools import swarm

# Agent điều phối swarm
swarm_coordinator = Agent(
    tools=[swarm],
    system_prompt="Điều phối đàn agent để giải quyết vấn đề phức tạp"
)

# Sử dụng swarm
swarm_coordinator("Phân tích báo cáo tài chính với 3 agent: phân tích số liệu, đánh giá rủi ro, và tạo khuyến nghị")


#### 3. Workflow
Tổ chức các quy trình tuần tự:

python
from strands_tools import workflow

# Agent quản lý workflow
workflow_manager = Agent(
    tools=[workflow],
    system_prompt="Quản lý quy trình công việc tuần tự"
)

# Định nghĩa workflow
workflow_steps = """
Bước 1: Thu thập dữ liệu
Bước 2: Làm sạch dữ liệu
Bước 3: Phân tích dữ liệu
Bước 4: Tạo báo cáo
"""

workflow_manager(f"Thực hiện workflow: {workflow_steps}")


## 5. Ví Dụ Multi-Agent Thực Tế: Interview Preparation System

Dựa trên project của bạn, đây là cách triển khai multi-agent architecture:

### Kiến Trúc Hệ Thống
python
# 1. Document Parser Agent
document_parser = Agent(
    model="claude-3-haiku",  # Model nhanh cho parsing
    tools=[file_read, editor],
    system_prompt="Chuyên gia phân tích và trích xuất nội dung từ tài liệu"
)

# 2. JD Analyzer Agent
jd_analyzer = Agent(
    model="claude-3-7-sonnet",  # Model mạnh cho phân tích
    tools=[],
    system_prompt="Chuyên gia phân tích job description và trích xuất yêu cầu"
)

# 3. CV Analyzer Agent
cv_analyzer = Agent(
    model="claude-3-7-sonnet",
    tools=[],
    system_prompt="Chuyên gia phân tích CV và đánh giá ứng viên"
)

# 4. Skills Matcher Agent
skills_matcher = Agent(
    model="claude-3-7-sonnet",
    tools=[calculator],
    system_prompt="Chuyên gia so sánh kỹ năng và tính điểm phù hợp"
)

# 5. Question Generator Agent
question_generator = Agent(
    model="claude-3-7-sonnet",
    tools=[],
    system_prompt="Chuyên gia tạo câu hỏi phỏng vấn theo cấp độ và vòng"
)

# 6. Answer Evaluator Agent
answer_evaluator = Agent(
    model="claude-3-7-sonnet",
    tools=[],
    system_prompt="Chuyên gia tạo tiêu chí đánh giá và câu trả lời mẫu"
)


### Orchestrator Agent (Agent Điều Phối)
python
from strands_tools import agent_graph, workflow

class InterviewPreparationSystem:
    def __init__(self):
        self.orchestrator = Agent(
            model="claude-3-7-sonnet",
            tools=[agent_graph, workflow],
            system_prompt="""
            Bạn là hệ thống điều phối chuẩn bị phỏng vấn.
            Nhiệm vụ: Điều phối 6 agent chuyên biệt để tạo ra
            gói chuẩn bị phỏng vấn hoàn chỉnh.
            """
        )

        # Khởi tạo các agent chuyên biệt
        self.agents = {
            'document_parser': document_parser,
            'jd_analyzer': jd_analyzer,
            'cv_analyzer': cv_analyzer,
            'skills_matcher': skills_matcher,
            'question_generator': question_generator,
            'answer_evaluator': answer_evaluator
        }

    async def prepare_interview(self, jd, cv, role, level, round_number):
        # Định nghĩa workflow
        workflow_definition = f"""
        1. document_parser: Parse JD và CV
        2. jd_analyzer: Phân tích job description
        3. cv_analyzer: Phân tích CV ứng viên
        4. skills_matcher: So sánh kỹ năng và tính điểm
        5. question_generator: Tạo câu hỏi cho {role} level {level} round {round_number}
        6. answer_evaluator: Tạo tiêu chí đánh giá
        """

        # Thực hiện workflow
        result = await self.orchestrator.arun(
            f"Thực hiện workflow chuẩn bị phỏng vấn: {workflow_definition}"
        )

        return result


## 6. Streaming và Event Handling

### Async Iterators (Bất Đồng Bộ)
python
import asyncio

async def process_streaming_response():
    agent = Agent(tools=[calculator])
    query = "Tính 25 * 48 và giải thích"

    # Lấy async iterator
    agent_stream = agent.stream_async(query)

    # Xử lý events theo thời gian thực
    async for event in agent_stream:
        if "data" in event:
            print(event["data"], end="", flush=True)
        elif "current_tool_use" in event:
            tool_name = event["current_tool_use"].get("name")
            print(f"\n[Đang sử dụng công cụ: {tool_name}]")

asyncio.run(process_streaming_response())


### Callback Handlers
python
import logging

logger = logging.getLogger("my_agent")

def callback_handler(**kwargs):
    if "data" in kwargs:
        logger.info(kwargs["data"])
    elif "current_tool_use" in kwargs:
        tool = kwargs["current_tool_use"]
        logger.info(f"Sử dụng công cụ: {tool.get('name')}")

agent = Agent(
    tools=[shell],
    callback_handler=callback_handler
)


## 7. Các Loại Tools (Công Cụ)

### Built-in Tools
python
from strands_tools import (
    # RAG & Memory
    retrieve,

    # File Operations
    editor, file_read, file_write,

    # Shell & System
    environment, shell,

    # Code Interpretation
    python_repl,

    # Web & Network
    http_request,

    # Multi-modal
    image_reader, generate_image,

    # AWS Services
    use_aws,

    # Utilities
    calculator, current_time,

    # Agents & Workflows
    agent_graph, swarm, workflow
)


### Custom Tools
python
@tool
def database_query(query: str) -> str:
    """Thực hiện truy vấn cơ sở dữ liệu"""
    # Logic truy vấn database
    return "Kết quả truy vấn"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Gửi email"""
    # Logic gửi email
    return f"Đã gửi email tới {to}"


### MCP (Model Context Protocol) Tools
python
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient

# Kết nối MCP server
mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(command="uvx", args=["server-name"])
))

with mcp_client:
    tools = mcp_client.list_tools_sync()
    agent = Agent(tools=tools)


## 8. Model Providers (Nhà Cung Cấp Mô Hình)

### Amazon Bedrock (Mặc định)
python
from strands.models import BedrockModel

bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name='us-west-2',
    temperature=0.3,
)


### Anthropic
python
from strands.models.anthropic import AnthropicModel

anthropic_model = AnthropicModel(
    client_args={"api_key": "<KEY>"},
    model_id="claude-3-7-sonnet-20250219",
    params={"temperature": 0.7}
)


### OpenAI qua LiteLLM
python
from strands.models.litellm import LiteLLMModel

litellm_model = LiteLLMModel(
    client_args={"api_key": "<KEY>"},
    model_id="gpt-4o"
)


### Ollama (Local Models)
python
from strands.models.ollama import OllamaModel

ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3",
    temperature=0.3
)


## 9. Best Practices cho Multi-Agent

### 1. Phân Chia Trách Nhiệm Rõ Ràng
• Mỗi agent chỉ làm một việc và làm tốt
• Tránh chồng chéo chức năng giữa các agent
• Định nghĩa interface rõ ràng giữa các agent

### 2. Quản Lý State và Data Flow
python
class AgentState:
    def __init__(self):
        self.parsed_documents = {}
        self.analysis_results = {}
        self.generated_content = {}

    def update_state(self, agent_name: str, result: dict):
        self.analysis_results[agent_name] = result


### 3. Error Handling và Recovery
python
async def safe_agent_execution(agent, input_data):
    try:
        result = await agent.arun(input_data)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


### 4. Monitoring và Logging
python
import logging

# Thiết lập logging cho từng agent
for agent_name in ['parser', 'analyzer', 'generator']:
    logger = logging.getLogger(f"agent.{agent_name}")
    logger.setLevel(logging.INFO)


## 10. Tối Ưu Hóa Performance

### 1. Parallel Processing
python
import asyncio

async def parallel_analysis(jd_text, cv_text):
    # Chạy song song JD và CV analysis
    jd_task = jd_analyzer.arun(jd_text)
    cv_task = cv_analyzer.arun(cv_text)

    jd_result, cv_result = await asyncio.gather(jd_task, cv_task)
    return jd_result, cv_result


### 2. Model Selection Strategy
python
# Sử dụng model phù hợp cho từng agent
AGENT_MODEL_MAPPING = {
    'document_parser': 'claude-3-haiku',      # Nhanh, rẻ
    'jd_analyzer': 'claude-3-7-sonnet',      # Mạnh, chính xác
    'cv_analyzer': 'claude-3-7-sonnet',      # Mạnh, chính xác
    'skills_matcher': 'claude-3-7-sonnet',   # Cần reasoning
    'question_generator': 'claude-3-7-sonnet', # Sáng tạo
    'answer_evaluator': 'claude-3-7-sonnet'  # Đánh giá phức tạp
}


### 3. Caching và Reuse
python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_analysis(content_hash: str):
    # Cache kết quả phân tích để tránh xử lý lại
    pass


## Kết Luận

Strands Agents framework cung cấp một nền tảng mạnh mẽ và linh hoạt để xây dựng các hệ thống AI agent phức tạp. Multi-agent architecture đặc biệt hữ
u ích cho các ứng dụng như Interview Preparation System của bạn, nơi cần sự phối hợp giữa nhiều chuyên gia AI để tạo ra kết quả chất lượng cao.

Các điểm mạnh chính:
• **Modularity**: Dễ phát triển và bảo trì
• **Scalability**: Có thể mở rộng linh hoạt
• **Specialization**: Mỗi agent tối ưu cho nhiệm vụ riêng
• **Flexibility**: Hỗ trợ nhiều model providers và tools
• **Real-time**: Streaming và event handling mạnh mẽ

Framework này rất phù hợp cho việc xây dựng các ứng dụng AI enterprise-grade với yêu cầu cao về chất lượng và hiệu suất.