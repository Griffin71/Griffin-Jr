from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Define some basic conversation pairs
pairs = [
    [r"my name is (.*)", ["Hello %1, How are you today?", "Sure, %1", "Eita %1!", "Ola! %1", "Hi hi hi! %1", "%1, you finally tried me :)"]],
    [r"hi|hello|hey", ["Hello!", "Hi there!", "Hey!"]],
    [r"what is your name?", ["I am Griffin Jr., a chatbot created by Griffin."]],
    [r"how are you?|Wassup?|Dnx?|Dnx|Dinsthang?", ["I'm a bot, so I don't have feelings, but thanks for asking! I'm doing great, thank you! How about you?"]],
    [r"I'm good too|Im well|im well|i am good too|i am happy", ["That's wonderful to hear!"]],
    [r"I'm not good|Im not well|ake sharp|my day is bad|im going through the most|nothing is going right in my life", ["Woah bro, what's wrong? Wanna talk?"]],
    [r"sorry (.*)", ["It's okay.", "No worries!", "Apology accepted."]],
    [r"i'm (.*) (good|well|okay|ok)", ["Good to hear that!", "Great! How can I assist you today?"]],
    [r"(.*) age?", ["I'm timeless!", "Age is just a number for me."]],
    [r"(.*) created you?", ["Griffin created me."]],
    [r"what do you like?", ["I enjoy learning new things and helping users like you!"]],
    [r"give me advice", ["Always be kind to others. Kindness goes a long way!", "Never stop learning and growing."]],
    [r"quit|bye|goodbye|goodnight|i am off to sleep|lol, goodnight|lol nah bye", ["Bye! Take care.", "Goodbye! Have a great day.", "Goodnight!"]],
]

# Function to handle name memory and personalization
user_info = {
    'name': None
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/get")
def get_bot_response():
    user_input = request.args.get('msg').strip().lower()

    # Handle user name setting
    if re.match(r"my name is (.*)", user_input):
        match = re.match(r"my name is (.*)", user_input)
        if match:
            user_info['name'] = match.group(1).capitalize()
            # Check if the user is the creator
            if user_info['name'].lower() == "kabelo samkelo kgosana":
                return f"Hello Creator {user_info['name']}! How may I assist you today?"
            return f"Hello {user_info['name']}, How are you today?"

    # Provide personalized responses
    if user_info['name']:
        for pattern, responses in pairs:
            if re.match(pattern, user_input, re.IGNORECASE):
                response = responses[0].replace("%1", user_info['name'])
                return response
        return "I don't understand that. Can you rephrase?"
    else:
        for pattern, responses in pairs:
            if re.match(pattern, user_input, re.IGNORECASE):
                return responses[0]
        return "I don't understand that. Can you rephrase?"

if __name__ == "__main__":
    app.run(debug=True)
