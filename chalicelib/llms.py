from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.chat_models import BedrockChat
from langchain.schema import HumanMessage


def get_simple_response_by_bedrock(message: str) -> str:
    chat = BedrockChat(
        region_name="us-east-1",
        model_id="anthropic.claude-v2",
        model_kwargs={"temperature": 0.1},
    )
    messages = [HumanMessage(content=message)]
    resp = chat(messages)
    return resp.content


def create_agent_chain():
    chat = BedrockChat(
        region_name="us-east-1",
        model_id="anthropic.claude-v2",
        model_kwargs={"temperature": 0.1},
    )
    tools = load_tools(["ddg-search", "wikipedia"])
    return initialize_agent(tools, chat, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)


def local_main():
    # agent_chain = create_agent_chain()
    # resp = agent_chain.run("Translate this sentence from English to French. I love programming.")
    # print(resp)
    resp = get_simple_response_by_bedrock("スヌーピーの誕生日は？")
    print(type(resp))
    breakpoint()
    print(resp)


if __name__ == "__main__":
    local_main()
