import json
import logging
import os
import sys

import openai

from analyzer.service.gpt_utils import num_tokens_from_messages, num_tokens_from_functions
from analyzer.service.utils import extract_json

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
