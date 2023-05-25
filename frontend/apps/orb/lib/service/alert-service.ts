import { restApi } from 'common-utils/utils';
import { getUrlRoot } from 'common-utils/utils/common';

export async function getAlerts() {
    return restApi(`${getUrlRoot()}/grafana/alerts`);
}
