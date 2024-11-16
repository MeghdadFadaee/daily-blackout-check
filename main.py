import os

token = os.getenv("EITAAYAR_TOKEN")

if token:
    print("Token received successfully!")
    print("token is:", token)
else:
    print("Token not found.")
