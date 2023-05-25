import { restApi } from 'common-utils/utils';
import { getUrlRoot } from 'common-utils/utils/common';

const urlBase = `${getUrlRoot()}/data`;

export interface WordCloudRequest {
    start_date: Date
    end_date: Date
    text_lang: string
    entity_name: string
    observer_type: string
    term: string
    emotion?: string
}

export async function getEmotionWordCloud(wordCloudRequest: WordCloudRequest) {
    const queryParams = new URLSearchParams();
    if (wordCloudRequest.start_date) {
        queryParams.set('start_date', wordCloudRequest.start_date.toISOString());
    }

    if (wordCloudRequest.end_date) {
        queryParams.set('end_date', wordCloudRequest.end_date.toISOString());
    }

    if (wordCloudRequest.text_lang && wordCloudRequest.text_lang !== 'All') {
        queryParams.set('text_lang', wordCloudRequest.text_lang);
    }

    if (wordCloudRequest.entity_name && wordCloudRequest.entity_name !== 'All') {
        queryParams.set('entity_name', wordCloudRequest.entity_name);
    }

    if (wordCloudRequest.observer_type && wordCloudRequest.observer_type !== 'All') {
        queryParams.set('observer_type', wordCloudRequest.observer_type);
    }

    if (wordCloudRequest.term && wordCloudRequest.term !== 'All') {
        queryParams.set('term', wordCloudRequest.term);
    }

    if (wordCloudRequest.emotion && wordCloudRequest.emotion !== 'All') {
        queryParams.set('emotion', wordCloudRequest.emotion);
    }

    return restApi(`${urlBase}/word-cloud?${queryParams}`);
}
