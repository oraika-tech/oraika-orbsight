gpt_prompt_sentiment_analysis = '''
You are an expert sentiment analyser. Evaluate sentiment of a given text and choose following options:
- positive: Complete text is positive
- negative: Complete text is negative
- neutral: Text is either neutral or mix of positive and negative
- undetermined: Not enough text to determine sentiment
'''

gpt_prompt_department_classification_template = '''
Task: Classify departments based on customer reviews for a sports activity centre.
__DEPARTMENT_LIST__
Instructions:
- For each customer review, independently identify all likely departments based on the presence of keywords or their implied meaning.
- Choose as many as possible departments from above list.
- Only tag a department if the confidence score is above 0.9
- Process each review independently and don't mix up.
'''

gpt_prompt_people_analysis = '''You are an expert ner analyser. Extract all people names of a given text.'''

sentiment_fx = [
    {
        "name": "sentiment_logger",
        "description": "Store sentiment of text by id for later use",
        "parameters": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "raw_data_id": {
                                "type": "integer"
                            },
                            "sentiment": {
                                "type": "string",
                                "description": "Choose one of sentiments - positive, negative, neutral, undetermined"
                            }
                        },
                        "required": ["raw_data_id", "sentiment"]
                    }
                }
            },
            "required": ["data"]
        }
    }
]

classification_fx = [
    {
        "name": "log_departments",
        "description": "Save department names along with their sentiment",
        "parameters": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "raw_data_id": {
                                "type": "integer"
                            },
                            "departments": {
                                "type": "array",
                                "description": "Department names that are related to given text",
                                "items": {
                                    "type": "string",
                                }
                            }
                        },
                        "required": ["raw_data_id", "departments"]
                    }
                }
            },
            "required": ["data"]
        }
    }
]

people_fx = [
    {
        "name": "people_logger",
        "description": "Store people names of text by id for later use",
        "parameters": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "raw_data_id": {
                                "type": "integer"
                            },
                            "people": {
                                "type": "array",
                                'items': {'type': 'string'},
                                "description": "extract people names in pascal case without any salutation"
                            }
                        },
                        "required": ["raw_data_id", "people"]
                    }
                }
            },
            "required": ["data"]
        }
    }
]
