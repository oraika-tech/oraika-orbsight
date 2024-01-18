import logging
from enum import Enum
from typing import List
from uuid import UUID

from pydantic import BaseModel

from service.common.utils.utils import intersect_arrays, split_array, flatten_array, convert_to_pascal
from service.workflow.nodes.analyzer.data.common_data import gpt_prompt_sentiment_analysis, sentiment_fx, classification_fx, \
    gpt_prompt_people_analysis, people_fx
from service.workflow.nodes.analyzer.data.playarena_data import activities as playarena_activities
from service.workflow.nodes.analyzer.data.playarena_data import department_list as playarena_department_list
from service.workflow.nodes.analyzer.data.playarena_data import department_sublist as playarena_department_sublist
from service.workflow.nodes.analyzer.data.playarena_data import gpt_prompt_department_classification as playarena_classification_prompt
from service.workflow.nodes.analyzer.data.playjuniors_data import activities as playjuniors_activities
from service.workflow.nodes.analyzer.data.playjuniors_data import department_list as playjuniors_department_list
from service.workflow.nodes.analyzer.data.playjuniors_data import department_sublist as playjuniors_department_sublist
from service.workflow.nodes.analyzer.data.playjuniors_data import gpt_prompt_department_classification as playjuniors_classification_prompt
from service.workflow.nodes.analyzer.data.trustpavilion_data import classification_fx as trustpavilion_classification_fx
from service.workflow.nodes.analyzer.data.trustpavilion_data import gpt_prompt_keyword_classification as trustpavilion_classification_prompt
from service.workflow.nodes.analyzer.domain_models import UnstructuredDataRequest, StructuredData
from service.workflow.nodes.analyzer.gpt_client import prompt

logger = logging.getLogger(__name__)


class TextClassification(BaseModel):
    raw_data_id: int
    tags: list[str]
    terms: list[str]


class Sentiment(str, Enum):
    NEGATIVE = 'negative'
    UNDETERMINED = 'undetermined'
    POSITIVE = 'positive'
    NEUTRAL = 'neutral'


class TextSentiment(BaseModel):
    raw_data_id: int
    sentiment: Sentiment


class TextPeople(BaseModel):
    raw_data_id: int
    people: List[str]


def segregate_tags_terms(data, classification_response):
    tags = [department for department in classification_response['departments']
            if department in data['department_list']]
    terms = [department for department in classification_response['departments']
             if department in data['activities']]

    for activities in data["department_sublist"]:
        if activities not in tags and len(intersect_arrays(data["department_sublist"][activities], terms)) > 0:
            tags.append(activities)

    return TextClassification(
        raw_data_id=classification_response['raw_data_id'],
        tags=tags,
        terms=terms
    )


def get_text_classification(classification_response):
    return TextClassification(
        raw_data_id=classification_response['raw_data_id'],
        tags=classification_response['keywords'],
        terms=[]
    )


tenant_data = {
    'b6d5a44a-4626-491a-8fc0-3a11344d97f7': {
        'is_playarena': True,
        'department_list': playjuniors_department_list,
        'department_sublist': playjuniors_department_sublist,
        'classification_prompt': playjuniors_classification_prompt,
        'classification_fx': classification_fx,
        'activities': playjuniors_activities
    },
    '02ddd60c-2d58-47cc-a445-275d8e621252': {
        'is_playarena': True,
        'department_list': playarena_department_list,
        'department_sublist': playarena_department_sublist,
        'classification_prompt': playarena_classification_prompt,
        'classification_fx': classification_fx,
        'activities': playarena_activities
    },
    '0b020761-b2a3-494d-b777-4024c92fe4ec': {
        'is_playarena': False,
        'classification_prompt': trustpavilion_classification_prompt,
        'classification_fx': trustpavilion_classification_fx
    }
}


def text_classification(tenant_id: UUID, reviews: list) -> list[TextClassification]:
    data = tenant_data[str(tenant_id)]
    reviews_list = split_array(reviews, 10)
    response_list = [
        prompt(
            data['classification_prompt'],
            data['classification_fx'],
            reviews_sublist
        )
        for reviews_sublist in reviews_list
    ]
    response = flatten_array(response_list)
    logger.info("response: %s", response)
    if data['is_playarena']:
        return [segregate_tags_terms(data, response_element) for response_element in response]
    else:
        return [get_text_classification(response_element) for response_element in response]


def text_sentiment_analysis(reviews: list) -> list[TextSentiment]:
    reviews_list = split_array(reviews, 10)
    response_list = [prompt(gpt_prompt_sentiment_analysis, sentiment_fx, reviews_sublist)
                     for reviews_sublist in reviews_list]
    response = flatten_array(response_list)
    return [
        TextSentiment(
            raw_data_id=element['raw_data_id'],
            sentiment=element['sentiment']
        )
        for element in response
    ]


def correct_name_case(people_list: List[str]) -> List[str]:
    return [convert_to_pascal(people) for people in people_list]


def text_people_analysis(reviews: list) -> list[TextPeople]:
    reviews_list = split_array(reviews, 10)
    response_list = [prompt(gpt_prompt_people_analysis, people_fx, reviews_sublist)
                     for reviews_sublist in reviews_list]
    response = flatten_array(response_list)
    return [
        TextPeople(
            raw_data_id=element['raw_data_id'],
            people=correct_name_case(element['people'])
        )
        for element in response
    ]


def review_analysis(tenant_id: UUID, reviews: list[UnstructuredDataRequest]) -> list[StructuredData]:
    if len(reviews) == 0:
        return []

    review_list = [el.model_dump() for el in reviews]
    classified_reviews = text_classification(tenant_id, review_list)
    reviews_sentiment = text_sentiment_analysis(review_list)
    reviews_people = {people_info.raw_data_id: people_info.people for people_info in text_people_analysis(review_list)}

    return [
        StructuredData(
            raw_data_id=review_data[0].raw_data_id,  # ---------------------- input
            tags=review_data[1].tags,  # ------------------------------------ gpt - classifier
            terms=review_data[1].terms,  # ---------------------------------- gpt - classifier
            categories=[],  # ----------------------------------------------- constant
            people=reviews_people.get(review_data[0].raw_data_id, []),  # --- gpt - people names
            emotion=review_data[2].sentiment,  # ---------------------------- gpt - sentiment analysis
            text_length=len(review_data[0].raw_text),  # -------------------- calc
            text_language='en',  # ------------------------------------------ constant
            remark=None  # -------------------------------------------------- constant
        )
        for review_data in zip(reviews, classified_reviews, reviews_sentiment)
    ]
