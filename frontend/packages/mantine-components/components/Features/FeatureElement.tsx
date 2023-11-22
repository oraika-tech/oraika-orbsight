import { Center, Flex, Image, Paper, SimpleGrid, Text, Title } from '@mantine/core';
import classes from './FeatureElement.module.css';

interface FeatureElementProps {
    imageSrc: any;
    title: string;
    description: string;
}

export function FeatureElement({ imageSrc, title, description }: FeatureElementProps) {
    return (
        <SimpleGrid
            cols={1}
            verticalSpacing={0}
        >
            <Center>
                <Paper className={classes.card}>
                    <Title order={4} ta="center">{title}</Title>
                    <Text ta="center" size="sm"> {description} </Text>
                </Paper>
            </Center>

            <Center>
                <Flex className={classes.banner}>
                    <Image w={200} src={imageSrc.src} />
                </Flex>
            </Center>
        </SimpleGrid>
    );
}
