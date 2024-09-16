import json
import os

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def get_config(config_filename="config.json"):
    """
    Reads the configuration file and returns it as a dictionary.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(
        current_dir, "..", "..", "configs", config_filename
    )

    with open(config_path, "r") as file:
        config_data = json.load(file)

    return config_data


def process_llm_request(
    job_description,
    openai_api_key,
    model_name,
    config_filename="config.json",
):
    """
    Processes the input through Langchain's LLM pipeline, using system prompts,
    user template,
    and job description.

    Args:
    - system_prompt: The system-level prompt for the LLM.
    - user_template: The template for user input in the LLM chain.
    - job_description: The input that the user provides for the function to
                       process.
    - config_filename: Optional, specify config file if different from default.

    Returns:
    - response from the LLM based on the input provided.
    """
    config = get_config(config_filename)

    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model_name=model_name,
    )
    prompt = ChatPromptTemplate(
        messages=[
            ("system", config["SYSTEM_PROMPT"]),
            ("user", config["USER_PROMPT"]),
        ]
    )

    chain = prompt | llm

    response = chain.invoke({"job_description": job_description})
    prefill_text = config["PREFILL_TEXT"]
    full_text = prefill_text + response.content
    return full_text
