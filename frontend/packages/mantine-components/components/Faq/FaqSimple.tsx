import { Accordion, Container, Text, Title } from '@mantine/core';
import classes from './FaqSimple.module.css';
import { Question } from './FaqTypes';

interface FaqSimpleProps {
    title: string;
    description: string;
    questions: Question[];
}

export function FaqSimple({ title, description, questions }: FaqSimpleProps) {
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
            <Title order={2} ta="center" className={classes.title}>
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
