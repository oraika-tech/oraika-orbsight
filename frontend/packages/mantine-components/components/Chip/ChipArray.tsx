import { Badge, Group, MantineNumberSize, MantineSize, Stack } from '@mantine/core';

export interface ChipArrayProps {
    chipList: string[];
    bgColor?: string;
    spacing?: MantineNumberSize;
    direction?: 'row' | 'column';
    justify?: 'center' | 'left' | 'right' | 'apart';
    size?: MantineSize;
    sx?: any;
}

export default function ChipArray({ chipList, bgColor, ...props }: ChipArrayProps) {
    const spacing = props.spacing === undefined ? 1 : props.spacing;

    const badgeList = chipList.map((chip: string) => (
        <Badge
            {...props}
            key={chip}
            size={props.size}
            color={bgColor}
            variant="filled"
        >
            {chip}
        </Badge>
    ));

    const justifyMap = {
        center: 'center',
        left: 'flex-start',
        right: 'flex-end',
        apart: 'space-between'
    };

    return props.direction === 'column' ? (
        <Stack
            justify={justifyMap[props.justify || 'left']}
            align="center"
            spacing={spacing}
        >
            {badgeList}
        </Stack>
    ) : (
        <Group
            position={props.justify || 'left'}
            align="center"
            spacing={spacing}
        >
            {badgeList}
        </Group>
    );
}

ChipArray.defaultProps = {
    spacing: 1,
    size: 'sm'
};
