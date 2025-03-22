import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from google.generativeai import configure

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API key
configure(api_key=os.getenv("GEMINI_API_KEY"))  # Load Gemini API key from .env

# Instantiate tools
search_tool = SerperDevTool()  # Serper API key is loaded from .env

@CrewBase
class CartCrew:
    """Cart Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def item_finder(self) -> Agent:
        return Agent(
            config=self.agents_config["item_finder"],
            llm=self.agents_config["item_finder"].get("llm"),
            tools=[search_tool],  # Use SerperDevTool for online search
        )

    @task
    def find_items(self) -> Task:
        return Task(config=self.tasks_config["find_items"])

    @crew
    def crew(self) -> Crew:
        """Creates the Cart Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            llm="gemini/gemini-2.0-flash",  # Default LLM for the crew
        )