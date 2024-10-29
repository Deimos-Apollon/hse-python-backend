import requests


for i in range(500):
    requests.get('http://localhost:8080/item')
for i in range(200):
    requests.get('http://localhost:8080/cart')