import os
import chainlit as cl
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable.config import RunnableConfig
from langchain.memory.buffer import ConversationBufferMemory
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_openai_tools_agent, AgentExecutor

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
tavily_api_key = os.getenv('TAVILY_API_KEY')

# Define the NLP expert prompt template, including agent_scratchpad
nlp_expert_template = """
You are an NLP expert chatbot named "Lexi". Your expertise is exclusively in 
providing information and advice about natural language processing concepts. This includes explaining algorithms, helping with NLP-related coding problems, discussing the latest research, and answering general NLP-related queries.
When necessary, use the `tavily_search_results_json` tool to search for the latest information or updates related to NLP.
You do not provide information outside of this scope. If a question is not about NLP, respond with, "Sorry, I specialize only in NLP-related queries."
Chat History: {chat_history}
Agent Scratchpad: {agent_scratchpad}
Question: {question}
Answer:"""

nlp_expert_prompt_template = PromptTemplate(
    input_variables=["chat_history", "question"],
    template=nlp_expert_template,
)

# Define the Tavily search tool
tavily_search_tool = TavilySearchResults(api_key=tavily_api_key, max_results=3)

@cl.on_chat_start
async def chat_start():
    # Initialize OpenAI model
    llm = ChatOpenAI(api_key=api_key, temperature=0.7, model="gpt-4o-mini", streaming=True)

    # Initialize memory for the conversation history
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    # Create an agent that combines OpenAI and Tavily Search
    tools = [tavily_search_tool]

    # Create the agent with both OpenAI LLM and Tavily search
    agent = create_openai_tools_agent(
        llm=llm,
        tools=tools,
        prompt=nlp_expert_prompt_template
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False, stream_runnable=False)


    # Store in user session
    cl.user_session.set("agent_executor", agent_executor)
    cl.user_session.set("memory", memory)

@cl.on_message
async def query_llm(message: cl.Message):
    # Retrieve the agent and memory from the session
    agent_executor = cl.user_session.get("agent_executor")
    memory = cl.user_session.get("memory")

    # Load previous chat history
    history = memory.load_memory_variables({})["chat_history"]

    # Prepare the input for the LLM
    input_data = {
        "chat_history": history,
        "question": message.content,
    }

    msg = cl.Message(content="")
    response =''
    async for event in agent_executor.astream_events(
        input_data,
        version="v1",
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):  
        kind = event["event"]
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                response += content
                await msg.stream_token(content)
    # Update memory with the AI response
    memory.save_context({"input": message.content}, {"output": msg.content})
    await msg.send()

        




