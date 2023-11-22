import { SimpleGrid } from '@mantine/core';
import { ArticleType } from '../../article-utils';
import ArticleItem from './ArticleItem';

export default function ArticleContainer({ posts }: { posts: ArticleType[] }) {
    return (
        <SimpleGrid
            cols={{ base: 1, xs: 2, md: 3 }}
            spacing="xl"
        >
            {posts.map((article: ArticleType) => (
                <ArticleItem key={article.slug} article={article} />
            ))}
        </SimpleGrid>
    );
}
