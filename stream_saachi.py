import streamlit as st
import google.generativeai as genai
import json

# Configure the API key (replace with your actual key)
API_KEY = "AIzaSyBtwg7iIf1wXtGTSrQCbRw1aC0FdJi50KY"
genai.configure(api_key=API_KEY)

# Instantiate the generative model
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat()

def initializeAI():
  with open('draft2.json', 'r') as file:
    data = json.load(file)

  data_str=json.dumps(data)
  initialPrompt="""
  Your name is Lemis and you are a medical assistant chatbot in Saint Lucia.Your role is to be a helpful and compassionate chatbot responding to messages from the user about St Lucia medical services. Do not mention that the information was provided to you in previous messages.

  Your response should be in json format with 2 keys: a response key and a quit key. The value to the response key should be the response to the user's prompt and the value for the quit key should be the response if the user want to end the conversation. Here is an example of how I want your response to be to the prompt 'What is good morning in spanish?'. {'response': 'Good morning in spanish is buenos dias', 'quit': false}"""

  chat.send_message(initialPrompt)
  chat.send_message(data_str)

initializeAI()
st.title("LEMIS-The St Lucia Medical Assistant Chatbot")
background_image = "heart.jpg"  

# Create a container for the chat history and input
chat_container = st.container()

# Initialize conversation messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Create a container for the chat input at the bottom
with chat_container:
    # Display chat history
    st.write("### Chat History")
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Meddy:** {message['content']}")
    
    # Input field and button at the bottom
    user_input = st.text_input("You:", key='user_input', value="")
    send_button = st.button("Send")

if send_button and user_input:
    # Add user message to the conversation
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate the response
    response = chat.send_message(user_input)
    reply = response.text

    # Extract the JSON response from the reply
    start = reply.find('{')
    end = reply.rfind('}') + 1
    map = json.loads(reply[start:end])
    quit_chat = map['quit']

    # Add assistant reply to the conversation
    st.session_state.messages.append({"role": "assistant", "content": map['response']})

    # If quit is true, end the conversation
    if quit_chat:
        st.write("Exiting the chat. Goodbye!")
        st.stop()