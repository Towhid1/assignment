import requests
from time import time
# ============================================
# Task 1 test
# ============================================
url = "http://127.0.0.1:8000/coolest_ten"

start = time()
try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
    data = response.json()
    print(data)
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
execution_time = time() - start
print(f"execution_time : {execution_time} sec")