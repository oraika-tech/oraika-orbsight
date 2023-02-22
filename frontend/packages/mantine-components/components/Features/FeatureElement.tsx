import { Center, createStyles, Flex, Image, Paper, SimpleGrid, Text, Title } from '@mantine/core';

interface FeatureElementProps {
    imageSrc: any;
    title: string;
    description: string;
}
const useStyles = createStyles((theme) => ({
    title: {
        color: theme.colors[theme.primaryColor][theme.colorScheme === 'dark' ? 2 : 4],
    },
    card: {
        borderWidth: '0px 0px 0px 4px',
        borderTopColor: 'transparent',
        // borderLeftColor: theme.colors.gray[4],
        padding: '5px 0px 5px 30px',

        [`@media (max-width: ${theme.breakpoints.xs}px)`]: {
            borderTopColor: theme.colors.gray[4],
            borderLeftColor: 'transparent'
        }
    },
    banner: {
        justifyContent: 'flex-end',
        paddingRight: '20px',
        [`@media (max-width: ${theme.breakpoints.xs}px)`]: {
            justifyContent: 'center'
        }
    }
}));

export function FeatureElement({ imageSrc, title, description }: FeatureElementProps) {
    const { classes } = useStyles();
    return (
        <SimpleGrid
            cols={2}
            verticalSpacing={0}
            breakpoints={[
                { maxWidth: 'xs', cols: 1 }
            ]}
        >
            <Flex className={classes.banner}>
                <Image width={300} src={imageSrc.src} />
            </Flex>

            <Center>
                <Paper className={classes.card} withBorder>
                    <Title order={5} className={classes.title}>{title}</Title>
                    <Text size="md"> {description} </Text>
                </Paper>
            </Center>
        </SimpleGrid>
    );
}
