import os
import requests
from bs4 import BeautifulSoup

# Check if proxies.txt exists and clear its contents if it does
if os.path.exists("proxies/proxylist.txt"):
    open("proxies/proxylist.txt", "w").close()
    print("proxies.txt file cleared.")

response = requests.get("https://free-proxy-list.net/")
soup = BeautifulSoup(response.text, 'html.parser')

# Find all <tr> tags
proxy_rows = soup.find_all('tr')

# Open a file in write mode
with open("proxies/proxylist.txt", "w") as file:
    # Extract IP and port from the first <tr> excluding the header row
    for row in proxy_rows[1:]:
        columns = row.find_all('td')
        # Check if there are enough columns in the row
        if len(columns) >= 2:
            ip = columns[0].text
            port = columns[1].text
            proxy = f"{ip}:{port}"
            file.write(proxy + "\n")  # Write the proxy to the file
            #print(f"Proxy added: {proxy}")
        else:
            print("Invalid row structure, skipping...")
            break

print("Proxies saved to proxies.txt")
