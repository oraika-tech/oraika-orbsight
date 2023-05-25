import { Card, Center, Grid, Loader, Title } from '@mantine/core';
import { getCurrentDate, getCurrentMinusNDays } from 'common-utils/utils';
import EmptyData from 'mantine-components/components/AlertMessage/EmptyData';
import WordCloudCard from 'mantine-components/components/WordCloudCard';
import { useEffect, useState } from 'react';
import { WordCloudRequest, getEmotionWordCloud } from '../../../lib/service/emotion-word-cloud';
import { getUndefForAll } from '../../utils/utils';
import FilterPanel, { FilterPanelData } from '../FilterPanel';

interface TextWordWeight {
    term: string
    weight: number
}

export default function WordCloudAnalysis() {
    const defaultFilterPanelData: FilterPanelData = {
        lang: 'all',
        entity: 'all',
        source: 'all',
        term: 'all',
        startDate: getCurrentMinusNDays(7),
        endDate: getCurrentDate()
    }

    const [isLoading, setLoading] = useState(false);
    const [negativeWords, setNegativeWords] = useState<TextWordWeight[]>();
    const [positiveWords, setPositiveWords] = useState<TextWordWeight[]>();
    const [filterData, setFilterData] = useState<FilterPanelData>(defaultFilterPanelData);

    const syncEmotionWords = (newFilterData) => {
        setLoading(true);
        const filters: WordCloudRequest = {
            start_date: newFilterData.startDate,
            end_date: newFilterData.endDate,
            text_lang: getUndefForAll(newFilterData.lang),
            entity_name: getUndefForAll(newFilterData.entity),
            observer_type: getUndefForAll(newFilterData.source),
            term: getUndefForAll(newFilterData.term)
        };

        getEmotionWordCloud(filters)
            .then(response => {
                for (const keyPhrase of response) {
                    if (keyPhrase.name === 'positive') {
                        setPositiveWords(keyPhrase.word_cloud);
                    } else {
                        setNegativeWords(keyPhrase.word_cloud);
                    }
                }
            })
            .finally(() => {
                setLoading(false);
            });
    };

    useEffect(() => () => {
        setNegativeWords([]);
        setPositiveWords([]);
    }, [filterData]);

    const handleChange = (filterPanelData: FilterPanelData) => {
        setFilterData(filterPanelData);
        syncEmotionWords(filterPanelData);
    };

    const cards = [
        {
            title: 'Positive',
            words: positiveWords,
            chipColor: 'orange'
        },
        {
            title: 'Negative',
            words: negativeWords,
            chipColor: 'red'
        }
    ];

    return (
        <Grid gutter="xs">
            <Grid.Col xs={12}>
                <FilterPanel
                    defaultValue={defaultFilterPanelData}
                    filterHandler={handleChange}
                />
            </Grid.Col>
            {cards.map(card =>
                <Grid.Col key={card.title} xs={12} lg={6}>
                    <Card sx={{ minHeight: '40vh' }}>
                        <Title order={2} sx={{ fontWeight: 800, textAlign: 'center' }}>
                            {card.title} World Cloud
                        </Title>
                        {isLoading
                            ? <Center h={200}><Loader /></Center>
                            : card.words === undefined
                                ? (
                                    <Title order={2} sx={{ fontWeight: 800, paddingTop: '1rem', textAlign: 'center' }}>
                                        Please select filter !
                                    </Title>
                                )
                                : card.words.length
                                    ? <WordCloudCard data={card.words} />
                                    : <EmptyData />
                        }
                    </Card>
                </Grid.Col>
            )}
        </Grid>
    );
}
