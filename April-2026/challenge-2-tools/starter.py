"""
Challenge 2: Adding Tools to Your Agent
Give your agent a calculator, weather tool, and age calculator.
Model: Amazon Nova Pro via Bedrock

Instructions:
  1. Fill in the TODO sections below
  2. Run: python starter.py
  3. Needs AWS credentials configured (aws configure)
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from datetime import date, datetime
from strands import Agent, tool
from strands_tools import calculator

MODEL = "us.amazon.nova-pro-v1:0"


# ============================================================
# TODO 1: Create a custom weather tool
# ============================================================
# Hint: Use the @tool decorator
# The function should take a city name and return weather info
# Use wttr.in API: https://wttr.in/{city}?format=j1
# Or return dummy data: f"The weather in {city} is sunny, 28°C"

# @tool
# def weather(city: str) -> str:
#     """Get the current weather for a city.
#     Args:
#         city: The name of the city.
#     """
#     # TODO: Implement this function
#     pass


# ============================================================
# TODO 2: Create a custom age calculator tool
# ============================================================
# Hint: Use @tool decorator
# Take a birth_date string in YYYY-MM-DD format
# Calculate the age using datetime

# @tool
# def age_calculator(birth_date: str) -> str:
#     """Calculate age from a birth date.
#     Args:
#         birth_date: Date of birth in YYYY-MM-DD format.
#     """
#     # TODO: Implement this function
#     pass


# ============================================================
# TODO 3: Create an agent with all tools
# ============================================================
# Hint: Agent(model=MODEL, tools=[calculator, weather, age_calculator], ...)

agent = None  # Replace this line


# ============================================================
# TODO 4: Test the agent with different questions
# ============================================================

# Test math
print("🧮 Math test:")
# response = agent("What is 42 * 17?")
# print(response)

# Test weather
print("\n🌤️ Weather test:")
# response = agent("What's the weather in Chennai?")
# print(response)

# Test age
print("\n🎂 Age test:")
# response = agent("How old is someone born on 2000-05-15?")
# print(response)


print("\n✅ Challenge 2 complete!")
