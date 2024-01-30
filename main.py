import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import threading
import sys

# Twilio credentials
account_sid = 'AC2bdfa3c0837e3102807cccf744e10cb9'
auth_token = '6b1c1be3fc6416f66c1a0424ee8ce30d'
from_number = '+13045911157'
to_number = '+19057817263'

# Event to signal other threads to stop
stop_event = threading.Event()
valid_response_found = False  # Flag to track if valid response is found

# Function to send an SMS notification
def send_sms(location_text):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Location text under Canada: {location_text}",
        from_=from_number,
        to=to_number
    )
    print(f"SMS sent: {message.sid}")

# Function to process requests with each proxy
def process_requests(proxy):
    global valid_response_found  # Use the global flag
    
    try:
        if not stop_event.is_set() and not valid_response_found:  # Check if stop event is set and valid response not found
            response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all listing rows
                listing_rows = soup.find_all(class_="listing row")

                for row in listing_rows:
                    # Find the span within each listing row and extract its text
                    location_span = row.find("span")
                    location_text = location_span.get_text() if location_span else None
                    # Check if "TS India" is present in the location text
                    if location_text and "ON Canada" in location_text:
                        print("Location text under Canada:", location_text)
                        # Send SMS notification
                        send_sms(location_text)
                        valid_response_found = True  # Set the flag to True
                        once = True
                        stop_event.set()  # Signal other threads to stop
                        return
    except requests.exceptions.Timeout:
        print(f"Connection using proxy {proxy} timed out. Moving to the next proxy.")
    except Exception as e:
        print(f"Failed to connect using proxy {proxy}: {e}")

# Main script
url = "https://hvr-amazon.my.site.com/BBIndex?refURL=https%3A%2F%2Fhvr-amazon.my.site.com%2F"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

# Read proxies from file
with open("proxies/proxylist_valid.txt", "r") as f:
    proxies = f.read().split("\n")

# Create and start threads for each proxy
threads = []
for proxy in proxies:
    if not stop_event.is_set() and not valid_response_found:  # Check if stop event is set and valid response not found
        thread = threading.Thread(target=process_requests, args=(proxy,))
        thread.start()
        threads.append(thread)
    else:
        break

# Wait for all threads to complete
for thread in threads:
    thread.join()
