from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask is running!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
    
@app.route('/auth/callback')
def auth_callback():
    auth_code = request.args.get("code")
    if not auth_code:
        return "Authorization code not provided", 400
    return f"Authorization Code: {auth_code}"

