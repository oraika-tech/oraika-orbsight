import { restApi } from 'common-utils/utils';
import { getUrlRoot } from 'common-utils/utils/common';

const urlBase = `${getUrlRoot()}/me/tenants`;

export async function getTenants() {
    return restApi(urlBase);
}
