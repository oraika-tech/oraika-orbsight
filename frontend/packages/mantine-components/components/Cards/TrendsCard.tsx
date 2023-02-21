import { ActionIcon, createStyles, Group, Stack, Title } from '@mantine/core';
import { IconTrendingDown, IconTrendingUp } from '@tabler/icons-react';

interface TrendsCardProps {
    percentage: number
    isTrendUp: boolean
    description: string
}

const useStyles = createStyles((theme) => ({
    heading1: {
        color: theme.colors[theme.primaryColor][theme.colorScheme === 'dark' ? 2 : 4]
    }
}));

export default function TrendsCard({ percentage, isTrendUp, description }: TrendsCardProps) {
    const { classes, theme } = useStyles();
    return (
        <Stack>
            <Group position="center">
                <Title className={classes.heading1}>{percentage}%</Title>
                <ActionIcon
                    variant="gradient"
                    p={5}
                    size="lg"
                    gradient={{ from: theme.colors.blue[2], to: theme.colors.blue[7] }}>
                    {isTrendUp
                        ? <IconTrendingUp stroke={3} />
                        : <IconTrendingDown stroke={3} />

                    }
                </ActionIcon>
            </Group>
            <Title align="center" order={5}> {description} </Title>
        </Stack>
    );
}
