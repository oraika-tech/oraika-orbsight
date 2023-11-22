import { ActionIcon, Group, useMantineColorScheme } from '@mantine/core';
import { IconMoonStars, IconSun } from '@tabler/icons-react';

export function ColorSchemeToggle() {
    const { colorScheme, toggleColorScheme } = useMantineColorScheme();
    const iconColor = colorScheme === 'light' ? 'var(--mantine-color-blue-6)' : 'var(--mantine-color-yellow-4)';
    const iconBgColor = colorScheme === 'light' ? 'var(--mantine-color-gray-0)' : 'var(--mantine-color-dark-6)';
    return (
        <Group justify="center">
            <ActionIcon
                onClick={() => toggleColorScheme()}
                size="xl"
                style={{
                    backgroundColor: iconBgColor,
                    color: iconColor,
                    borderRadius: '5px'
                }}
            >
                {colorScheme === 'dark' ? (
                    <IconMoonStars size={20} stroke={1.5} />
                ) : (
                    <IconSun size={20} stroke={1.5} />
                )}
            </ActionIcon>
        </Group>
    );
}
