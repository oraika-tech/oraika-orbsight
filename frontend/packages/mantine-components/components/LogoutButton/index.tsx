import { ActionIcon } from '@mantine/core';
import { IconLogout } from '@tabler/icons-react';

interface LogoutButtonProps {
    handleLogout: () => void;
}

export default function LogoutButton(props: LogoutButtonProps) {
    return (
        <ActionIcon {...props} onClick={props.handleLogout}>
            <IconLogout fontSize="small" />
        </ActionIcon>
    );
}
