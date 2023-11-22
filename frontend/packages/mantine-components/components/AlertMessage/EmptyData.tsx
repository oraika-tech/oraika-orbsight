import { Space, Stack, Text } from '@mantine/core';
import { IconZoomExclamation } from '@tabler/icons-react';

export default function EmptyData() {
    return (
        <Stack align="center">
            <Space h="1rem" />
            <IconZoomExclamation size={100} stroke={1.5} color="black" />
            <Text size="xl" fw={500} style={{ marginTop: '0.3rem' }}>
                Oops! No data found.
            </Text>
            <Text size="md" c="dimmed" style={{ marginTop: '0.3rem' }}>
                No data matches your current filters - try adjusting them to discover more!
            </Text>
            <Space h="1rem" />
        </Stack>
    );
}
