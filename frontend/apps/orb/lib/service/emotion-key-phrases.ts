import { restApi } from 'common-utils/utils';
import { getUrlRoot } from 'common-utils/utils/common';

const urlBase = `${getUrlRoot()}/data`;

export interface KeyPhrasesRequest {
    start_date: Date
    end_date: Date
    text_lang: string
    entity_name: string
    observer_type: string
    term: string
    emotion?: string
    limit?: number
}

export async function getEmotionKeyPhrases(keyPhrasesRequest: KeyPhrasesRequest) {
    const queryParams = new URLSearchParams();
    if (keyPhrasesRequest.start_date) {
        queryParams.set('start_date', keyPhrasesRequest.start_date.toISOString());
    }
    if (keyPhrasesRequest.end_date) {
        queryParams.set('end_date', keyPhrasesRequest.end_date.toISOString());
    }
    if (keyPhrasesRequest.text_lang && keyPhrasesRequest.text_lang !== 'All') {
        queryParams.set('text_lang', keyPhrasesRequest.text_lang);
    }
    if (keyPhrasesRequest.entity_name && keyPhrasesRequest.entity_name !== 'All') {
        queryParams.set('entity_name', keyPhrasesRequest.entity_name);
    }
    if (keyPhrasesRequest.observer_type && keyPhrasesRequest.observer_type !== 'All') {
        queryParams.set('observer_type', keyPhrasesRequest.observer_type);
    }
    if (keyPhrasesRequest.term && keyPhrasesRequest.term !== 'All') {
        queryParams.set('term', keyPhrasesRequest.term);
    }
    if (keyPhrasesRequest.emotion && keyPhrasesRequest.emotion !== 'All') {
        queryParams.set('emotion', keyPhrasesRequest.emotion);
    }
    if (keyPhrasesRequest.limit) {
        queryParams.set('limit', keyPhrasesRequest.limit.toString());
    }

    return restApi(`${urlBase}/key-phrases?${queryParams}`);
}
