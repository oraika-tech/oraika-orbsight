import { restApi } from 'common-utils/utils';
import { getUrlRoot } from 'common-utils/utils/common';

const urlBase = `${getUrlRoot()}/visualization`;

export function getDashboards(frontendKey: string) {
    let url = `${urlBase}/dashboards`;
    if (frontendKey) {
        url += `?frontend_key=${frontendKey}`;
    }
    return restApi(url, { method: 'GET' });
}

export function getDashboard(dashboard_id: string, filters: object[]) {
    return restApi(
        `${urlBase}/dashboards/${dashboard_id}`,
        {
            method: 'POST',
            body: JSON.stringify({ filters })
        });
}
