import math

# Define tokens for safe and risky responses
safe_token = "No"
risky_token = "Yes"
# Number of top log probabilities to consider
nlogprobs = 5


# Function to parse the output from the model
def parse_output(generated_tokens_list):
    label, prob_of_risk = None, None

    # If nlogprobs is greater than 0, calculate probabilities
    if nlogprobs > 0:
        # Extract top tokens from the generated tokens list
        top_tokens_list = [
            generated_tokens["top_tokens"] for generated_tokens in generated_tokens_list
        ]
        # Get probabilities for safe and risky tokens
        prob = get_probablities(top_tokens_list)
        prob_of_risk = prob[1]

    # Extract the generated text from the first result
    res = next(iter(generated_tokens_list))["text"].strip()

    # Determine the label based on the generated text
    if risky_token.lower() == res.lower():
        label = risky_token
    elif safe_token.lower() == res.lower():
        label = safe_token
    else:
        label = "Failed"

    return label, prob_of_risk


# Function to calculate probabilities of safe and risky tokens
def get_probablities(top_tokens_list):
    safe_token_prob = 1e-50
    risky_token_prob = 1e-50
    # Iterate through top tokens to find probabilities of safe and risky tokens
    for top_tokens in top_tokens_list:
        for token in top_tokens:
            if token["text"].strip().lower() == safe_token.lower():
                safe_token_prob += math.exp(token["logprob"])
            if token["text"].strip().lower() == risky_token.lower():
                risky_token_prob += math.exp(token["logprob"])

    # Calculate softmax probabilities
    probabilities = softmax([math.log(safe_token_prob), math.log(risky_token_prob)])

    return probabilities


# Function to compute softmax of a list of values
def softmax(values):
    exp_values = [math.exp(v) for v in values]
    total = sum(exp_values)
    return [v / total for v in exp_values]
