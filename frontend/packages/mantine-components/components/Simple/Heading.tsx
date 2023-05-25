import { Card, Text } from '@mantine/core';

interface HeadingProps {
    title: string
    sx?: object
}

export function Heading({ title, sx }: HeadingProps) {
    const style = sx || {};
    return (
        <Card sx={{ height: '2.5rem', borderRadius: '0.5rem', paddingLeft: '1rem', justifyContent: 'center' }}>
            <Text sx={{ ...style, alignContent: 'center' }}>{title}</Text>
        </Card>
    );
}

Heading.defaultProps = {
    sx: {}
};
