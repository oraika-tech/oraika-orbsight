import { restApi } from 'common-utils/utils';
import { getUrlRoot } from 'common-utils/utils/common';

const urlBase = `${getUrlRoot()}/observers`;

export async function getDataSources() {
    return restApi(urlBase);
}

export async function updateDataSourceEnabled(id: string, isEnabled: boolean) {
    return restApi(
        `${urlBase}/${id}`,
        {
            method: 'PATCH',
            body: JSON.stringify({ enabled: isEnabled })
        }
    );
}
