import { Card, Text } from '@mantine/core';

interface StatsCardProps {
    height: string
    template: string
    values: Record<string, any>
}

export function StatsCard({ height, template, values }: StatsCardProps) {
    let message = template;
    if (values && Object.keys(values).length > 0) {
        Object.keys(values).forEach(key => {
            if (!values[key]) {
                // eslint-disable-next-line no-param-reassign
                values[key] = '-';
            }
        });
        const field: string = Object.keys(values)[0];
        message = message.replace(`{${field}}`, values[field]);
        const sx = height ? { height } : {};
        return (
            <Card style={{ ...sx, padding: '-0.2rem' }}>
                <Text
                    variant="button"
                    tt="capitalize"
                >
                    <div dangerouslySetInnerHTML={{ __html: message }} />
                </Text>
            </Card>
        );
    }
    return (
        <Card style={{ padding: '1rem' }}>
            ...
        </Card>
    );
}
