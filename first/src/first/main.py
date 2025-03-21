#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from first.crews.cart_crew.cart_crew import CartCrew

class CartState(BaseModel):
    user_id: int = 1
    cart_contents: list = []
    recommendations: list = []
    total_price: float = 0.0

class CartFlow(Flow[CartState]):

    @start()
    def initialize_cart(self):
        print("Initializing cart for user")
        self.state.cart_contents = []

    @listen(initialize_cart)
    def update_catalog(self):
        print("Updating catalog")
        CartCrew().crew().kickoff()

    @listen(update_catalog)
    def check_prices(self):
        print("Checking prices")
        CartCrew().crew().kickoff()

    @listen(check_prices)
    def check_inventory(self):
        print("Checking inventory")
        CartCrew().crew().kickoff()

    @listen(check_inventory)
    def suggest_products(self):
        print("Suggesting products")
        result = CartCrew().crew().kickoff()
        self.state.recommendations = result.raw

    @listen(suggest_products)
    def manage_cart(self):
        print("Managing cart")
        result = CartCrew().crew().kickoff()
        
        # Debug: Print the raw output
        print(f"Raw output from manage_cart task: {result.raw}")
        
        # Ensure result.raw is a dictionary
        if isinstance(result.raw, dict):
            self.state.cart_contents = result.raw.get("cart_contents", [])
            self.state.total_price = result.raw.get("total_price", 0.0)
        else:
            print("Error: Unexpected output format from manage_cart task.")
            self.state.cart_contents = []
            self.state.total_price = 0.0

def kickoff():
    cart_flow = CartFlow()
    cart_flow.kickoff()

def plot():
    cart_flow = CartFlow()
    cart_flow.plot()

if __name__ == "__main__":
    kickoff()