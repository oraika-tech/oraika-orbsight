import { Container, Divider, SimpleGrid, Stack, Text, Title, useMantineTheme } from '@mantine/core';
import classes from './FaqGrid.module.css';

interface FeatureProps {
    title: React.ReactNode;
    description: React.ReactNode;
}

export function Feature({ title, description }: FeatureProps) {
    const theme = useMantineTheme();
    return (
        <Stack gap={5}>
            <Divider />
            <Text style={{ marginTop: theme.spacing.sm, marginBottom: 7 }}>{title}</Text>
            <Text size="sm" c="dimmed" style={{ lineHeight: 1.6 }}>
                {description}
            </Text>
        </Stack>
    );
}

interface FeaturesGridProps {
    title: React.ReactNode;
    description: React.ReactNode;
    questions: FeatureProps[];
}

export function FaqGrid({ title, description, questions }: FeaturesGridProps) {
    const features = questions.map((feature, index) => <Feature {...feature} key={index} />);

    return (
        <Container className={classes.wrapper}>
            <Title order={2} className={classes.title}>{title}</Title>

            <Text size="md" className={classes.description}>
                {description}
            </Text>

            <SimpleGrid
                mt={20}
                cols={{ base: 1, sm: 2, md: 3 }}
                spacing="calc(var(--mantine-spacing-md) * 2)"
            >
                {features}
            </SimpleGrid>
        </Container>
    );
}
