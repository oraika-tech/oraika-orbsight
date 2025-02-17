import { Badge, Group, MantineSize, MantineSpacing, Stack } from '@mantine/core';

export interface ChipArrayProps {
    chipList: string[];
    bgColor?: string;
    spacing?: MantineSpacing;
    direction?: 'row' | 'column';
    justify?: 'center' | 'left' | 'right' | 'apart';
    size?: MantineSize;
    sx?: any;
}

export default function ChipArray({ chipList, bgColor, ...props }: ChipArrayProps) {
    const spacing = props.spacing === undefined ? 1 : props.spacing;
    chipList = chipList || [];

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
            gap={spacing}
        >
            {badgeList}
        </Stack>
    ) : (
        <Group
            justify={props.justify || 'left'}
            align="center"
            gap={spacing}
        >
            {badgeList}
        </Group>
    );
}

ChipArray.defaultProps = {
    spacing: 1,
    size: 'sm'
};
