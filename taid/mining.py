import requests
import time

while True:
	requests.get("http://0.0.0.0:1000/mine")
	time.sleep(5)