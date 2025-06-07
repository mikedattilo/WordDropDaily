# Initialize Groq client
def initialize_groq_client(api_key):
    from groq import Groq
    try:
        client = Groq(api_key=api_key)
        print("Groq client initialized successfully.")
        return client
    except Exception as e:
        print(f"Failed to initialize Groq client: {e}")
        raise
    
# Create function to generate a text script using Groq client
def generate_vocab_word(client, content_instructions):
    # Create a chat completion
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user",
            "content": content_instructions},
        ]
    )

    return response.choices[0].message.content

def check_vocab_word(script, used_words="used_words.txt"):
    # Get the word from the first line of the script, strip and lowercase it
    lines = script.strip().splitlines()
    if not lines:
        return False  # Empty script
    
    word = lines[0].strip().lower()
    
    # Read the used words from file (if file exists)
    try:
        with open(used_words, "r") as f:
            used_words_set = set(line.strip().lower() for line in f if line.strip())
    except FileNotFoundError:
        used_words_set = set()
    
    # Check for duplication
    print(f"Checking if the word '{word}' has been used...")
    if word in used_words_set:
        print(f"The word '{word}' has already been used. Generating a new word...")
        return False  # Word already used
    
    # If unique, append to file and return True
    print(f"The word '{word}' is unique. Saving...")
    with open(used_words, "a") as f:
        f.write(word + "\n")
        print(f"'{word}' saved to '{used_words}'")
    return True
