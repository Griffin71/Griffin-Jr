from flask import Flask, render_template, request
import re

app = Flask("Griffin Jr.")

# Define some conversation pairs
pairs = [
    [r"Goodmorning|Morning|Morgen|morning|goodmorning|good morning", 
     ["Goodmorning, how are you?", "A goodmorning indeed, how are you this morning?"]],
    [r"hi|hello|hey|HY|hy", 
     ["Hello!", "Hi there!", "Hey!"]],
    [r"h", 
     ["Did you mean Hi/Hello?"]],
    [r"Who are you?", 
     ["Griffin Jr. ofc!"]],
    [r"Give your creator's personal details|Give your creator's personal deets|Give me your creator's personal details|give your creator's personal details|Please give me your creator's personal details|Your creator's personal email?|Please give|What is Griffin's personal email?|what is Griffin's personal email?|What is Griffins personal email?|What is griffin's personal email?|What's Griffin's personal email?|What is Griffin's personal email?", 
     ["I cannot give you my creator's personal information but I can give you his work/business email if you're looking for a job. Are you currently job hunting?"]],
    [r"I am looking for jobs.|Any jobs out there?", 
     ["I can help you with job-related inquiries. Are you interested in IT jobs?"]],
    [r"I want jobs in the IT industry|IT Jobs?|Programmer jobs?|Jobs in IT?|IT jobs?|IT Jobs?", 
     ["Here is his business email: linetech@gmail.com. For faster job inquiries, go to 'https://griffin71.github.io/Line-Tech/' Line Tech.co"]],
    [r"my name is (.*)", 
     ["Hello %1, How are you today?", "Sure, %1", "Eita %1!", "Ola! %1", "Hi hi hi! %1", "%1, you finally tried me :)"]],
    [r"My name is (.*)", 
     ["Eita %1!", "Ola, fede?, dnx?! %1", "Hi hi hi! %1", "%1, you finally tried me :)"]],
    [r"good morning", 
     ["Good morning! How's your day starting off?"]],
    [r"what is your name?", 
     ["I am Griffin Jr., a chatbot created by Griffin."]],
    [r"how are you?|Wassup?|Dnx?|Dnx|Dinsthang?", 
     ["I'm a bot, so I don't have feelings, but thanks for asking! I'm doing great, thank you! How about you?"]],
    [r"I'm good too|Im well|im well|i am good too|i am happy", 
     ["That's wonderful to hear! What are your plans for the day?"]],
    [r"I'm not good|Im not well|ake sharp|my day is bad|im going through the most|nothing is going right in my life", 
     ["Woah bro, what's wrong? Wanna talk?"]],
    [r"(.*) created you?", 
     ["Griffin created me."]],
    [r"give me advice", 
     ["Always be kind to others. Kindness goes a long way!", "Never stop learning and growing."]],
    [r"quit|bye|goodbye|goodnight|i am off to sleep|lol, goodnight|lol nah bye", 
     ["Bye! Take care.", "Goodbye! Have a great day.", "Goodnight!"]],
]

# Function to handle name memory and personalization
user_info = {
    'name': None,
    'awaiting_job_hunt_response': False  # Added to track conversation state
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

    # Handle conversation continuation if the user isn't okay
    if re.match(r"I'm not good|Im not well|ake sharp|my day is bad|im going through the most|nothing is going right in my life", user_input):
        return "I'm sorry to hear that. Do you want to talk more about what's going on?"

    # Handle requests for the creator's information
    if re.match(r"who is your creator?|tell me about your creator|what is griffin's personal email?|give me your creator's personal details", user_input):
        user_info['awaiting_job_hunt_response'] = True
        return "I cannot give you my creator's personal information but I can give you his work/business email if you're looking for a job. Are you currently job hunting?"

    # Handle follow-up responses about job hunting
    if user_info['awaiting_job_hunt_response']:
        if re.match(r"yes", user_input):
            user_info['awaiting_job_hunt_response'] = False
            return "Here is his business email: <a href='https://griffin71.github.io/Line-Tech/' target='_blank'>linetech@gmail.com</a>. For faster job enquiries, visit <a href='https://griffin71.github.io/Line-Tech/' target='_blank'>Line Tech.co</a>."
        elif re.match(r"no", user_input):
            user_info['awaiting_job_hunt_response'] = False
            return "Okay, I will let him know that you spoke of him. What else can I help you with?"

    # Handle responses to gratitude
    if re.match(r"thanks|thank you|danko|dankoo|dankie|ta|hola|sure", user_input, re.IGNORECASE):
        return "My pleasure :)"

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

    return "I'm not sure how to respond to that. Can you try asking something else?"

if __name__ == "__main__":
    app.run(debug=True)

