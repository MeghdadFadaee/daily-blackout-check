import os

token = os.getenv("EITAAEAR_TOKEN")

if token:
    print("Token received successfully!")
    print("token is:", token)
else:
    print("Token not found.")
