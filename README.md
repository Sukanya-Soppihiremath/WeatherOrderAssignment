# Weather Order Assignment

This Python project checks the weather for customer orders and flags potential delivery delays. Orders are stored in `orders.json` and the script updates their status based on current weather conditions using the OpenWeatherMap API.

## Features

- **Parallel Weather Fetching:** Uses asyncio and aiohttp to fetch weather data for multiple cities concurrently.  
- **Golden Flow Logic:** Orders are marked as **Delayed** if the weather is Rain, Snow, or Extreme.  
- **Weather-Aware Apology:** Generates personalized messages for delayed orders, e.g.,  
  > "Hi Alice, your order to New York is delayed due to rain. We appreciate your patience!"  
- **Resilience:** Invalid cities are logged with errors but the script continues processing other orders.  
- **Secure API Key:** Uses `.env` file; API keys are never hardcoded.

## Requirements

- Python 3.11+  
- Libraries: `aiohttp`, `python-dotenv`  
- OpenWeatherMap API key (Free Tier)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
