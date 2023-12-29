import { Button, Group } from '@mantine/core';
import { IconCheck, IconX } from '@tabler/icons-react';

interface ConfirmPanelProps {
    onConfirm: () => void;
    onCancel: () => void;
}

export default function ConfirmPanel({ onConfirm, onCancel }: ConfirmPanelProps) {
    return (
        <Group gap={5}>
            <Button
                size="xs"
                variant="filled"
                onClick={onConfirm}
                pb={0}
                pt={0}
                pl={10}
                pr={10}
            >
                <IconCheck size={15} />
            </Button>
            <Button
                size="xs"
                variant="outline"
                onClick={onCancel}
                pb={0}
                pt={0}
                pl={10}
                pr={10}
            >
                <IconX size={15} />
            </Button>
        </Group>
    );
}
