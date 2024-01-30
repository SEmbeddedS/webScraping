import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Function to scrape proxies from a website
def scrape_proxies():
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
            else:
                print("Invalid row structure, skipping...")
                break

    print("Proxies saved to proxies.txt")

# Function to check the validity of scraped proxies
def check_proxies():
    def check_proxy(proxy):
        try:
            res = requests.get("https://www.google.ca/", proxies={"http": proxy, "https": proxy}, timeout=5)
            if res.status_code == 200:
                return proxy
        except Exception as e:
            print(f"Error occurred while checking proxy {proxy}: {e}")
            return None

    # Clear the proxylist_valid file
    with open("proxies/proxylist_valid.txt", "w") as valid_file:
        valid_file.write("")

    # Check if proxylist.txt exists
    if os.path.exists("proxies/proxylist.txt"):
        with open("proxies/proxylist.txt", "r") as f:
            proxies = f.read().split("\n")

        valid_proxies = []

        with ThreadPoolExecutor(max_workers=300) as executor:  # Adjust max_workers as needed
            futures = [executor.submit(check_proxy, proxy) for proxy in proxies]
            for future in futures:
                result = future.result()
                if result:
                    valid_proxies.append(result)

        if valid_proxies:
            with open("proxies/proxylist_valid.txt", "w") as valid_file:
                valid_file.write("\n".join(valid_proxies) + "\n")
            print("Finished checking proxies. Valid proxies saved to proxylist_valid.txt")
        else:
            print("No valid proxies found.")
    else:
        print("Proxy list file not found.")

# Run the scraper first
scrape_proxies()

# Then check the proxies
check_proxies()
