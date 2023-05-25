import { ActionIcon } from '@mantine/core';
import { IconLayoutSidebarLeftCollapse, IconLayoutSidebarLeftExpand } from '@tabler/icons-react';

interface CollapseToggleButtonProps {
    opened: boolean;
    toggle: () => void;
}

export default function CollapseToggleButton({ opened, toggle }: CollapseToggleButtonProps) {
    const buttonIcon = opened
        ? <IconLayoutSidebarLeftCollapse size={20} />
        : <IconLayoutSidebarLeftExpand size={20} />;
    return (
        <ActionIcon onClick={toggle}>
            {buttonIcon}
        </ActionIcon>
    );
}
