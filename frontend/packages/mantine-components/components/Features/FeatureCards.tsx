import { Card, Center, Divider, Grid, Image, Stack, Text, Title, useMantineTheme } from '@mantine/core';
import { useViewportSize } from '@mantine/hooks';
import { StaticImageData } from 'next/image';
import classes from './FeatureCards.module.css';

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
    const { width } = useViewportSize();
    const theme = useMantineTheme();

    const getImage = (section: FeatureSection, imgWidth?: number) => (
        <Center>
            <Image src={section.image.src} w={imgWidth || 170} className={classes.image} />
        </Center>
    );

    const getText = (section: FeatureSection) => (
        <Center>
            <Stack className={classes.featureText}>
                <Title ta="left" order={3}><b>{section.heading}</b></Title>
                <Text ta="left">{section.description}</Text>
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
            <Grid.Col span={6}>
                {getImage(section)}
            </Grid.Col>
            <Grid.Col span={6} className={classes.dividerVerticalLine}>
                <Center>
                    {getText(section)}
                </Center>
            </Grid.Col>
        </Grid>
    );

    const getTextAndImageHorizontal = (section: FeatureSection) => (
        <Grid key={section.heading}>
            <Grid.Col span={6}>
                {getText(section)}
            </Grid.Col>
            <Grid.Col span={6} className={classes.dividerVerticalLine}>
                {getImage(section)}
            </Grid.Col>
        </Grid>
    );

    const emToPx = (em: string) => parseInt(em, 10) * 16;

    const sectionItems = width > emToPx(theme.breakpoints.xs)
        ? sections.map(section => (
            <Card key={section.heading} shadow="lg" radius={16} withBorder>
                {section.imageAlign === 'left'
                    ? getImageAndTextHorizontal(section)
                    : getTextAndImageHorizontal(section)
                }
            </Card>
        ))
        : sections.map(section => (
            <Card key={section.heading} shadow="lg" radius={16} withBorder>
                {getImageAndTextVertical(section)}
            </Card>
        ));

    return (
        <Stack gap="lg">
            <Title order={2} ta="center" className={classes.title}>
                {title}
            </Title>
            {sectionItems}
        </Stack>
    );
}
