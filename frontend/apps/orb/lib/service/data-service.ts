import { restApi } from 'common-utils/utils';
import { getUrlRoot } from 'common-utils/utils/common';

const urlBase = `${getUrlRoot()}/data`;

export interface DataRequest {
    start_date?: Date
    end_date?: Date
    text_lang?: string
    entity_name?: string
    observer_type?: string
    term?: string
    emotion?: string
}

export async function getData(subUrl: string, dataRequest: DataRequest) {
    const queryParams = new URLSearchParams();
    if (dataRequest.start_date) {
        queryParams.set('start_date', dataRequest.start_date.toISOString());
    }
    if (dataRequest.end_date) {
        queryParams.set('end_date', dataRequest.end_date.toISOString());
    }
    if (dataRequest.text_lang && dataRequest.text_lang !== 'All') {
        queryParams.set('text_lang', dataRequest.text_lang);
    }
    if (dataRequest.entity_name && dataRequest.entity_name !== 'All') {
        queryParams.set('entity_name', dataRequest.entity_name);
    }
    if (dataRequest.observer_type && dataRequest.observer_type !== 'All') {
        queryParams.set('observer_type', dataRequest.observer_type);
    }
    if (dataRequest.term && dataRequest.term !== 'All') {
        queryParams.set('term', dataRequest.term);
    }
    if (dataRequest.emotion && dataRequest.emotion !== 'All') {
        queryParams.set('emotion', dataRequest.emotion);
    }

    return restApi(`${urlBase + subUrl}?${queryParams}`);
}

export async function getDirectData(url: string) {
    return restApi(getUrlRoot() + url);
}

export async function getPanelData(key: string) {
    const queryParams = new URLSearchParams();
    queryParams.set('panel', key);
    return restApi(`${getUrlRoot()}/dashboards/panels?${queryParams}`);
}
