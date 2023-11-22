import { Group, Paper, Stack, Text } from '@mantine/core';
import {
    Icon,
    IconArrowDownRight,
    IconArrowUpRight,
    IconCoin,
    IconDiscount2,
    IconReceipt2,
    IconUserPlus
} from '@tabler/icons-react';
import classes from './index.module.css';

const icons: Record<string, Icon> = {
    user: IconUserPlus,
    discount: IconDiscount2,
    receipt: IconReceipt2,
    coin: IconCoin
};

interface IntroCardProps {
    title: string;
    icon: keyof typeof icons;
    value: string;
    diff: number
}

export function IntroCardGrid({ title, icon, value, diff }: IntroCardProps) {
    const CardIcon = icons[icon];
    const DiffIcon = diff > 0 ? IconArrowUpRight : IconArrowDownRight;

    return (
        <Paper withBorder p="md" radius="md" key={title}>
            <Group justify="space-between">
                <Stack>
                    <Text size="xs" className={classes.title}>
                        {title}
                    </Text>
                    <Group align="flex-end" gap="xs" mt={25}>
                        <Text className={classes.value}>{value}</Text>
                        <Text c={diff > 0 ? 'teal' : 'red'} fz="sm" fw={500} className={classes.diff}>
                            <span>{diff}%</span>
                            <DiffIcon size="1rem" stroke={1.5} />
                        </Text>
                    </Group>
                </Stack>
                <CardIcon className={classes.icon} size="3rem" stroke={2.5} />
            </Group>

        </Paper>
    );
}
