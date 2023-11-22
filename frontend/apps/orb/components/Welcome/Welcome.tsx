import { Anchor, Text, Title } from '@mantine/core';
import classes from './Welcome.module.css';

export function Welcome() {
    return (
        <>
            <Title className={classes.title} ta="center" mt={100}>
                Welcome to{' '}
                <Text inherit variant="gradient" component="span">
                    TechEase
                </Text>
            </Title>
            <Text c="dimmed" ta="center" size="lg" style={{ maxWidth: 580 }} mx="auto" mt="xl">
                This starter Next.js project includes a minimal setup for server side rendering, if
                you want to learn more on Mantine + Next.js integration follow{' '}
                <Anchor href="https://mantine.dev/guides/next/" size="lg">
                    this guide
                </Anchor>
                . To get started edit index.tsx file.
            </Text>
        </>
    );
}
