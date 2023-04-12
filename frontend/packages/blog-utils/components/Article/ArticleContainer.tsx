import { SimpleGrid } from '@mantine/core';
import { ArticleType } from '../../article-utils';
import ArticleItem from './ArticleItem';

export default function ArticleContainer({ posts }: { posts: ArticleType[] }) {
    return (
        <SimpleGrid
            cols={3}
            spacing="xl"
            breakpoints={[
                { maxWidth: 'md', cols: 2 },
                { maxWidth: 'xs', cols: 1 }
            ]}
        >
            {posts.map((article: ArticleType) => (
                <ArticleItem key={article.slug} article={article} />
            ))}
        </SimpleGrid>
    );
}
