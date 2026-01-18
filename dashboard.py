import sys
import os
import asyncio
import gradio as gr
from dotenv import load_dotenv


load_dotenv()


from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.types import Command


from agent.graph import create_guardian_graph

THREAD_ID = "session_1"
CONFIG = {"configurable": {"thread_id": THREAD_ID}}

async def run_scan_cycle():
    """Starts the graph and runs until it pauses at the Approval Node."""
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["agent/mcp_server.py"],
        env=dict(os.environ)
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            tools = await load_mcp_tools(session)
            app = create_guardian_graph(tools)
            
            logs = []
            async for event in app.astream(
                {"messages": [HumanMessage(content="Scan my AWS infrastructure")]}, 
                config=CONFIG
            ):
                for node, values in event.items():
                    if "messages" in values:
                        last_msg = values["messages"][-1]
                        if isinstance(last_msg, AIMessage):
                            logs.append(f"🤖 {node.upper()}: {last_msg.content}")
            
            state = app.get_state(CONFIG)
            if state.next:
                return (
                    "\n\n".join(logs), 
                    "⚠️ WAITING FOR APPROVAL", 
                    gr.update(visible=True), 
                    gr.update(visible=True)  
                )
            else:
                return (
                    "\n\n".join(logs), 
                    "✅ SCAN COMPLETE (No Risks)", 
                    gr.update(visible=False), 
                    gr.update(visible=False)
                )

async def run_fix_cycle(decision: bool):
    """Resumes the graph with the user's decision."""
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["agent/mcp_server.py"],
        env=dict(os.environ)
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            tools = await load_mcp_tools(session)
            app = create_guardian_graph(tools)
            
            logs = []
            async for event in app.astream(
                Command(resume=decision), 
                config=CONFIG
            ):
                for node, values in event.items():
                    if "messages" in values:
                        last_msg = values["messages"][-1]
                        logs.append(f"🛠️ {node.upper()}: {last_msg.content}")
            
            status = "✅ FIXES APPLIED" if decision else "❌ FIXES CANCELLED"
            return (
                "\n\n".join(logs), 
                status, 
                gr.update(visible=False), 
                gr.update(visible=False)
            )

async def on_approve():
    return await run_fix_cycle(True)

async def on_deny():
    return await run_fix_cycle(False)

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛡️ AWS Guardian: Human-in-the-Loop Dashboard")
    
    with gr.Row():
        scan_btn = gr.Button("🚀 Start Security Scan", variant="primary")
        approve_btn = gr.Button("✅ Approve Fixes", variant="stop", visible=False)
        deny_btn = gr.Button("❌ Deny", visible=False)
    
    status_box = gr.Textbox(label="Status", value="Ready")
    log_box = gr.Textbox(label="Agent Activity Log", lines=15, interactive=False)

    
    scan_btn.click(
        fn=run_scan_cycle, 
        outputs=[log_box, status_box, approve_btn, deny_btn]
    )
    approve_btn.click(
        fn=on_approve,
        outputs=[log_box, status_box, approve_btn, deny_btn]
    )
    
    deny_btn.click(
        fn=on_deny,
        outputs=[log_box, status_box, approve_btn, deny_btn]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)