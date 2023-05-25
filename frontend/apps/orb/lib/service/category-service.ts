import { restApi } from 'common-utils/utils';
import { getUrlRoot } from 'common-utils/utils/common';

const urlBase = `${getUrlRoot()}/categories`;

export async function getCategories() {
    return restApi(urlBase);
}
