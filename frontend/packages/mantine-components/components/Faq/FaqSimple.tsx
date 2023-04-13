import { Accordion, Container, createStyles, Text, Title } from '@mantine/core';
import { Question } from './FaqTypes';

const useStyles = createStyles((theme) => ({
    wrapper: {
        paddingTop: 10,
        paddingBottom: 10,
        minHeight: 50
    },

    title: {
        marginBottom: `calc(${theme.spacing.xl} * 1.5)`
    },

    description: {
        textAlign: 'center',

        [`@media (max-width: ${theme.breakpoints.xs})`]: {
            textAlign: 'left',
            fontSize: theme.fontSizes.md
        }
    },

    item: {
        borderRadius: theme.radius.md,
        marginBottom: theme.spacing.lg,

        border: `1px solid ${theme.colorScheme === 'dark' ? theme.colors.dark[4] : theme.colors.gray[3]
            }`
    }
}));

interface FaqSimpleProps {
    title: string;
    description: string;
    questions: Question[];
}

export function FaqSimple({ title, description, questions }: FaqSimpleProps) {
    const { classes } = useStyles();

    const questionsComponent = questions.map((question) => (
        <Accordion.Item
            className={classes.item}
            key={question.index}
            value={question.index.toString()}
        >
            <Accordion.Control> {question.title} </Accordion.Control>
            <Accordion.Panel> {question.description} </Accordion.Panel>
        </Accordion.Item>
    ));

    return (
        <Container size="sm" className={classes.wrapper}>
            <Title align="center" className={classes.title}>
                {title}
            </Title>
            <Text size="lg" color="dimmed" className={classes.description}>
                {description}
            </Text>

            <Accordion variant="separated" defaultValue="1">
                {' '}
                {questionsComponent}{' '}
            </Accordion>
        </Container>
    );
}
