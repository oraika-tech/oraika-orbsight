import { Box, createStyles, Divider, Grid, Image, Stack, Text, ThemeIcon, Timeline, Title } from '@mantine/core';
import { IconDotsVertical } from '@tabler/icons-react';
import { StaticImageData } from 'next/image';

const useStyles = createStyles((theme) => ({
    title: {
        color: theme.colors[theme.primaryColor][theme.colorScheme === 'dark' ? 4 : 6],
        paddingBottom: 50
    },
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

export default function FeatureGridLine({ title, sections }: FeatureLineProps) {
    const { classes } = useStyles();

    const getTextOrImage = (isGetImage: boolean, section: FeatureSection) => {
        let sectionItem;
        if (isGetImage) {
            sectionItem = (
                <center>
                    <Image src={section.image.src} width={250} className={classes.image} />
                </center>
            );
        } else {
            sectionItem = (
                <center>
                    <Stack className={classes.featureText}>
                        <Title align="left" order={2}>{section.heading}</Title>
                        <Text align="left">{section.description}</Text>
                    </Stack>
                </center>
            );
        }
        return sectionItem;
    };

    const sectionItems = sections.map(section => (
        <Grid key={section.heading}>
            <Grid.Col xs={12} sm={6} className={classes.hiddenMobile}>
                {getTextOrImage(section.imageAlign === 'left', section)}
            </Grid.Col>

            <Grid.Col xs={12} sm={6} className={classes.hiddenDesktop}>
                {getTextOrImage(true, section)}
            </Grid.Col>

            <Grid.Col xs={1} className={classes.hiddenMobile}>
                <Timeline
                    className={classes.timeline}
                    color="lime"
                    active={1}
                    bulletSize={24}
                    lineWidth={2}
                >
                    <Timeline.Item>
                        <Box sx={{ height: '250px' }}> </Box>
                    </Timeline.Item>
                    <Timeline.Item bullet={
                        <ThemeIcon color="lime" radius={50} variant="light">
                            <IconDotsVertical size={16} />
                        </ThemeIcon>
                    }
                    />
                </Timeline>
            </Grid.Col>

            <Grid.Col xs={12} sm={5} className={classes.hiddenMobile}>
                {getTextOrImage(section.imageAlign === 'right', section)}
            </Grid.Col>

            <Grid.Col xs={12} sm={5} className={classes.hiddenDesktop}>
                {getTextOrImage(false, section)}
            </Grid.Col>

            <Grid.Col xs={12} className={classes.hiddenDesktop}>
                <Divider size="sm" />
            </Grid.Col>

        </Grid>
    ));

    return (
        <Stack spacing="lg">
            <Title align="center" className={classes.title}>
                {title}
            </Title>
            {sectionItems}
        </Stack>
    );
}
