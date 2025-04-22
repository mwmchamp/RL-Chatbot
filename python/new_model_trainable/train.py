import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Want to use PPO with gpt2 (relatively boring chatbot) bootstrapped against each other over epochs
# Chatbots alternate learning and being static, and talk to each other
# Reward is length of response and semantic coherence
# Goal = Proof of concept for chatbots talking to themselves to increase complexity

def get_log_probs(model, input_ids, generated_ids):
    pass

def get_reward(conversation):

    # Return coherence_reward, uniqueness_reward, length_reward
    pass

def simulate_conversation(learning_model, static_model, turns_per_convo, starting_phrase):
    # Generate a series of call and responses starting with the starting phrase and then alternating b/w learning and static

    # Calculate reward and log probs
    # reward = alpha * coherence_reward + beta * coherence_reward + gamma * length_reward

    pass

def train(model, epochs, turns_per_bot, turns_per_convo):
    # each epoch, for turns_per_bot, do one convo with one model as learning, one model as static, calculate reward and log probs, do PPO
    # Swap the model used for learning and the model used as static, repeat
    # Each epoch, print reward per bot and the starting and ending phrase - want to return reward types separately for graphing

    pass

def evaluate(model, epochs, turns_per_convo):
    pass