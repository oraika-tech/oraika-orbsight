import { restApi } from 'common-utils/utils';
import { getUrlRoot } from 'common-utils/utils/common';

const urlBase = `${getUrlRoot()}/taxonomies`;

export async function getTaxonomies() {
    return restApi(urlBase);
}
