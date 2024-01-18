import { Card, Title } from '@mantine/core';

interface HeadingProps {
    title: string
    sx?: object
}

export function Heading({ title, sx }: HeadingProps) {
    const style = sx || {};
    return (
        <Card style={{ height: '3.5rem', borderRadius: '0.5rem', paddingLeft: '1rem', justifyContent: 'center' }}>
            <Title order={1} style={{ ...style, alignContent: 'center' }}>{title}</Title>
        </Card>
    );
}

Heading.defaultProps = {
    sx: {}
};
