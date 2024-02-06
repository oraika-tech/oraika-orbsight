import { Paper } from '@mantine/core';
import DocPage from 'blog-utils/components/DocPage';
import { DocUtils } from 'blog-utils/doc-utils';
import { serialize } from 'next-mdx-remote/serialize';
import ErrorPage from 'next/error';
import { useRouter } from 'next/router';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import rehypeCodeTitles from 'rehype-code-titles';
import rehypeSlug from 'rehype-slug';

const docsUtils = new DocUtils('docs');

export default function Doc({ doc }) {
    const router = useRouter();

    if (!router.isFallback && !doc?.slug) {
        return <ErrorPage statusCode={404} />;
    }

    return (
        <Paper>
            <DocPage
                loading={router.isFallback}
                doc={doc}
            />
        </Paper>
    );
}

export async function getStaticProps({ params }) {
    //fetch the particular file based on the slug
    const { slug } = params;
    const docData = docsUtils.getPageBySlug(slug);

    const mdxSource = await serialize(docData.content, {
        mdxOptions: {
            rehypePlugins: [
                rehypeSlug,
                [
                    rehypeAutolinkHeadings,
                    {
                        properties: { className: ['anchor'] }
                    },
                    { behaviour: 'wrap' }
                ],
                // rehypeHighlight,
                rehypeCodeTitles
            ]
        }
    });

    return {
        props: {
            doc: {
                ...docData,
                source: mdxSource,
                slug
            }
        }
    };
}

// dynamically generate the slugs for each doc(s)
export async function getStaticPaths() {
    const paths = (await docsUtils.getAllSlugs()).map((slug) => ({ params: { slug } }));

    return {
        paths,
        fallback: false
    };
}
