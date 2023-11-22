import { Card, NavLink, Stack, Title } from '@mantine/core';
import { getHeadingAnchor } from 'blog-utils/md-utils';
import classes from './TableOfContent.module.css';

interface TocItem {
    text: string;
    level: number;
}

interface TableOfContentProps {
    tocItems: TocItem[];
}

function getNavs(tocItems: TocItem[]) {
    const levelCount = [0, 0, 0, 0];
    return tocItems.map((item) => {
        levelCount[item.level - 2] += 1;
        const label = `${levelCount.slice(0, item.level - 1).join('.')}. ${item.text}`;
        const idText = getHeadingAnchor(item.text);
        return (
            <NavLink
                pr={15}
                key={idText}
                label={label}
                component="a"
                href={`#${idText}`}
                style={{ marginLeft: (item.level - 2) * 10 }}
            />
        );
    });
}

export default function TableOfContent({ tocItems }: TableOfContentProps) {
    return (
        <Card className={classes.card} shadow="xl" radius="lg" p={20}>
            <Stack justify="flex-start" gap={0}>
                <Title order={4}>
                    Table of Content
                </Title>
                {getNavs(tocItems)}
            </Stack>
        </Card>
    );
}
