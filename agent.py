from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv

load_dotenv(override=True)

# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState) -> dict:
    messages = state["messages"]

    # Đảm bảo SystemMessage luôn ở đầu
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)

    response = llm_with_tools.invoke(messages)

    # === LOGGING ===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"  [Tool] Gọi tool: {tc['name']}({tc['args']})")
    else:
        print("  [Agent] Trả lời trực tiếp")

    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# Khai báo edges
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy — Trợ lý Du lịch Thông minh")
    print("  Gõ 'quit' để thoát")
    print("=" * 60)

    history = []

    while True:
        user_input = input("\nBạn: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Tạm biệt! Chúc bạn có chuyến đi vui vẻ!")
            break

        history.append(("human", user_input))

        print("\nTravelBuddy đang suy nghĩ...")
        try:
            result = graph.invoke({"messages": history})
            final = result["messages"][-1]
            history = result["messages"]  # cập nhật lịch sử đầy đủ từ graph
            print(f"\nTravelBuddy: {final.content}")
        except Exception as e:
            print(f"\n[Lỗi] {e}")
