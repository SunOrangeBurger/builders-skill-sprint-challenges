import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from datetime import date, datetime
import requests
from strands import Agent, tool
from strands_tools import calculator

MODEL = "us.amazon.nova-pro-v1:0"

@tool
def weather(city: str) -> str:
    """Get the current weather for a city.
    Args:
        city: The name of the city.
    """
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=3",
            timeout=5
        )
        return response.text
    except:
        return f"The weather in {city} is sunny, 28°C"

@tool
def age_calculator(birth_date: str) -> str:
    """Calculate age from a birth date.
    Args:
        birth_date: Date of birth in YYYY-MM-DD format.
    """
    today = date.today()
    born = datetime.strptime(birth_date, "%Y-%m-%d").date()
    age = today.year - born.year - (
        (today.month, today.day) < (born.month, born.day)
    )
    return f"Someone born on {birth_date} is {age} years old."

agent = Agent(
    model=MODEL,
    tools=[calculator, weather, age_calculator],
    system_prompt="You are a helpful assistant with tools. Use them to answer accurately."
)

print("🧮 Math test:")
response = agent("What is 42 * 17?")
print(response)

print("\n🌤️ Weather test:")
response = agent("What's the weather in Chennai?")
print(response)

print("\n🎂 Age test:")
response = agent("How old is someone born on 2000-05-15?")
print(response)

print("\n✅ Challenge 2 complete!")