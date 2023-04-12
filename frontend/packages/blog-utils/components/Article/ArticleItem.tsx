import dayjs from 'dayjs';
import Image from 'next/image';

import { Avatar, Badge, Group, Paper, Stack, Text, Title, createStyles } from '@mantine/core';
import Link from 'next/link';
import { ArticleType } from '../../article-utils';

interface Props {
  article: ArticleType;
};

const useStyles = createStyles((theme) => ({
  link: {
    textDecoration: 'none',
    color: '#101010'
  },
  container: {
    height: '100%'
  },
  card: {
    minWidth: 250,
    maxWidth: 350,
  }
}));

export default function ArticleItem({ article }: Props) {
  const { classes } = useStyles();
  return (
    <Paper withBorder p={20} radius={20} className={classes.card}>
      <Link className={classes.link} as={`/blog/${article.slug}`} href="/blog/[slug]">

        <Stack className={classes.container} justify="space-between">
          <Stack spacing={10}>

            {article.ogImage && article.ogImage.url && (
              <Image
                src={article.ogImage.url}
                alt="Image for article"
                style={{ width: '100%', height: 250, borderRadius: 5 }}
              />
            )}

            {article.author && article.author.name && (
              <Group spacing={5}>
                {article.author.picture
                  ? <Avatar radius="xl" src={`/assets/images/${article.author.picture}`} />
                  : <Avatar radius="xl" />
                }
                <Text size="lg">
                  {article.author.name}
                </Text>
              </Group>
            )}

            <Title order={4} align="left">
              {article.title}
            </Title>

            <Text align="left">
              {article.excerpt}
            </Text>

          </Stack>

          <Stack>

            <Text style={{ color: '#6F6F6F', fontSize: 16, fontWeight: 300 }}>
              {dayjs(article.publishedAt).format('MMMM D, YYYY')}
              &nbsp; • &nbsp;
              {article.timeReading.text}
            </Text>

            <Group spacing={5}>
              {article.tags.map((tag) => (
                <Badge key={tag} variant="filled" radius="lg" color="teal"> {tag} </Badge>
              ))}
            </Group>

          </Stack>

        </Stack>
      </Link>
    </Paper>
  );
}
