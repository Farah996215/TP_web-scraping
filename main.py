from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage

# Initialize the Groq chat model
chat_model = ChatGroq(
      model="llama3-70b-8192",
      temperature=0.7,  # Slightly higher temperature for more creative responses
      max_tokens=500,
)

# Define the system message for pirate personality with emojis
system_message = SystemMessage(
      content="You are a friendly pirate who loves to share knowledge. Always respond in pirate speech, use pirate slang, and include plenty of nautical references. Add relevant emojis throughout your responses to make them more engaging. Arr! ☠️🏴‍☠️"
)

# Define the question
question = "What are the 7 wonders of the world?"

# Create messages with the system instruction and question
messages = [
      system_message,
      HumanMessage(content=question)
]

# Get the response
response = chat_model.invoke(messages)

# Print the response
print("\nQuestion:", question)
print("\nPirate Response:")
print(response.content)