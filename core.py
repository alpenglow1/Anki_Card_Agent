import os
import asyncio
from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKClient,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ResultMessage,
)
from tools import get_server, get_tools_list


def load_system_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


async def run_anki_agent_generator(user_prompt: str, verbose: bool = False):
    """
    Anki Agent 核心逻辑 (Generator).
    """
    # 1. 获取本地工具 Server
    server = get_server()
    server_name = "anki-tools"  # 必须与 tools.py 中的 name 一致

    # 2. 自动生成 allowed_tools 列表
    tools = get_tools_list()
    tool_names = [t.name for t in tools]
    allowed_tools = [f"mcp__{server_name}__{name}" for name in tool_names]

    system_prompt = load_system_prompt()

    yield {"type": "log", "message": "--- 启动 Anki Agent ---"}
    yield {"type": "log", "message": f"已加载工具集 '{server_name}': {tool_names}"}
    yield {"type": "log", "message": f"正在处理任务: {user_prompt}"}
    yield {"type": "log", "message": "-" * 30}

    # 3. 配置 Agent 选项
    options = ClaudeAgentOptions(
        mcp_servers={server_name: server},
        allowed_tools=allowed_tools,
        system_prompt=system_prompt,
        model="glm-4.7"
    )

    try:
        # 4. 启动 Client 并发送查询
        async with ClaudeSDKClient(options=options) as client:
            await client.query(user_prompt)

            # 5. 实时处理响应流
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            # 打印 Claude 的思考或回答
                            yield {"type": "assistant_message", "content": block.text}
                        elif isinstance(block, ToolUseBlock):
                            # 打印工具调用状态
                            yield {
                                "type": "tool_use",
                                "name": block.name,
                                "input": block.input,
                            }
                elif isinstance(message, ResultMessage):
                    if message.usage:
                        yield {"type": "usage", "usage": message.usage}
                    if message.total_cost_usd is not None:
                        yield {
                            "type": "cost",
                            "cost": message.total_cost_usd,
                        }
                    yield {
                        "type": "completion",
                        "turns": message.num_turns,
                        "message": f"✅ 任务完成 (轮次: {message.num_turns})",
                    }

    except asyncio.CancelledError:
        yield {"type": "cancelled", "message": "⚠️ 任务已被用户取消。"}
        # Re-raise to ensure the task is truly cancelled in the caller
        raise
    except Exception as e:
        yield {"type": "error", "message": f"❌ 发生错误: {e}"}
        import traceback

        traceback.print_exc()


async def run_anki_agent(user_prompt: str, verbose: bool = False):
    """
    Anki Agent 核心逻辑 (CLI wrapper).
    """
    async for event in run_anki_agent_generator(user_prompt, verbose):
        if event["type"] == "log":
            print(event["message"])
        elif event["type"] == "assistant_message":
            print(f"🤖 Claude: {event['content']}")
        elif event["type"] == "tool_use":
            print(f"🛠️  调用工具: {event['name']}")
            if verbose:
                print(f"    参数: {event['input']}")
        elif event["type"] == "usage":
            print(f"📊 Token 使用情况: {event['usage']}")
        elif event["type"] == "cost":
            print(f"💰 本次花费: ${event['cost']:.4f}")
        elif event["type"] == "completion":
            print(event["message"])
        elif event["type"] == "cancelled":
            print(event["message"])
        elif event["type"] == "error":
            print(event["message"])
