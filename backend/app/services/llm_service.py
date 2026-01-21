def generate(prompt: str) -> str:
    """
    Fast enterprise-safe response generator.
    """
    if "Context:" in prompt:
        context = prompt.split("Context:")[1].split("Question:")[0].strip()
        return (
            "Here is the information I found based on internal knowledge:\n\n"
            + context
        )

    return "I can access internal enterprise knowledge."
