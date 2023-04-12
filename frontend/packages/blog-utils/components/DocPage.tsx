import {
    Center,
    Container,
    Loader
} from '@mantine/core';
import { MDXRemote } from 'next-mdx-remote';

interface BlogPageProps {
    loading: boolean;
    components?: any;
    doc: any;
}

export default function DocPage({ loading, components, doc }: BlogPageProps) {
    const source = doc ? doc.source : {};
    return loading ? (
        <Center>
            <Loader />
        </Center>
    ) : (
        <Container size="md">
            <MDXRemote
                {...source}
                components={components}
            />
        </Container>
    );
}
