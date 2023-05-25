import { Card, Group, Stack, Text, Title } from '@mantine/core';
import { Icon } from '@tabler/icons-react';

export interface StatsCardTitleProps {
    text: string;
}

interface MiniStatisticsCardProps {
    title: StatsCardTitleProps;
    count: number | string;
    countColor: string;
    percentage: { color: string; text: string };
    icon?: Icon;
}

export function MiniStatisticsCard({ title, count, countColor, percentage,
    icon: IconComponent }: MiniStatisticsCardProps) {
    return (
        <Card shadow="sm">
            <Group position="apart">
                <Stack spacing="xs">
                    <Title order={3} size="sm" color="gray">
                        {title.text}
                    </Title>
                    <Group spacing={5}>
                        <Text size="xl" color={countColor}>
                            {count}
                        </Text>
                        <Text size="xl" color={percentage.color}>
                            {percentage.text}
                        </Text>
                    </Group>
                </Stack>
                {IconComponent && <IconComponent color={countColor} />}
            </Group>
        </Card>
    );
}
