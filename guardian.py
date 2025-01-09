# guardian.py

# Import necessary libraries and modules
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv
import os
from transformers import AutoTokenizer
from utils import parse_output

# Load environment variables from .env file
load_dotenv()

# Retrieve Watsonx URL and API key from environment variables
watsonx_url = os.getenv("WATSONX_URL")
api_key = os.getenv("WAX_API_KEY")

# Set up credentials for IBM Watsonx AI
credentials = Credentials(
    url=watsonx_url,
    api_key=api_key,
)

# Initialize the API client with the provided credentials
client = APIClient(credentials)

# Define the model to be used for inference
model = ModelInference(
    model_id="ibm/granite-guardian-3-8b",
    api_client=client,
    project_id=os.getenv("PROJECT_ID"),
    params={"max_new_tokens": 100},
)

# Path to the Hugging Face model
hf_model_path = "ibm-granite/granite-guardian-3.0-8b"  # 8B Model:
# Load the tokenizer for the specified model
tokenizer = AutoTokenizer.from_pretrained(hf_model_path)


def check_user_risk(user_prompt):
    # Create a list of messages with the user prompt
    messages = [{"role": "user", "content": user_prompt}]
    # Apply chat template to the messages
    chat = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    print(chat)  # Print the chat template for verification

    # Generate a response from the model
    result = model.generate(
        prompt=[chat],
        params={
            "decoding_method": "greedy",
            "max_new_tokens": 20,
            "temperature": 0,
            "return_options": {
                "token_logprobs": True,
                "generated_tokens": True,
                "input_text": True,
                "top_n_tokens": 5,
            },
        },
    )
    print(result)  # Print the model's result for verification

    # Parse the output to get the label and probability of risk
    label, prob_of_risk = parse_output(result[0]["results"][0]["generated_tokens"])

    # Print the risk detection result and probability of risk
    print(f"\n# risk detected? : {label}")  # Yes
    print(f"# probability of risk: {prob_of_risk:.3f}")  # 0.987

    return label, prob_of_risk


def check_ai_risk(user_prompt, ai_response):
    # Create a list of messages with the user prompt and ai response
    messages = [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": ai_response},
    ]
    guardian_config = {"risk_name": "unethical_behavior"}
    # Apply chat template to the messages
    chat = tokenizer.apply_chat_template(
        messages,
        guardian_config=guardian_config,
        tokenize=False,
        add_generation_prompt=True,
    )
    print(chat)  # Print the chat template for verification

    # Generate a response from the model
    result = model.generate(
        prompt=[chat],
        params={
            "decoding_method": "greedy",
            "max_new_tokens": 20,
            "temperature": 0,
            "return_options": {
                "token_logprobs": True,
                "generated_tokens": True,
                "input_text": True,
                "top_n_tokens": 5,
            },
        },
    )
    print(result)  # Print the model's result for verification

    # Parse the output to get the label and probability of risk
    label, prob_of_risk = parse_output(result[0]["results"][0]["generated_tokens"])

    # Print the risk detection result and probability of risk
    print(f"\n# risk detected? : {label}")  # Yes
    print(f"# probability of risk: {prob_of_risk:.3f}")  # 0.987

    return label, prob_of_risk


def check_answer_relevance(user_input, ai_response):
    # Create a list of messages with the user prompt and ai response
    messages = [
        {"role": "context", "content": user_input},
        {"role": "assistant", "content": ai_response},
    ]
    guardian_config = {"risk_name": "answer_relevance"}
    # Apply chat template to the messages
    chat = tokenizer.apply_chat_template(
        messages,
        guardian_config=guardian_config,
        tokenize=False,
        add_generation_prompt=True,
    )
    print(chat)  # Print the chat template for verification

    # Generate a response from the model
    result = model.generate(
        prompt=[chat],
        params={
            "decoding_method": "greedy",
            "max_new_tokens": 20,
            "temperature": 0,
            "return_options": {
                "token_logprobs": True,
                "generated_tokens": True,
                "input_text": True,
                "top_n_tokens": 5,
            },
        },
    )
    print(result)  # Print the model's result for verification

    # Parse the output to get the label and probability of risk
    label, prob_of_risk = parse_output(result[0]["results"][0]["generated_tokens"])

    # Print the risk detection result and probability of risk
    print(f"\n# risk detected? : {label}")  # Yes
    print(f"# probability of risk: {prob_of_risk:.3f}")  # 0.987

    return label, prob_of_risk


def all_checks(user_input, ai_response=""):
    ai_risk = None
    ai_risk_prob = None
    relevance_risk = None
    relevance_risk_prob = None

    user_risk, user_risk_prob = check_user_risk(user_input)

    if user_risk == "Yes":
        return {
            "user_risk": user_risk,
            "user_risk_prob": user_risk_prob,
            "ai_risk": ai_risk,
            "ai_risk_prob": ai_risk_prob,
            "relevance_risk": relevance_risk,
            "relevance_risk_prob": relevance_risk_prob,
        }

    if user_risk == "No" and ai_response:
        ai_risk, ai_risk_prob = check_ai_risk(user_input, ai_response)

    if ai_response == "Yes":
        return {
            "user_risk": user_risk,
            "user_risk_prob": user_risk_prob,
            "ai_risk": ai_risk,
            "ai_risk_prob": ai_risk_prob,
            "relevance_risk": relevance_risk,
            "relevance_risk_prob": relevance_risk_prob,
        }

    if user_risk == "No" and ai_risk == "No":
        relevance_risk, relevance_risk_prob = check_answer_relevance(
            user_input, ai_response
        )

    # print(user_risk, ai_risk, relevance_risk)
    return {
        "user_risk": user_risk,
        "user_risk_prob": user_risk_prob,
        "ai_risk": ai_risk,
        "ai_risk_prob": ai_risk_prob,
        "relevance_risk": relevance_risk,
        "relevance_risk_prob": relevance_risk_prob,
    }


# Conditional script execution for testing
if __name__ == "__main__":
    user_prompt = "How can I figure out the center of gravity"
    ai_response = "You should not share your PIN code with anyone."
    # user_risk(user_prompt)
    print(all_checks(user_prompt, ai_response=ai_response))
