# Filter Warframe Prime in json and search market
# create a list of item prices
# Get Warframe public data at https://wiki.warframe.com/w/Public_Export
import json
import os
import requests


def SearchPrimeSetPrices(prime_set):
    print("Searching price for {} sets...".format(len(prime_set)))
    prime_prices = []
    for prime in prime_set:
        search_item = prime['name'].lower().replace('&','and').replace(" ", "_") + "_set"

        # Query the API
        url = f"https://api.warframe.market/v2/orders/item/{search_item}"
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Parse the JSON response
            result = response.json()

            # Get the orders from the data field
            orders = result.get('data', [])

            # Filter sell orders
            sell_orders = [
                order for order in orders if order.get('type') == 'sell']

            # Filter online orders
            online_orders = [order for order in sell_orders if order.get(
                'user', {}).get('status') == 'ingame']

            # Find the minimum platinum price
            if online_orders:
                min_price_order = min(
                    online_orders, key=lambda x: x.get('platinum', float('inf')))
                prime_prices.append(
                    (prime['name'], min_price_order.get('platinum')))
            else:
                print(f"{prime['name']} - No sell orders found")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {prime['name']}: {e}")

    # Sort prime_prices by price (second value in tuple) in ascending order
    sorted_prices = sorted(prime_prices, key=lambda x: x[1])
    print("\nPrices (Ascending Order):")
    for name, price in sorted_prices:
        print(f"{name}: {price} platinum")


# Function to load and filter prime items from a JSON file
def load_prime_items(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [item for item in data if item.get('isPrime', False) == True]


# Load prime items
prime_sets = load_prime_items('Warframes.json')

SearchPrimeSetPrices(prime_sets)
