import {
    Avatar,
    Badge,
    Center,
    Container,
    Grid,
    Group,
    Loader,
    Stack,
    Text,
    Title
} from '@mantine/core';
import dayjs from 'dayjs';
import TableOfContent from 'mantine-components/components/TableOfContent/TableOfContent';
import { MDXRemote } from 'next-mdx-remote';
import Image from 'next/image';

interface BlogPageProps {
    loading: boolean;
    components: any;
    post: any;
    classes: any;
}

export default function BlogPage({ loading, components, post, classes }: BlogPageProps) {
    const source = post ? post.source : {};
    return loading ? (
        <Center>
            <Loader />
        </Center>
    ) : (
        <Stack>
            {post.coverImage && (
                <Center>
                    <Image
                        src={`/assets/images/${post.coverImage}`}
                        alt="Cover Image"
                        width={600}
                        height={200}
                    />
                </Center>
            )}
            <Grid gutter="xl">
                <Grid.Col>
                    <Container size="md">
                        <Title className={classes.heading} align="center">{post.title}</Title>
                    </Container>
                </Grid.Col>
                <Grid.Col span={12} xs={10} sm={8} md={4}>
                    <TableOfContent tocItems={post.toc} />
                </Grid.Col>
                <Grid.Col span={12} xs={12} sm={12} md={8}>
                    <Container size="md">
                        <Stack spacing="md">
                            <Group position="apart">
                                {post.author && post.author.name && (
                                    <Group spacing={5}>
                                        {post.author.picture
                                            ? <Avatar
                                                radius="xl"
                                                src={`/assets/images/${post.author.picture}`}
                                            />
                                            : <Avatar radius="xl" />
                                        }
                                        <Text size="lg">
                                            {post.author.name}
                                        </Text>
                                    </Group>
                                )}
                                <Text style={{ color: '#6F6F6F', fontSize: 16, fontWeight: 300 }}>
                                    {dayjs(post.publishedAt).format('MMMM D, YYYY')}
                                    &nbsp; • &nbsp;
                                    {post.timeReading.text}
                                </Text>
                            </Group>
                            <MDXRemote
                                {...source}
                                components={components}
                            />
                            <Group spacing={5} position="right">
                                {post.tags.map((tag) => (
                                    <Badge
                                        key={tag}
                                        size="sm"
                                        variant="filled"
                                        radius="lg"
                                        className={classes.badge}
                                    >
                                        {tag}
                                    </Badge>
                                ))}
                            </Group>
                        </Stack>
                    </Container>
                </Grid.Col>
            </Grid>
        </Stack>
    );
}
