import subprocess
import schedule
import time

def run_file1():
    subprocess.run(['python', 'fetchValidProxies.py'])

def run_file2():
    subprocess.run(['python', 'main.py'])

# Schedule file1.py to run every 1 minute
schedule.every(2).minutes.do(run_file1)

# Schedule file2.py to run every 5 seconds
schedule.every(10).seconds.do(run_file2)

while True:
    schedule.run_pending()
    time.sleep(1)
