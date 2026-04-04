from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

# Initialize the Groq chat model
llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.3,
    max_tokens=500,
)

# Create a prompt template for generating meal titles
prompt_template = PromptTemplate.from_template(
    "List {n} cooking/meal titles for {cuisine} cuisine (name only)."
)

# Create a runnable chain using the pipe operator
chain = prompt_template | llm

# Run the chain with specific parameters
response = chain.invoke({
    "n": 5,
    "cuisine": "Italian"
})

# Print the response
print("\nPrompt: List 5 cooking/meal titles for Italian cuisine (name only).")
print("\nResponse:")
print(response.content)