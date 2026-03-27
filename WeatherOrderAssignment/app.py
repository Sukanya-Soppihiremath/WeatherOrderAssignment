import json
import os
import asyncio
import aiohttp
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

if not API_KEY:
    raise Exception("API Key not found! Add OPENWEATHER_API_KEY in your .env file.")
print(f"API Key loaded: {API_KEY}")

# Load orders from orders.json
with open("orders.json") as f:
    orders = json.load(f)

# Function to generate a weather-aware apology message
def generate_apology(order, weather_main):
    return f"Hi {order['customer']}, your order to {order['city']} is delayed due to {weather_main.lower()}. We appreciate your patience!"

# Async function to fetch weather for one order
async def fetch_weather(session, order):
    city = order["city"]
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        async with session.get(BASE_URL, params=params) as resp:
            data = await resp.json()
            if resp.status != 200:
                # Handle invalid city or API errors
                message = data.get("message", "Unknown error")
                print(f"[ERROR] Could not fetch weather for {city}: {message}")
                order["message"] = f"Could not fetch weather: {message}"
                return order

            weather_main = data["weather"][0]["main"]
            # Golden Flow logic
            if weather_main in ["Rain", "Snow", "Extreme"]:
                order["status"] = "Delayed"
                order["message"] = generate_apology(order, weather_main)
            else:
                order["status"] = "On Time"
            return order
    except Exception as e:
        print(f"[EXCEPTION] Error fetching weather for {city}: {e}")
        order["message"] = f"Could not fetch weather: {e}"
        return order

# Main async function to process all orders concurrently
async def process_orders():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_weather(session, order) for order in orders]
        return await asyncio.gather(*tasks)

# Run the async main function
if __name__ == "__main__":
    updated_orders = asyncio.run(process_orders())
    # Save updated orders back to orders.json
    with open("orders.json", "w") as f:
        json.dump(updated_orders, f, indent=2)
    print("✅ Orders updated successfully!")