gpt_prompt_keyword_classification_template = '''
Task: For given reviews, news and search results, do label following keywords based on their meaning and provided description:
__KEYWORD_LIST__
Instructions:
- For each message, independently identify all likely keywords. 
- Process each review independently and don't mix up.
- Only tag a keywords if the confidence score is above 0.9
- Labelled keywords must be from given list, don't make up new keywords.
'''

department_list = [
    "Collaboration",
    "Employees",
    "Alert",
    "Production",
    "Safety",
    "Environment",
    "Growth",
    "Finance",
    "Legal",
    "Business",
    "Operation",
    "Events",
    "Facilities"
]

gpt_prompt_keyword_classification = gpt_prompt_keyword_classification_template.replace('__KEYWORD_LIST__', '''
Keywords with their keywords:
- Collaboration: collaboration and acquisition
- Employees: employee related
- Alert: any news which need immediate attention
- Production
- Safety:
- Environment: world environment related
- Growth: company growth related
- Finance:
- Legal:
- Business:
- Operation:
- Events: Coordination, events, decoration, artist
- Facilities: Housekeeping, maintenance, security
''')

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
        "name": "log_keywords",
        "description": "Save keyword names along with their sentiment",
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
                            "keywords": {
                                "type": "array",
                                "description": "Keyword names that are related to given text",
                                "items": {
                                    "type": "string",
                                }
                            }
                        },
                        "required": ["raw_data_id", "keywords"]
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
                                "description": "extract people names in pascal case without any salutation, " +
                                               "don't include organization names like Rio Tinto"
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
