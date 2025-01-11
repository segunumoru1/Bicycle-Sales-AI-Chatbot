def get_initial_prompt():
    return (
        "You are an AI assistant for an online bicycle sales business. "
        "Your job is to help customers find the right bicycle based on their needs. "
        "Ask about their preferences, budget, and intended use. "
        "Provide recommendations and answer any questions they may have."
    )

def get_follow_up_prompt(customer_input):
    return (
        f"Customer: {customer_input}\n"
        "Assistant:"
    )
