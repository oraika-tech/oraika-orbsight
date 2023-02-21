import { Card, Center, createStyles, Divider, Grid, Image, Stack, Text, Title, useMantineTheme } from '@mantine/core';
import { useViewportSize } from '@mantine/hooks';
import { StaticImageData } from 'next/image';

const useStyles = createStyles((theme) => ({
    title: {
        color: theme.colors[theme.primaryColor][theme.colorScheme === 'dark' ? 2 : 4],
        paddingBottom: 50
    },
    // heading3: {
    //     bold
    // },
    flex: {
        width: '100%'
    },
    featureText: {
        paddingLeft: '10px',
        width: '90%'
    },
    image: {
        [`@media (max-width: ${theme.breakpoints.sm}px)`]: {
            maxWidth: '90%'
        },

        [`@media (min-width: ${theme.breakpoints.sm}px)`]: {
            maxWidth: 700
        }
    },
    timeline: {
        [theme.fn.smallerThan('sm')]: {
            display: 'none'
        }
    },
    hiddenMobile: {
        [theme.fn.smallerThan('sm')]: {
            display: 'none'
        }
    },

    hiddenDesktop: {
        [theme.fn.largerThan('sm')]: {
            display: 'none'
        }
    },

    dividerVerticalLine: {
        alignSelf: 'stretch',
        height: 'auto',
        borderLeftWidth: '2px',
        borderLeftColor: '#ced4da',
        borderLeftStyle: 'solid'
    }
}));

export interface FeatureSection {
    heading: string
    description: string
    image: StaticImageData
    imageAlign: string
}

interface FeatureLineProps {
    title: string
    sections: FeatureSection[]
}

export default function FeatureCards({ title, sections }: FeatureLineProps) {
    const { classes } = useStyles();
    const { width } = useViewportSize();
    const theme = useMantineTheme();

    const getImage = (section: FeatureSection, imgWidth?: number) => (
        <Center>
            <Image src={section.image.src} width={imgWidth || 200} className={classes.image} />
        </Center>
    );

    const getText = (section: FeatureSection) => (
        <Center>
            <Stack className={classes.featureText}>
                <Title align="left" order={3}><b>{section.heading}</b></Title>
                <Text align="left">{section.description}</Text>
            </Stack>
        </Center>
    );

    const getImageAndTextVertical = (section: FeatureSection) => (
        <Stack>
            {getImage(section, 250)}
            <Divider size="sm" orientation="vertical" />
            {getText(section)}
        </Stack>
    );

    const getImageAndTextHorizontal = (section: FeatureSection) => (
        <Grid key={section.heading}>
            <Grid.Col xs={6}>
                {getImage(section)}
            </Grid.Col>
            <Grid.Col xs={6} className={classes.dividerVerticalLine}>
                <Center>
                    {getText(section)}
                </Center>
            </Grid.Col>
        </Grid>
    );

    const getTextAndImageHorizontal = (section: FeatureSection) => (
        <Grid key={section.heading}>
            <Grid.Col xs={6}>
                {getText(section)}
            </Grid.Col>
            <Grid.Col xs={6} className={classes.dividerVerticalLine}>
                {getImage(section)}
            </Grid.Col>
        </Grid>
    );

    const sectionItems = width > theme.breakpoints.xs
        ? sections.map(section => (
            <Card key={section.heading} shadow="lg" radius={16} withBorder>
                {section.imageAlign === 'left'
                    ? getImageAndTextHorizontal(section)
                    : getTextAndImageHorizontal(section)
                    // : getImageAndTextHorizontal(section)
                }
            </Card>
        ))
        : sections.map(section => (
            <Card key={section.heading} shadow="lg" radius={16} withBorder>
                {getImageAndTextVertical(section)}
            </Card>
        ));

    return (
        <Stack spacing="lg">
            <Title order={2} align="center" className={classes.title}>
                {title}
            </Title>
            {sectionItems}
        </Stack>
    );
}
