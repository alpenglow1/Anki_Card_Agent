import os, anyio
from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock



load_dotenv()

async def main():
    options = ClaudeAgentOptions(
        model="glm-4.5-air",
        # env={"ANTHROPIC_MODEL": os.getenv("MODEL", "glm-4.7")},
    )
    async for msg in query(prompt="你是谁", options=options):
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, TextBlock):
                    print(block.text)

anyio.run(main)
