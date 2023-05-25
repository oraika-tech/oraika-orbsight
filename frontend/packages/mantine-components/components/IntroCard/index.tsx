import { Group, Paper, Stack, Text, createStyles, rem } from '@mantine/core';
import {
    Icon,
    IconArrowDownRight,
    IconArrowUpRight,
    IconCoin,
    IconDiscount2,
    IconReceipt2,
    IconUserPlus
} from '@tabler/icons-react';

const useStyles = createStyles((theme) => ({
    root: {
        padding: `calc(${theme.spacing.xl} * 1.5)`
    },

    value: {
        fontSize: rem(24),
        fontWeight: 700,
        lineHeight: 1
    },

    diff: {
        lineHeight: 1,
        display: 'flex',
        alignItems: 'center'
    },

    icon: {
        color: theme.colorScheme === 'dark' ? theme.colors.dark[3] : theme.colors.gray[4]
    },

    title: {
        fontWeight: 700,
        textTransform: 'uppercase'
    }
}));

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
    const { classes } = useStyles();
    const Icon = icons[icon];
    const DiffIcon = diff > 0 ? IconArrowUpRight : IconArrowDownRight;

    return (
        <Paper withBorder p="md" radius="md" key={title}>
            <Group position="apart">
                <Stack>
                    <Text size="xs" className={classes.title}>
                        {title}
                    </Text>
                    <Group align="flex-end" spacing="xs" mt={25}>
                        <Text className={classes.value}>{value}</Text>
                        <Text color={diff > 0 ? 'teal' : 'red'} fz="sm" fw={500} className={classes.diff}>
                            <span>{diff}%</span>
                            <DiffIcon size="1rem" stroke={1.5} />
                        </Text>
                    </Group>
                </Stack>
                <Icon className={classes.icon} size="3rem" stroke={2.5} />
            </Group>

        </Paper>
    );
}
