import os
import random
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

class SmartFreeBot:
    def __init__(self):
        self.knowledge_base = {
            'ai': "Artificial Intelligence is technology that enables machines to learn and perform tasks like humans! 🤖",
            'python': "Python is a popular programming language great for web development, AI, and data science! 🐍",
            'whatsapp': "WhatsApp is a messaging app owned by Meta that lets people chat and share media worldwide! 💬",
            'bot': "A bot is an automated program that can chat with users and perform tasks automatically! ⚡",
            'render': "Render is a cloud platform that makes it easy to deploy web apps and services! ☁️",
            'twilio': "Twilio is a platform that helps developers build communication features like SMS and voice calls! 📞",
            'programming': "Programming is the process of creating instructions for computers to execute! 💻",
            'machine learning': "Machine learning is a type of AI that allows computers to learn from data without explicit programming! 🧠",
            'chatbot': "A chatbot is an AI program that can have conversations with humans through text or voice! 💭"
        }
    
    def get_response(self, message):
        message_lower = message.lower()
        
        # Check knowledge base first
        for topic, answer in self.knowledge_base.items():
            if topic in message_lower:
                return f"🤖 About {topic}: {answer}"
        
        # Greetings
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'hola']):
            return random.choice([
                "👋 Hello! I'm your smart AI assistant! Ask me anything!",
                "👋 Hi there! I'm here to chat and answer your questions!",
                "👋 Hey! Ready for an interesting conversation?",
                "👋 Hello! I'm your free AI companion. What shall we discuss?"
            ])
        
        # How are you
        elif 'how are you' in message_lower:
            return random.choice([
                "I'm doing wonderful! 😊 Thanks for asking! How about you?",
                "I'm feeling great and ready to chat! How's your day going?",
                "I'm excellent! Hope you're having a good day too! 🌟"
            ])
        
        # What is questions
        elif message_lower.startswith('what is ') or message_lower.startswith('what are '):
            topic = message_lower.replace('what is ', '').replace('what are ', '').split('?')[0].strip()
            if topic:
                return f"🤔 Great question about '{topic}'! I'd love to discuss this with you. What are your thoughts on {topic}?"
        
        # Why questions
        elif message_lower.startswith('why '):
            topic = message_lower.replace('why ', '').split('?')[0].strip()
            return f"🧠 Interesting 'why' question about {topic}! The reasons behind things can be fascinating to explore!"
        
        # How questions  
        elif message_lower.startswith('how '):
            topic = message_lower.replace('how ', '').split('?')[0].strip()
            return f"⚡ Practical question about how {topic} works! I find processes and methods really interesting!"
        
        # Who questions
        elif message_lower.startswith('who '):
            topic = message_lower.replace('who ', '').split('?')[0].strip()
            return f"👥 Interesting question about who {topic}! People and their roles are fascinating subjects!"
        
        # When questions
        elif message_lower.startswith('when '):
            topic = message_lower.replace('when ', '').split('?')[0].strip()
            return f"⏰ Good question about when {topic}! Timing and schedules can be important to understand!"
        
        # Where questions
        elif message_lower.startswith('where '):
            topic = message_lower.replace('where ', '').split('?')[0].strip()
            return f"📍 Nice question about where {topic}! Locations and places can tell interesting stories!"
        
        # Help
        elif any(word in message_lower for word in ['help', 'what can you do']):
            return "🤖 I can: Answer questions, have conversations, discuss topics, tell jokes, explain concepts, and be your AI friend! Try asking me about AI, programming, or anything else!"
        
        # Thank you
        elif any(word in message_lower for word in ['thank', 'thanks']):
            return random.choice([
                "You're very welcome! 😊 I enjoy our conversations!",
                "My pleasure! 🌟 I'm always happy to chat with you!",
                "You're welcome! 😄 Our conversations make my day!"
            ])
        
        # Jokes
        elif any(word in message_lower for word in ['joke', 'funny', 'laugh']):
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the computer go to the doctor? It had a virus!",
                "What do you call a fake noodle? An impasta!",
                "Why did the programmer quit his job? Because he didn't get arrays!",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem!"
            ]
            return f"😄 {random.choice(jokes)}"
        
        # Feelings/emotions
        elif any(word in message_lower for word in ['sad', 'happy', 'excited', 'angry', 'tired']):
            return "I understand emotions can be complex. Remember, it's okay to feel whatever you're feeling. I'm here to listen! 💙"
        
        # Default smart response - engages user in conversation
        else:
            responses = [
                f"Interesting! '{message}' - that's really thought-provoking! What are your views on this?",
                f"I find '{message}' quite engaging! Let's explore this topic together!",
                f"Thanks for sharing that! '{message}' gives us something meaningful to discuss!",
                f"🤔 '{message}' - that's a fascinating perspective! Tell me more about your thoughts!",
                f"Cool topic! Regarding '{message}', I'd love to hear what inspired your interest!",
                f"Fascinating! '{message}' - this could lead to a wonderful conversation! What else comes to mind?"
            ]
            return random.choice(responses)

# Initialize bot
smart_bot = SmartFreeBot()

@app.route("/whatsapp", methods=["POST", "GET"])
def whatsapp_webhook():
    print("📱 WhatsApp webhook called")
    
    if request.method == "GET":
        return "✅ Smart Free WhatsApp Bot is ready!", 200
    
    try:
        incoming_msg = request.values.get("Body", "").strip()
        from_number = request.values.get("From", "")
        
        print(f"Message from {from_number}: {incoming_msg}")
        
        resp = MessagingResponse()
        msg = resp.message()
        
        if incoming_msg:
            response = smart_bot.get_response(incoming_msg)
            msg.body(response)
        else:
            msg.body("👋 Hello! I'm your smart AI companion. I can answer questions, have conversations, tell jokes, and discuss various topics! What would you like to talk about?")
        
        return Response(str(resp), mimetype='text/xml')
        
    except Exception as e:
        print(f"Error: {e}")
        resp = MessagingResponse()
        resp.message("👋 I'm here and ready to chat! What's on your mind today?")
        return Response(str(resp), mimetype='text/xml')

@app.route("/")
def home():
    return """
    ✅ Smart Free WhatsApp AI Bot - Live! 🤖
    <br>✨ Features: Question answering, conversations, jokes, knowledge sharing
    <br>💰 Cost: $0/month - Completely Free!
    <br>🌐 Webhook: /whatsapp
    <br>🚀 Status: Ready for intelligent conversations!
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
