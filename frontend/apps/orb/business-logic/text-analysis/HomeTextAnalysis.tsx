import { Card, Grid, Loader, Title } from '@mantine/core';
import EmptyData from 'mantine-components/components/AlertMessage/EmptyData';
import ChipColumn from 'mantine-components/components/Text/ChipColumn';
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

    return (
        <Grid gutter={1} sx={{ minHeight: height }}>
            <Grid.Col xs={12}>
                <Card>
                    <Grid gutter={0}>
                        <Grid.Col xs={12}>
                            <Title
                                order={1}
                                sx={{ fontSize: '1.3rem', padding: '1%', fontWeight: 500, textAlign: 'center' }}
                            >
                                Key Entities
                            </Title>
                        </Grid.Col>
                        <Grid.Col xs={12}>
                            <Card
                                shadow="md"
                                withBorder
                                sx={{
                                    padding: '0.5rem',
                                    margin: '0.1rem 0.5rem 0.5rem 0.5rem',
                                    borderRadius: '1rem',
                                    backgroundColor: 'Lavender'
                                }}
                            >
                                {isLoading
                                    ? <Loader />
                                    : words || words.length > 0
                                        ? <WordCloudCard data={words} />
                                        : <EmptyData />
                                }
                            </Card>
                        </Grid.Col>
                    </Grid>
                </Card>
            </Grid.Col>

            <Grid.Col xs={12} sm={6} md={12} xl={6}>
                <ChipColumn
                    title="Positive Keyphrases"
                    words={positiveKeywords}
                    isLoading={isLoading}
                    bgColor="success"
                />
            </Grid.Col>

            <Grid.Col xs={12} sm={6} md={12} xl={6}>
                <ChipColumn
                    title="Negative Keyphrases"
                    words={negativeKeywords}
                    isLoading={isLoading}
                    bgColor="error"
                />
            </Grid.Col>

        </Grid>
    );
}
