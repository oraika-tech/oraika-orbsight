import { restApi } from 'common-utils/utils';
import { getUrlRoot } from 'common-utils/utils/common';

const urlBase = `${getUrlRoot()}/data`;

export async function getTextAnalysisData() {
    const queryParams = new URLSearchParams();
    queryParams.set('limit', '30');

    return restApi(`${urlBase}/text?${queryParams}`);
}
