import { Card, Group, Stack, Text, Title } from '@mantine/core';
import { Icon } from '@tabler/icons-react';

export interface StatsCardTitleProps {
    text: string;
}

interface MiniStatisticsCardProps {
    title: StatsCardTitleProps;
    count: number | string;
    countColor: string;
    percentage: { color: string[]; text: number | string };
    icon?: Icon;
}

export function MiniStatisticsCard({ title, count, countColor, percentage,
    icon: IconComponent }: MiniStatisticsCardProps) {
    const percentageColor = typeof percentage.text === 'string'
        ? percentage.color[0] // single color for text type
        : percentage.text > 0
            ? percentage.color[0] // postive % color
            : percentage.text < 0
                ? percentage.color[1] // negative % color
                : 'gray';
    const percentageText = typeof percentage.text === 'string' ? percentage.text : `${percentage.text}%`;

    return (
        <Card shadow="sm">
            <Group position="apart">
                <Stack spacing="xs">
                    <Title order={2} size="sm" color="gray">
                        {title.text}
                    </Title>
                    <Group spacing={5} align="flex-end">
                        <Text size="xl" fw="bolder" color={countColor}>
                            {count}
                        </Text>
                        <Text size="md" pb={1.5} fw="bold" color={percentageColor}>
                            {percentageText}
                        </Text>
                    </Group>
                </Stack>
                {IconComponent && <IconComponent color={countColor} />}
            </Group>
        </Card>
    );
}
