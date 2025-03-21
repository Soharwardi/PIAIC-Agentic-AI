from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from google.generativeai import configure

# Configure Gemini API key
configure(api_key="AIzaSyAafVfM8sUZsoHIyOpC47pRHpG3m2RAGIs")

@CrewBase
class CartCrew:
    """Cart Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def catalog_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["catalog_manager"],
            llm=self.agents_config["catalog_manager"].get("llm"),  # Pass the LLM string directly
        )

    @agent
    def price_checker(self) -> Agent:
        return Agent(
            config=self.agents_config["price_checker"],
            llm=self.agents_config["price_checker"].get("llm"),  # Pass the LLM string directly
        )

    @agent
    def inventory_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["inventory_manager"],
            llm=self.agents_config["inventory_manager"].get("llm"),  # Pass the LLM string directly
        )

    @agent
    def recommendation_engine(self) -> Agent:
        return Agent(
            config=self.agents_config["recommendation_engine"],
            llm=self.agents_config["recommendation_engine"].get("llm"),  # Pass the LLM string directly
        )

    @agent
    def cart_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["cart_manager"],
            llm=self.agents_config["cart_manager"].get("llm"),  # Pass the LLM string directly
        )

    @task
    def update_catalog(self) -> Task:
        return Task(config=self.tasks_config["update_catalog"])

    @task
    def check_prices(self) -> Task:
        return Task(config=self.tasks_config["check_prices"])

    @task
    def check_inventory(self) -> Task:
        return Task(config=self.tasks_config["check_inventory"])

    @task
    def suggest_products(self) -> Task:
        return Task(config=self.tasks_config["suggest_products"])

    @task
    def manage_cart(self) -> Task:
        return Task(config=self.tasks_config["manage_cart"])

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