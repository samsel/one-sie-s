# browser AI Agent
# an AI agent that uses your browser and a locally installed LLM

from langchain_ollama import ChatOllama
from browser_use import Agent, BrowserConfig, Browser
import asyncio

llm = ChatOllama(model="llama3.1:latest")

config = BrowserConfig(
    chrome_instance_path="/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"
)

browser = Browser(config=config)


async def main():
    agent = Agent(
        task="Type a random sentence above weather in the search box",
        llm=llm,
        browser=browser
    )
    result = await agent.run()
    # Manually close the browser
    await browser.close()
    print(result)

asyncio.run(main())