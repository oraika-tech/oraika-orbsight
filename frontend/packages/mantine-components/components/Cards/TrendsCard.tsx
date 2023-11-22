import { ActionIcon, Group, Stack, Title } from '@mantine/core';
import { IconTrendingDown, IconTrendingUp } from '@tabler/icons-react';
import classes from './TrendsCard.module.css';

interface TrendsCardProps {
    percentage: number
    isTrendUp: boolean
    description: string
}

export default function TrendsCard({ percentage, isTrendUp, description }: TrendsCardProps) {
    return (
        <Stack>
            <Group justify="center">
                <Title className={classes.heading1}>{percentage}%</Title>
                <ActionIcon
                    variant="gradient"
                    p={5}
                    size="lg"
                    gradient={{ from: 'var(--mantine-color-blue-2)', to: 'var(--mantine-color-blue-7)' }}
                >
                    {isTrendUp
                        ? <IconTrendingUp stroke={3} />
                        : <IconTrendingDown stroke={3} />

                    }
                </ActionIcon>
            </Group>
            <Title ta="center" order={5}> {description} </Title>
        </Stack>
    );
}
