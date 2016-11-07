import base64
with open ("secret.txt", "br+") as f:
    i = input('Enter your password: ')
    encoded = base64.b64encode(i.encode())
    f.write(encoded);
