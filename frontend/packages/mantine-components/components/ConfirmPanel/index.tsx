import { Button, Group } from '@mantine/core';
import { IconCheck, IconX } from '@tabler/icons-react';

interface ConfirmPanelProps {
    onConfirm: () => void;
    onCancel: () => void;
}

export default function ConfirmPanel({ onConfirm, onCancel }: ConfirmPanelProps) {
    return (
        <Group spacing={5}>
            <Button
                size="xs"
                variant="filled"
                onClick={onConfirm}
            >
                <IconCheck size={20} />
            </Button>
            <Button
                size="xs"
                variant="outline"
                onClick={onCancel}
            >
                <IconX size={20} />
            </Button>
        </Group>
    );
}
