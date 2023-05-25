import { Divider, Group, Paper, ScrollArea, Stack, Text, Title, Tooltip } from '@mantine/core';
import { IconClockHour5, IconUserCircle } from '@tabler/icons-react';
import { getLogoFromObserverType } from 'common-utils/utils/common';
import Image from 'next/image';
import ChipArray from '../Chip/ChipArray';
import Highlighted from '../Highlighted';

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

    const bgColor = '#84ffff'; // '#e0f2f1'; //emotion == 'positive' ? '#eeffee' : '#ffeeee';
    const tweeterHandlerRegex: string[] = []; // ['@\\w+']; disabled handle highlighting

    return (
        <Paper shadow="md" sx={{ padding: '0.5rem', borderRadius: '0.5rem', backgroundColor: bgColor }}>
            <Stack spacing="xs">

                <Group position="apart" h={24}>
                    <Group spacing={5}>
                        <Tooltip label={observerType} position="left">
                            <Image
                                src={logo}
                                width={24}
                                height={24}
                                style={{ paddingRight: '0.3rem' }}
                                alt={observerType}
                            />
                        </Tooltip>
                        <Title order={5} sx={{ minHeight: '1rem' }}>{entityName}</Title>
                    </Group>

                    <Group spacing={5}>
                        <IconUserCircle />
                        <Title order={6} sx={{ textAlign: 'left' }}> {authorName} </Title>
                    </Group>
                </Group>

                <Divider />

                <ScrollArea h={76}>
                    <Text variant="body2">
                        {/* <Paper shadow="xs" variant="elevation" sx={{ backgroundColor: bgColor }}> */}
                        <Highlighted text={text} chipHighlights={taxonomies} markHighlights={tweeterHandlerRegex} />
                        {/* </Paper> */}
                    </Text>
                </ScrollArea>

                <Divider />

                <Group position="apart" h={24}>
                    <ChipArray chipList={categories} bgColor="info" />
                    <Group spacing={5}>
                        <IconClockHour5 />
                        <Text variant="subtitle2" sx={{ textAlign: 'left' }}>
                            {eventTime.toLocaleString()}
                        </Text>
                    </Group>
                </Group>

            </Stack >
        </Paper >
    );
}
