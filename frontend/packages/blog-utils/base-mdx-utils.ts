import fs from 'fs';
import matter from 'gray-matter';
import { join } from 'path';

export interface BaseMdxType {
    slug: string;
    tags?: string[];
    content: string;
}

export abstract class BaseMdxUtils<PageType extends BaseMdxType> {
    mdxDirectory: string;

    constructor(mdxDirectory: string) {
        this.mdxDirectory = join(process.cwd(), mdxDirectory);
    }

    abstract getPageBySlug(slug: string): PageType;

    getRawPageBySlug(slug: string): matter.GrayMatterFile<string> {
        const fullPath = join(this.mdxDirectory, `${slug}.mdx`);
        const fileContents = fs.readFileSync(fullPath, 'utf8');
        return matter(fileContents);
    }

    getAllSlugs(): Array<string> {
        return fs
            .readdirSync(this.mdxDirectory)
            .map((slug) => slug.replace(/\.mdx$/, ''));
    }

    getAllPages(): Array<PageType> {
        return this.getAllSlugs().map((slug) => this.getPageBySlug(slug));
    }

    getPageByTag(tag: string): Array<PageType> {
        return this.getAllPages().filter((page) => {
            const tags = page.tags ?? [];
            return tags.includes(tag);
        });
    }

    getAllTags(): Array<string> {
        const pages = this.getAllPages();
        const allTags = new Set<string>();
        pages.forEach((page) => {
            const tags = page.tags as Array<string>;
            tags.forEach((tag) => allTags.add(tag));
        });
        return Array.from(allTags);
    }
}
