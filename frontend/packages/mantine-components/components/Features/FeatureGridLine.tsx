import { Box, Divider, Grid, Image, Stack, Text, ThemeIcon, Timeline, Title } from '@mantine/core';
import { IconDotsVertical } from '@tabler/icons-react';
import { StaticImageData } from 'next/image';
import classes from './FeatureGridLine.module.css';

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
    const getTextOrImage = (isGetImage: boolean, section: FeatureSection) => {
        let sectionItem;
        if (isGetImage) {
            sectionItem = (
                <center>
                    <Image src={section.image.src} w={250} className={classes.image} />
                </center>
            );
        } else {
            sectionItem = (
                <center>
                    <Stack className={classes.featureText}>
                        <Title ta="left" order={2}>{section.heading}</Title>
                        <Text ta="left">{section.description}</Text>
                    </Stack>
                </center>
            );
        }
        return sectionItem;
    };

    const sectionItems = sections.map(section => (
        <Grid key={section.heading}>
            <Grid.Col span={{ base: 12, sm: 6 }} visibleFrom="sm">
                {getTextOrImage(section.imageAlign === 'left', section)}
            </Grid.Col>

            <Grid.Col span={{ base: 12, sm: 6 }} hiddenFrom="sm">
                {getTextOrImage(true, section)}
            </Grid.Col>

            <Grid.Col span={1} visibleFrom="md">
                <Timeline
                    className={classes.timeline}
                    color="lime"
                    active={1}
                    bulletSize={24}
                    lineWidth={2}
                >
                    <Timeline.Item>
                        <Box style={{ height: '250px' }}> </Box>
                    </Timeline.Item>
                    <Timeline.Item bullet={
                        <ThemeIcon color="lime" radius={50} variant="light">
                            <IconDotsVertical size={16} />
                        </ThemeIcon>
                    }
                    />
                </Timeline>
            </Grid.Col>

            <Grid.Col span={{ base: 12, sm: 5 }} visibleFrom="sm">
                {getTextOrImage(section.imageAlign === 'right', section)}
            </Grid.Col>

            <Grid.Col span={{ base: 12, sm: 5 }} hiddenFrom="sm">
                {getTextOrImage(false, section)}
            </Grid.Col>

            <Grid.Col span={12} hiddenFrom="sm">
                <Divider size="sm" />
            </Grid.Col>

        </Grid>
    ));

    return (
        <Stack gap="lg">
            <Title ta="center" className={classes.title}>
                {title}
            </Title>
            {sectionItems}
        </Stack>
    );
}
