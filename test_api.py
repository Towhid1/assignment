import requests
from time import time

# ============================================
# Task 1 test
# ============================================
BASE_URL = "http://127.0.0.1:8000"
run_n = 10
start = time()
try:
    for i in range(run_n):
        response = requests.get(f"{BASE_URL}/coolest_ten")
    response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
    print(f"api response : {response.json()}")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
execution_time = time() - start
print(f"\n>> 1st task avg execution_time : {execution_time/run_n} sec")

# ============================================
# Task 2 test
# ============================================
start = time()
date_str = "2023-11-03"  # Replace with the desired date
try:
    for i in range(run_n):
        response = requests.get(f"{BASE_URL}/predict/{date_str}")
    response.raise_for_status()
    print(f"api response : {response.json()}")

except requests.RequestException as e:
    print(f"Request error: {e}")
execution_time = time() - start
print(f"\n>> 2nd task execution_time : {execution_time/run_n} sec")
