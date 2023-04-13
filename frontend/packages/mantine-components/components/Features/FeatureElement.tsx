import { Center, createStyles, Flex, Image, Paper, SimpleGrid, Text, Title } from '@mantine/core';
import { getSecondaryFontShade } from '../../../../apps/home/business-logic/theme/theme';

interface FeatureElementProps {
    imageSrc: any;
    title: string;
    description: string;
}
const useStyles = createStyles((theme) => ({
    title: {
        color: getSecondaryFontShade(theme)
    },
    card: {
        borderWidth: '0px 0px 0px 0px',
        borderTopColor: 'transparent',
        // borderLeftColor: theme.colors.gray[4],
        padding: '5px 0px 5px 30px',

        [`@media (max-width: ${theme.breakpoints.xs})`]: {
            borderTopColor: theme.colors.gray[4],
            borderLeftColor: 'transparent'
        }
    },
    banner: {
        justifyContent: 'flex-end',
        paddingRight: '20px',
        [`@media (max-width: ${theme.breakpoints.xs})`]: {
            justifyContent: 'center'
        }
    }
}));

export function FeatureElement({ imageSrc, title, description }: FeatureElementProps) {
    const { classes } = useStyles();
    return (
        <SimpleGrid
            cols={1}
            verticalSpacing={0}
            breakpoints={[
                { maxWidth: 'sm', cols: 1 }
            ]}
        >
            <Center>
                <Paper className={classes.card}>
                    <Title order={4} align="center" className={classes.title}>{title}</Title>
                    <Text align="center" size="sm"> {description} </Text>
                </Paper>
            </Center>

            <Center>
                <Flex className={classes.banner}>
                    <Image width={200} src={imageSrc.src} />
                </Flex>
            </Center>
        </SimpleGrid>
    );
}
