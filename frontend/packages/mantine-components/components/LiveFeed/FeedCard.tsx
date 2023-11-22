import { Divider, Group, Paper, ScrollArea, Stack, Text, Title, Tooltip } from '@mantine/core';
import { IconClockHour5, IconUserCircle } from '@tabler/icons-react';
import { getLogoFromObserverType } from 'common-utils/utils/common';
import Image from 'next/image';
import ChipArray from '../Chip/ChipArray';
import Highlighted from '../Highlighted';
import classes from './FeedCard.module.css';

interface FeedData {
    observerType: string
    entityName: string
    text: string
    authorName: string
    eventTime: Date
    categories: string[]
    taxonomies: string[]
}

export default function FeedCard({ observerType, entityName, text,
    authorName, eventTime, categories, taxonomies }: FeedData) {
    const logo = getLogoFromObserverType(observerType);

    const tweeterHandlerRegex: string[] = []; // ['@\\w+']; disabled handle highlighting

    return (
        <Paper shadow="md" className={classes.paper}>
            <Stack gap="xs">

                <Group justify="space-between" h={24}>
                    <Group gap={5}>
                        <Tooltip label={observerType} position="left">
                            <Image
                                src={logo}
                                width={24}
                                height={24}
                                style={{ paddingRight: '0.3rem' }}
                                alt={observerType}
                            />
                        </Tooltip>
                        <Title order={5} style={{ minHeight: '1rem' }}>{entityName}</Title>
                    </Group>

                    <Group gap={5}>
                        <IconUserCircle />
                        <Title order={6} style={{ textAlign: 'left' }}> {authorName} </Title>
                    </Group>
                </Group>

                <Divider />

                <ScrollArea h={76}>
                    <Text variant="body2">
                        {/* <Paper shadow="xs" variant="elevation" style={{ backgroundColor: bgColor }}> */}
                        <Highlighted text={text} chipHighlights={taxonomies} markHighlights={tweeterHandlerRegex} />
                        {/* </Paper> */}
                    </Text>
                </ScrollArea>

                <Divider />

                <Group justify="space-between" h={24}>
                    <ChipArray chipList={categories} bgColor="info" />
                    <Group gap={5}>
                        <IconClockHour5 />
                        <Text variant="subtitle2" style={{ textAlign: 'left' }}>
                            {eventTime.toLocaleString()}
                        </Text>
                    </Group>
                </Group>

            </Stack>
        </Paper>
    );
}
