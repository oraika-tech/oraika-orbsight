import { useUpdate } from '@refinedev/core';
import ToggleButton from 'mantine-components/components/ToggleButton';

interface EnableButtonProps {
    resource: string;
    id: string | number;
    enabled: boolean;
}

export default function EnableButton({ resource, id, enabled }: EnableButtonProps) {
    const { mutate } = useUpdate();
    const toggleEnabled = (identifier, isEnabled, handlerDone) => {
        mutate({ resource, id: identifier, values: { is_enabled: isEnabled } });
        handlerDone(true);
    };
    return (
        <ToggleButton
            value={{ id, isEnabled: enabled }}
            handleToggle={toggleEnabled}
        />
    );
}
