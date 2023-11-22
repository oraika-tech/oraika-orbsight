import { Avatar, Group, Text, UnstyledButton, UnstyledButtonProps } from '@mantine/core';
import classes from './UserButton.module.css';

interface UserButtonProps extends UnstyledButtonProps {
    image: string;
    name: string;
    email: string;
    icon?: React.ReactNode;
}

export function UserButton({ image, name, email, icon, ...others }: UserButtonProps) {
    return (
        <UnstyledButton className={classes.user} {...others}>
            <Group gap="xs" wrap="nowrap">
                <Avatar src={image} radius="xl" />

                <div style={{ flex: 1 }}>
                    <Text size="sm" fw={500}>
                        {name}
                    </Text>

                    <Text c="dimmed" size="xs">
                        {email}
                    </Text>
                </div>

                {/* {icon || <IconChevronRight size="0.9rem" stroke={1.5} />} */}
            </Group>
        </UnstyledButton>
    );
}
