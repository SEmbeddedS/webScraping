import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to send an email notification
def send_email(location_text):
    # Email configuration
    sender_email = "sunilpatel1503@yahoo.com"
    receiver_email = "sunilpatel15321@gmail.com"
    password = "chako143chaki"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Location Notification"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Create the HTML version of the email (you can customize this)
    html = f"""\
    <html>
      <body>
        <p>Location text under CANADA: {location_text}</p>
      </body>
    </html>
    """

    # Attach HTML to the email
    part2 = MIMEText(html, 'html')
    msg.attach(part2)

    # Send the email
    with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

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
    if location_text and "United Kingdom" in location_text:
        print("Location text under CANADA:", location_text)
        # Send email notification
        send_email(location_text)
