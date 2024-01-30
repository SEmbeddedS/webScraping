import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

# Twilio credentials
account_sid = 'AC2bdfa3c0837e3102807cccf744e10cb9'
auth_token = '6b1c1be3fc6416f66c1a0424ee8ce30d'
from_number = '+13045911157'
to_number = '+19057817263'

# Function to send an SMS notification
def send_sms(location_text):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Location text under Canada: {location_text}",
        from_=from_number,
        to=to_number
    )
    print(f"SMS sent: {message.sid}")

# Main script
url = "https://hvr-amazon.my.site.com/BBIndex?refURL=https%3A%2F%2Fhvr-amazon.my.site.com%2F"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

# Find all listing rows
listing_rows = soup.find_all(class_="listing row")

for row in listing_rows:
    # Find the span within each listing row and extract its text
    location_span = row.find("span")
    location_text = location_span.get_text() if location_span else None
    # Check if "CANADA" is present in the location text
    if location_text and "Canada" in location_text:
        print("Location text under Canada:", location_text)
        # Send SMS notification
        send_sms(location_text)
