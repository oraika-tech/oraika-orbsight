import json
import logging
import os
import sys

import openai
import tiktoken

from service.common.utils import extract_json

openai.api_key = os.environ["OPENAI_API_KEY"]

logger = logging.getLogger(__name__)

MODEL_NAME = 'gpt-3.5-turbo'
MODEL_CONTEXT_SIZE = 4096


def prompt(system_message: str, fx_params_def, user_message):
    final_messages = [
        {"role": "system", "content": system_message}
    ]
    for raw_data in user_message:
        final_messages.append({"role": "user", "content": json.dumps(raw_data)})

    max_token_count = (MODEL_CONTEXT_SIZE
                       - num_tokens_from_messages(final_messages)
                       - num_tokens_from_functions(fx_params_def))

    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=final_messages,
            functions=fx_params_def,
            function_call={"name": fx_params_def[0]['name']},
            max_tokens=max_token_count,
            temperature=0
        )
    except openai.error.AuthenticationError:
        # logger.error("OpenAI API failure: %s", error.user_message) # openai itself is logging
        sys.exit(127)  # Why exit ? No point hitting expired token

    return json.loads(response.choices[0].message.function_call.arguments)['data']


def prompt_plain(system_message: str, user_message):
    system_message = "You are a microservice which strictly communicate only in json format. " + \
                     "You will be given json input and you will give json output. " + \
                     system_message

    final_messages = [
        {"role": "system", "content": system_message}
    ]
    for raw_data in user_message:
        final_messages.append({"role": "user", "content": json.dumps(raw_data)})

    max_token_count = MODEL_CONTEXT_SIZE - num_tokens_from_messages(final_messages)
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=final_messages,
        max_tokens=max_token_count,
        temperature=0
    )
    return extract_json(response.choices[0].message.content)


def num_tokens_from_functions(functions, model="gpt-3.5-turbo-0613"):
    (encoding, tokens_per_message, tokens_per_name) = _get_encoding(model)
    return len(encoding.encode(json.dumps(functions)))


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    (encoding, tokens_per_message, tokens_per_name) = _get_encoding(model)
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def _get_encoding(model):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return _get_encoding(model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return _get_encoding(model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. 
                Information on how messages are converted to tokens:
                https://github.com/openai/openai-python/blob/main/chatml.md"""
        )
    return encoding, tokens_per_message, tokens_per_name
