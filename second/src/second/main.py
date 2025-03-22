#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from second.crews.cart_crew.cart_crew import CartCrew

class CartState(BaseModel):
    user_id: int = 1
    search_query: str = ""  # Field to store the user's search query
    search_results: list = []  # Field to store the search results

class CartFlow(Flow[CartState]):

    @start()
    def initialize_flow(self):
        print("Welcome to the Cart Agent!")
        self.state.search_query = input("What item are you looking for? ")  # Take user input

    @listen(initialize_flow)
    def find_items(self):
        print(f"Searching for: {self.state.search_query}")
        result = CartCrew().crew().kickoff(inputs={"query": self.state.search_query})
        self.state.search_results = result.raw  # Store the search results
        print("Search results:", self.state.search_results)

def kickoff():
    cart_flow = CartFlow()
    cart_flow.kickoff()

def plot():
    cart_flow = CartFlow()
    cart_flow.plot()

if __name__ == "__main__":
    kickoff()