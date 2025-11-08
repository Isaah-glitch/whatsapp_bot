import os
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI
try:
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print("✅ OpenAI client initialized")
except Exception as e:
    print(f"❌ OpenAI client failed: {e}")
    openai_client = None

@app.route("/whatsapp", methods=["POST", "GET"])
def whatsapp_webhook():
    print("📱 WhatsApp webhook called")
    
    if request.method == "GET":
        return "✅ WhatsApp AI Bot is ready for POST requests!", 200
    
    try:
        incoming_msg = request.values.get("Body", "").strip()
        from_number = request.values.get("From", "")
        
        print(f"Message from {from_number}: {incoming_msg}")
        
        resp = MessagingResponse()
        msg = resp.message()
        
        if incoming_msg:
            if openai_client:
                response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": incoming_msg}],
                    max_tokens=150
                )
                ai_reply = response.choices[0].message.content
                msg.body(ai_reply)
            else:
                msg.body("🤖 AI service unavailable. You said: " + incoming_msg)
        else:
            msg.body("👋 Hello! Send me a message!")
        
        return Response(str(resp), mimetype='text/xml')
        
    except Exception as e:
        print(f"Error: {e}")
        resp = MessagingResponse()
        resp.message("❌ Sorry, I encountered an error.")
        return Response(str(resp), mimetype='text/xml')

@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp AI Bot Server is Running! Visit /whatsapp for webhook.", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
