import { BaseMdxType, BaseMdxUtils } from './base-mdx-utils';

export interface DocType extends BaseMdxType {
    title?: string;
}

export class DocUtils extends BaseMdxUtils<DocType> {
    getPageBySlug(slug: string): DocType {
        const { data, content } = this.getRawPageBySlug(slug);

        const docData: DocType = {
            slug,
            content,
            title: data.title || null,
            tags: data.tags || []
        };

        return docData;
    }
}
