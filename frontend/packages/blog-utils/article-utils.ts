import readingTime from 'reading-time';
import { BaseMdxType, BaseMdxUtils } from './base-mdx-utils';
import { getHeadings } from './md-utils';

export interface AuthorType {
    name: string;
    picture: string;
}

export interface TocItem {
    text: string;
    level: number;
}

export interface ArticleType extends BaseMdxType {
    title: string;
    excerpt: string;
    publishedAt: Date,
    coverImage: string;
    author: AuthorType;
    timeReading: {
        text: string,
        minutes: number,
        time: number,
        words: number
    },
    toc: TocItem[];
    ogImage: {
        url: string;
    };
}

export class ArticleUtils extends BaseMdxUtils<ArticleType> {
    getPageBySlug(slug: string): ArticleType {
        const { data, content } = this.getRawPageBySlug(slug);
        const timeReading: any = readingTime(content);
        const tocItems: TocItem[] = getHeadings(content);

        const articleData: ArticleType = {
            slug,
            toc: tocItems || [],
            content,
            timeReading,
            title: data.title,
            publishedAt: data.publishedAt,
            coverImage: data.coverImage || null,
            author: data.author,
            excerpt: data.excerpt,
            tags: data.tags || [],
            ogImage: data.ogImage || null
        };

        return articleData;
    }
}
