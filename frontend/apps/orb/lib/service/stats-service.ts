import { restApi } from 'common-utils/utils';
import { getUrlRoot } from 'common-utils/utils/common';

export async function getStats(statsObjectUrl: string) {
    return restApi(`${getUrlRoot() + statsObjectUrl}/stats`);
}
