from typing import TypedDict, Annotated, List, Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from agent.prompts import MONITOR_PROMPT, VERIFIER_PROMPT


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

def create_guardian_graph(tools):
    """Factory function to build the graph with specific tools"""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
   
    llm_with_tools = llm.bind_tools(tools)

    
    def monitor_node(state: AgentState):
        messages = [SystemMessage(content=MONITOR_PROMPT)] + state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    from langgraph.prebuilt import ToolNode
    tool_node = ToolNode(tools)

    def verifier_node(state: AgentState):
        monitor_report = state["messages"][-1].content
        messages = [
            SystemMessage(content=VERIFIER_PROMPT),
            HumanMessage(content=f"Review this report and propose fixes:\n{monitor_report}")
        ]
        return {"messages": [llm.invoke(messages)]}

    def approval_node(state: AgentState):
        user_approved = interrupt("Do you want to apply these fixes?")
        
        if user_approved:
            return Command(goto="fixer")
        else:
            return Command(goto=END)

    def fixer_node(state: AgentState):
        last_message = state["messages"][-1]
        messages = [
            SystemMessage(content="You are the Remediation Engineer. Execute the tool calls to fix the issues identified."),
            last_message 
        ]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

   
    workflow = StateGraph(AgentState)
    
    workflow.add_node("monitor", monitor_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("verifier", verifier_node)
    workflow.add_node("approval", approval_node)
    workflow.add_node("fixer", fixer_node)
    
    workflow.set_entry_point("monitor")

   
    def should_continue_monitor(state):
        if state["messages"][-1].tool_calls:
            return "tools"
        return "verifier"
    
    def should_continue_fixer(state):
        if state["messages"][-1].tool_calls:
            return "tools" 
        return END

    workflow.add_conditional_edges("monitor", should_continue_monitor)
    workflow.add_edge("tools", "monitor")
    workflow.add_edge("verifier", "approval")
    workflow.add_conditional_edges("fixer", should_continue_fixer)

    return workflow.compile(checkpointer=MemorySaver())