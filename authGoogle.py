from pyngrok import ngrok

# Start ngrok tunnel for localhost:5000
public_url = ngrok.connect(5000)  # Corrected method

print(f"Ingress established at: {public_url}")
