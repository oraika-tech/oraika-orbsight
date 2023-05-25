import { Popover, Text } from '@mantine/core';
import { useState } from 'react';

interface TypographyWrapProps {
    length: number
    children: React.ReactNode
}

export default function TypographyWrap(props: TypographyWrapProps) {
    const isOverflow = props.length > 90;
    const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);
    const handlePopoverOpen = (event: React.MouseEvent<HTMLElement>) => {
        if (isOverflow) {
            setAnchorEl(event.currentTarget);
        }
    };

    const handlePopoverClose = () => {
        if (isOverflow) {
            setAnchorEl(null);
        }
    };

    const open = Boolean(anchorEl);

    return (
        <Popover opened={open} width={500}>
            <Popover.Target>
                <Text
                    aria-owns={open ? 'mouse-over-popover' : undefined}
                    aria-haspopup="true"
                    onMouseEnter={handlePopoverOpen}
                    onMouseLeave={handlePopoverClose}
                    variant="body2"
                    lineClamp={1}
                >
                    {props.children}
                </Text>
            </Popover.Target>
            <Popover.Dropdown sx={{ pointerEvents: 'none' }}>
                <Text color="dark" variant="body2">
                    {props.children}
                </Text>
            </Popover.Dropdown>
        </Popover>
    );
}
