/* eslint-disable max-len */
import { Card, Center, Grid, Loader, Title } from '@mantine/core';
import { getCurrentDate, getCurrentMinusNDays } from 'common-utils/utils';
import EmptyData from 'mantine-components/components/AlertMessage/EmptyData';
import ChipArray from 'mantine-components/components/Chip/ChipArray';
import { useEffect, useState } from 'react';
import { KeyPhrasesRequest, getEmotionKeyPhrases } from '../../../lib/service/emotion-key-phrases';
import { getUndefForAll } from '../../utils/utils';
import FilterPanel, { FilterPanelData } from '../FilterPanel';

interface KeyPhraseWeight {
    phrase: string
    weight?: number
}

export default function KeyPhrasesAnalysis() {
    const defaultFilterPanelData: FilterPanelData = {
        lang: 'all',
        entity: 'all',
        source: 'all',
        term: 'all',
        startDate: getCurrentMinusNDays(7),
        endDate: getCurrentDate()
    };

    const [isLoading, setLoading] = useState(false);
    const [negativeKeyPhrases, setNegativeKeyPhrases] = useState<string[]>();
    const [positiveKeyPhrases, setPositiveKeyPhrases] = useState<string[]>();
    const [filterData, setFilterData] = useState<FilterPanelData>(defaultFilterPanelData);

    const syncEmotionKeyPhrases = (newFilterData) => {
        const filters: KeyPhrasesRequest = {
            start_date: newFilterData.startDate,
            end_date: newFilterData.endDate,
            text_lang: getUndefForAll(newFilterData.lang),
            entity_name: getUndefForAll(newFilterData.entity),
            observer_type: getUndefForAll(newFilterData.source),
            term: getUndefForAll(newFilterData.term),
            limit: 100 // hardcoded for better performance
        };

        setLoading(true);
        getEmotionKeyPhrases(filters)
            .then(response => {
                for (const keyPhrase of response) {
                    if (keyPhrase.key_phrases.length % 2 === 1) {
                        keyPhrase.key_phrases.pop();
                    }
                    if (keyPhrase.name === 'positive') {
                        setPositiveKeyPhrases(keyPhrase.key_phrases.map((el: KeyPhraseWeight) => el.phrase));
                    } else if (keyPhrase.name === 'negative') {
                        setNegativeKeyPhrases(keyPhrase.key_phrases.map((el: KeyPhraseWeight) => el.phrase));
                    }
                }
            })
            .finally(() => {
                setLoading(false);
            });
    };

    useEffect(() => () => {
        setNegativeKeyPhrases([]);
        setPositiveKeyPhrases([]);
    }, [filterData]);

    const handleChange = (filterPanelData: FilterPanelData) => {
        setFilterData(filterPanelData);
        syncEmotionKeyPhrases(filterPanelData);
    };

    const cards = [
        {
            title: 'Positive',
            keyPhrases: positiveKeyPhrases,
            chipColor: 'green'
        },
        {
            title: 'Negative',
            keyPhrases: negativeKeyPhrases,
            chipColor: 'red'
        }
    ];

    return (
        <Grid gutter="md">
            <Grid.Col span={12}>
                <FilterPanel
                    defaultValue={defaultFilterPanelData}
                    filterHandler={handleChange}
                />
            </Grid.Col>
            {cards.map(card =>
                <Grid.Col span={{ base: 12, lg: 6 }} key={card.title}>
                    <Card style={{ textAlign: 'center', minHeight: '45vh', maxHeight: '65vh', overflow: 'scroll' }}>
                        <Grid style={{ height: '90%' }} gutter="xl">
                            <Grid.Col span={12}>
                                <Title style={{ fontWeight: 800 }} order={2}>{card.title} Key Phrases</Title>
                            </Grid.Col>
                            <Grid.Col span={12} style={{ height: '100%' }}>
                                {isLoading
                                    ? <Center h={200}><Loader /></Center>
                                    : card.keyPhrases === undefined
                                        ? (
                                            <Title
                                                order={3}
                                                style={{
                                                    fontWeight: 800,
                                                    paddingTop: '1rem',
                                                    textAlign: 'center'
                                                }}
                                            >
                                                Please select filter !
                                            </Title>
                                        )
                                        : card.keyPhrases.length
                                            ? (
                                                <Grid style={{ justifyContent: 'left' }} gutter={3}>
                                                    <Grid.Col span={{ base: 12, md: 6 }}>
                                                        <ChipArray
                                                            sx={{
                                                                fontWeight: 700,
                                                                fontSize: '0.8rem',
                                                                flexWrap: 'wrap',
                                                                minWidth: '15rem',
                                                                height: '1.5rem'
                                                            }}
                                                            chipList={card.keyPhrases.slice(0, card.keyPhrases.length / 2)}
                                                            direction="column"
                                                            spacing="xs"
                                                            size="sm"
                                                            bgColor={card.chipColor}
                                                        />
                                                    </Grid.Col>
                                                    <Grid.Col span={{ base: 12, md: 6 }}>
                                                        <ChipArray
                                                            sx={{
                                                                fontWeight: 700,
                                                                fontSize: '0.8rem',
                                                                flexWrap: 'wrap',
                                                                minWidth: '15rem',
                                                                height: '1.5rem'
                                                            }}
                                                            chipList={card.keyPhrases.slice(card.keyPhrases.length / 2)}
                                                            direction="column"
                                                            spacing="xs"
                                                            bgColor={card.chipColor}
                                                        />
                                                    </Grid.Col>
                                                </Grid>
                                            )
                                            : <EmptyData />
                                }
                                <Grid.Col span={6} />
                            </Grid.Col>
                        </Grid>
                    </Card>
                </Grid.Col>
            )
            }
        </Grid>
    );
}
