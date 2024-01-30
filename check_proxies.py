import os
import requests
from concurrent.futures import ThreadPoolExecutor

def check_proxy(proxy):
    try:
        res = requests.get("https://www.google.ca/", proxies={"http": proxy, "https": proxy}, timeout=5)
        if res.status_code == 200:
            return proxy
    except Exception as e:
        print(f"Error occurred while checking proxy {proxy}: {e}")
        return None

def main():
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

if __name__ == "__main__":
    main()
