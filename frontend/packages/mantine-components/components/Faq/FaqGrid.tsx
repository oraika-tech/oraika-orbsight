import {
    Container,
    createStyles,
    Divider,
    SimpleGrid,
    Stack,
    Text,
    Title,
    useMantineTheme
} from '@mantine/core';

interface FeatureProps {
    title: React.ReactNode;
    description: React.ReactNode;
}

export function Feature({ title, description }: FeatureProps) {
    const theme = useMantineTheme();
    return (
        <Stack spacing={5}>
            <Divider />
            <Text style={{ marginTop: theme.spacing.sm, marginBottom: 7 }}>{title}</Text>
            <Text size="sm" color="dimmed" style={{ lineHeight: 1.6 }}>
                {description}
            </Text>
        </Stack>
    );
}

const useStyles = createStyles((theme) => ({
    wrapper: {
        paddingTop: 10,
        paddingBottom: 10
    },

    title: {
        marginBottom: theme.spacing.md,
        textAlign: 'center',

        [theme.fn.smallerThan('sm')]: {
            fontSize: 28,
            textAlign: 'left'
        }
    },

    description: {
        textAlign: 'center',

        [theme.fn.smallerThan('sm')]: {
            textAlign: 'left'
        }
    }
}));

interface FeaturesGridProps {
    title: React.ReactNode;
    description: React.ReactNode;
    questions: FeatureProps[];
}

export function FaqGrid({ title, description, questions }: FeaturesGridProps) {
    const { classes, theme } = useStyles();
    const features = questions.map((feature, index) => <Feature {...feature} key={index} />);

    return (
        <Container className={classes.wrapper}>
            <Title order={2} className={classes.title}>{title}</Title>

            <Text size="md" className={classes.description}>
                {description}
            </Text>

            <SimpleGrid
                mt={20}
                cols={3}
                spacing={theme.spacing.md * 2}
                breakpoints={[
                    { maxWidth: 980, cols: 2, spacing: 'xl' },
                    { maxWidth: 755, cols: 1, spacing: 'xl' }
                ]}
            >
                {features}
            </SimpleGrid>
        </Container>
    );
}
