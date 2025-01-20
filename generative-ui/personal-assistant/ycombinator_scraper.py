from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
import json
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the agents using environment variable
config_list = [
    {
        "model": "gpt-4o-mini",
        "api_key": os.getenv('OPENAI_API_KEY')
    }
]

# Create the web scraping agent
scraper_agent = AssistantAgent(
    name="scraper",
    llm_config={
        "config_list": config_list,
        "temperature": 0.7,
    },
    system_message="""You are a web scraping specialist. Your task is to:
    1. Browse Y Combinator's website to find W24 batch companies. Just pick 2 companies from the list.
    2. Extract company names and their website URLs
    3. Format the data and send it to the analyzer agent
    Use appropriate web scraping libraries and handle errors gracefully."""
)

# Create the analyzer agent
analyzer_agent = AssistantAgent(
    name="analyzer",
    llm_config={
        "config_list": config_list,
        "temperature": 0.5,
    },
    system_message="""You are a company analyst. Your task is to:
    1. Receive company data from the scraper agent
    2. Visit each company's website
    3. Analyze their product and problem statement
    4. Extract founder information
    5. Create a JSON file with all the information
    Be thorough and accurate in your analysis."""
)

# Create a user proxy agent
user_proxy = UserProxyAgent(
    name="user_proxy",
    code_execution_config={
        "work_dir": "workspace",
        "use_docker": False  # Disable Docker usage
    },
    human_input_mode="NEVER"
)

# Function to initiate the workflow
async def analyze_yc_companies():
    # Start the conversation between agents
    await user_proxy.initiate_chat(
        scraper_agent,
        message="""Please scrape the YC W24 batch companies and their website URLs. 
        Once done, share the data with the analyzer agent."""
    )

    # The scraper agent will collect data and pass it to the analyzer
    await user_proxy.initiate_chat(
        analyzer_agent,
        message="""Analyze each company website and create a JSON file with:
        1. Company name
        2. Website URL
        3. Product description
        4. Problem statement
        5. Founder names"""
    )

# Save results to JSON
def save_to_json(companies_data):
    with open('yc_w24_companies.json', 'w') as f:
        json.dump(companies_data, f, indent=4)

asyncio.run(analyze_yc_companies()) 