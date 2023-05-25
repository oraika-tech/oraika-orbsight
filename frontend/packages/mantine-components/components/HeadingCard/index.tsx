import { Card } from '@mantine/core';
import React from 'react';

interface HeadingCardProps {
    children: React.ReactNode
}

function HeadingCard(props: HeadingCardProps) {
    return (
        <Card sx={{ height: '100%' }}>
            <h1>{props.children}</h1>
        </Card>
    );
}

export default HeadingCard;
