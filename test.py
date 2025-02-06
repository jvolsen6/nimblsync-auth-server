import requests

TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"

data = {
    "grant_type": "authorization_code",
    "code": "AB117387766987WWJsshrgJHBhmOzmDoaDxnflGPeODGuxw7A5",
    "redirect_uri": "https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl",
    "client_id": "ABwuhNRa4dtcPaDOUh0g3D8DzGeyApFa9hby56MU8s69hdXcT2",
    "client_secret": "9rAUjGnhM8yOBSVr8mDgCOk6vwB0cY271t7mxotB",
}

response = requests.post(TOKEN_URL, data=data)

print(response.json())  # Check for errors
