from sic_framework.services.openai_gpt.gpt import GPT, GPTResponse, GPTConf, GPTRequest

"""
Please use the 0.28 version of openai, and not the recently updated >1.0 version as this file has not been updated yet.
pip install openai==0.28.1

The GPT service should be running. You can start it with:
[services/openai_gpt/] python gpt.py 
"""

# Read OpenAI key from file
with open("openai_key", "rb") as f:
    openai_key = f.read()
    openai_key = openai_key.decode("utf-8").strip()  # Decode bytes to string and remove new line character

# Setup GPT
conf = GPTConf(openai_key=openai_key)
gpt = GPT(conf=conf)


# Constants
NUM_TURNS = 5
i = 0
context = []

# Continuous conversation with GPT
while i < NUM_TURNS:
    # Ask for user input
    inp = input("Start typing...\n-->" if i == 0 else "-->")

    # Get reply from model
    reply = gpt.request(GPTRequest(inp, context_messages=context))
    print(reply.response, "\n", sep='')

    # Add user input to context messages for the model (this allows for conversations)
    context.append(inp)
    i += 1
