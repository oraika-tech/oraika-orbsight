import { Card, Grid, Loader, MantineColor, Space, Title } from '@mantine/core';
import EmptyData from 'mantine-components/components/AlertMessage/EmptyData';
import ChipArray from 'mantine-components/components/Chip/ChipArray';
import WordCloudCard from 'mantine-components/components/WordCloudCard';

export default function WordCloudAnalysis({ height }) {
    const isLoading = false;

    const words = [
        {
            term: 'Paint Ball',
            weight: 10
        },
        {
            term: 'Peak time',
            weight: 9
        },
        {
            term: 'Weekends',
            weight: 9
        },
        {
            term: 'Rock climb',
            weight: 8
        },
        {
            term: 'Food Court',
            weight: 7
        },
        {
            term: 'Sanjay',
            weight: 7
        },
        {
            term: 'Go-kart',
            weight: 7
        },
        {
            term: 'Bangalore',
            weight: 7
        },
        {
            term: 'Hritik',
            weight: 7
        }
    ];

    const positiveKeywords = [
        // "Brilliant experience",
        // "Enjoyed the game thoroughly",
        'Made us comfortable',
        // "Explained clearly",
        'Extremely had fun',
        // "Wonderful and sporty time spent",
        'Spacious food court',
        // "Good coordination",
        // "Best experience ever",
        'Supportive staff',
        'Friendly service',
        'Outstanding coordination',
        'Remarkable photoshoot'
        // "Good communication",
        // "Staff in trampoline park were really helpful",
        // "Beautiful experience",
        // "Explained the rules and regulations in 4 languages",
        // "Assisted us with everything required",
        // "Wall climbing experience was awesome",
        // "Off road biking experience was great"
    ];

    const negativeKeywords = [
        'Food not that great',
        'Expensive feeling',
        'Occupied weekends',
        'A bit crowded',
        "It's a mess there",
        'Waste of time',
        'Slightly expensive'
    ];

    const getTitle = (titleText: string) => (
        <Title
            order={1}
            sx={{ fontSize: '1.3rem', padding: '1%', fontWeight: 500, textAlign: 'center' }}
        >
            {titleText}
        </Title>
    );

    const keyPhrasesComponent = (title: string, phrases: string[], color: MantineColor) => (
        <Card p={20}>
            {getTitle(title)}
            <Space h={8} />
            <ChipArray
                sx={{
                    fontWeight: 700,
                    fontSize: '0.8rem',
                    flexWrap: 'wrap',
                    minWidth: '12rem',
                    height: '1.4rem'
                }}
                chipList={phrases}
                direction="column"
                spacing="xs"
                size="sm"
                bgColor={color}
            />
        </Card>

    );

    return (
        <Grid gutter="sm" sx={{ minHeight: height }}>
            <Grid.Col xs={12}>
                <Card>
                    <Grid gutter={0}>
                        <Grid.Col xs={12}>
                            {getTitle('Key Entities')}
                        </Grid.Col>
                        <Grid.Col xs={12}>
                            {isLoading
                                ? <Loader />
                                : words || words.length > 0
                                    ? <WordCloudCard height={150} data={words} />
                                    : <EmptyData />
                            }
                        </Grid.Col>
                    </Grid>
                </Card>
            </Grid.Col>

            <Grid.Col xs={12} sm={6} md={12} xl={6}>
                {keyPhrasesComponent('Positive Keyphrases', positiveKeywords, 'green')}
            </Grid.Col>

            <Grid.Col xs={12} sm={6} md={12} xl={6}>
                {keyPhrasesComponent('Negative Keyphrases', negativeKeywords, 'red')}
            </Grid.Col>

        </Grid>
    );
}
