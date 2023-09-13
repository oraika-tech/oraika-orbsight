import logging
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from analyzer.data.common_data import gpt_prompt_sentiment_analysis, sentiment_fx, classification_fx
from analyzer.data.playarena_data import activities as playarena_activities
from analyzer.data.playarena_data import department_list as playarena_department_list
from analyzer.data.playarena_data import department_sublist as playarena_department_sublist
from analyzer.data.playarena_data import gpt_prompt_department_classification as playarena_classification_prompt
from analyzer.data.playjuniors_data import activities as playjuniors_activities
from analyzer.data.playjuniors_data import department_list as playjuniors_department_list
from analyzer.data.playjuniors_data import department_sublist as playjuniors_department_sublist
from analyzer.data.playjuniors_data import gpt_prompt_department_classification as playjuniors_classification_prompt
from analyzer.model.structure_data_request import UnstructuredDataRequest, StructuredData
from analyzer.service.gpt_client import prompt
from analyzer.service.utils import split_array, flatten_array, intersect_arrays

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


tenant_data = {
    'b6d5a44a-4626-491a-8fc0-3a11344d97f7': {
        'department_list': playjuniors_department_list,
        'department_sublist': playjuniors_department_sublist,
        'classification_prompt': playjuniors_classification_prompt,
        'activities': playjuniors_activities
    },
    '02ddd60c-2d58-47cc-a445-275d8e621252': {
        'department_list': playarena_department_list,
        'department_sublist': playarena_department_sublist,
        'classification_prompt': playarena_classification_prompt,
        'activities': playarena_activities
    }
}


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


def text_classification(tenant_id: UUID, reviews: list) -> list[TextClassification]:
    data = tenant_data[str(tenant_id)]
    reviews_list = split_array(reviews, 10)
    response_list = [prompt(data['classification_prompt'], classification_fx, reviews_sublist)
                     for reviews_sublist in reviews_list]
    response = flatten_array(response_list)
    return [segregate_tags_terms(data, response_element) for response_element in response]


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


def review_analysis(tenant_id: UUID, reviews: list[UnstructuredDataRequest]) -> list[StructuredData]:
    if len(reviews) == 0:
        return []

    review_list = [el.dict() for el in reviews]
    classified_reviews = text_classification(tenant_id, review_list)
    reviews_sentiment = text_sentiment_analysis(review_list)

    return [
        StructuredData(
            raw_data_id=review_data[0].raw_data_id,  # - input
            tags=review_data[1].tags,  # ------------------ gpt - classifier
            terms=review_data[1].terms,  # ---------------- gpt - classifier
            categories=[],  # ----------------------------- constant
            emotion=review_data[2].sentiment,  # ---------- gpt - sentiment analysis
            text_length=len(review_data[0].raw_text),  # calc
            text_language='en',  # ------------------------ constant
            remark=None  # -------------------------------- constant
        )
        for review_data in zip(reviews, classified_reviews, reviews_sentiment)
    ]
