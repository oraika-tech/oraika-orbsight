import { restApi } from 'common-utils/utils';
import { getUrlRoot } from 'common-utils/utils/common';

const urlBase = `${getUrlRoot()}/entities`;

export async function getEntities() {
    return restApi(urlBase);
}

export async function updateEntityEnabled(id: string, isEnabled: boolean) {
    return restApi(
        `${urlBase}/${id}`,
        {
            method: 'PATCH',
            body: JSON.stringify({ enabled: isEnabled })
        }
    );
}
