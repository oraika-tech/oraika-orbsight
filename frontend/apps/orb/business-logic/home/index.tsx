import { Grid, createStyles } from '@mantine/core';
import { IconBuildingBank, IconCategory, IconCircleDot, IconMessage } from '@tabler/icons-react';

import LiveFeed, { FeedData } from 'mantine-components/components/LiveFeed';
import { MiniStatisticsCard } from 'mantine-components/components/StatsCard/MiniStatisticsCard';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import { getStats } from '../../lib/service/stats-service';
import { getTextAnalysisData } from '../../lib/service/text-analysis-data';

interface Stats {
    active: number
    total: number
}

interface StatsResponseElement {
    name: string
    value: number
}

interface TextAnalysisData {
    raw_data_id: number
    event_time?: Date
    emotion?: string
    entity_name: string
    observer_type: string
    raw_text: string
    text_lang?: string
    author_name?: string
    categories: string[]
    taxonomies: string[]
}

const convertFeedData = (textAnalysisData: TextAnalysisData) => ({
    rawDataId: textAnalysisData.raw_data_id,
    eventTime: new Date(textAnalysisData.event_time),
    emotion: textAnalysisData.emotion,
    entityName: textAnalysisData.entity_name,
    observerType: textAnalysisData.observer_type,
    text: textAnalysisData.raw_text,
    textLang: textAnalysisData.text_lang,
    authorName: textAnalysisData.author_name,
    categories: textAnalysisData.categories,
    taxonomies: textAnalysisData.taxonomies
});

const initialStats: () => Stats = () => ({ active: -1, total: -1 });

const convertStats = (responseElements: StatsResponseElement[]) => {
    const stats: Stats = initialStats();
    for (const element of responseElements) {
        switch (element.name) {
            case 'Tracked':
                stats.active = element.value;
                break;
            case 'Total':
                stats.total = element.value;
                break;
        }
    }
    return stats;
};

const getConsistentValue = (value: number) => value >= 0 ? value : '-';

const useStyles = createStyles(() => ({
    link: {
        textDecoration: 'none'
    }
}));

export default function Home() {
    const { classes } = useStyles();
    const [feeds, setFeeds] = useState<FeedData[]>([]);

    const [entityStats, setEntityStats] = useState<Stats>(initialStats());
    const [observerStats, setObserverStats] = useState<Stats>(initialStats());
    const [taxonomyStats, setTaxonomyStats] = useState<Stats>(initialStats());
    const [categoriesStats, setCategoriesStats] = useState<Stats>(initialStats());

    useEffect(() => {
        const syncFeeds = () => getTextAnalysisData()
            .then(response => setFeeds(response.map(convertFeedData)))
            .catch(() => { }); // eat 401

        const syncStats = (url, setMethod) => getStats(url)
            .then((response: StatsResponseElement[]) => setMethod(convertStats(response)))
            .catch(err => console.log(err));

        const timerId = setInterval(syncFeeds, 300000);

        syncFeeds();
        syncStats('/entities', setEntityStats);
        syncStats('/observers', setObserverStats);
        syncStats('/taxonomies', setTaxonomyStats);
        syncStats('/categories', setCategoriesStats);

        return () => {
            clearInterval(timerId);
            setFeeds([]);
        };
    }, []);

    return (
        <Grid gutter="sm">
            <Grid.Col xs={12} sm={9}>
                <LiveFeed displayCount={3} feeds={feeds} />
            </Grid.Col>
            <Grid.Col xs={12} sm={3}>
                <Grid gutter="xs">
                    <Grid.Col xs={12}>
                        <Link key="entity" className={classes.link} href="/manage/entity">
                            <MiniStatisticsCard
                                title={{ text: 'Entities' }}
                                count={getConsistentValue(entityStats.active)}
                                countColor="success"
                                percentage={{ color: ['dark'], text: `/ ${getConsistentValue(entityStats.total)}` }}
                                icon={IconBuildingBank}
                            />
                        </Link>
                    </Grid.Col>
                    <Grid.Col xs={12}>
                        <Link key="data-source" className={classes.link} href="/manage/data-source">
                            <MiniStatisticsCard
                                title={{ text: 'Data Sources' }}
                                count={getConsistentValue(observerStats.active)}
                                countColor="success"
                                percentage={{ color: ['dark'], text: `/ ${getConsistentValue(observerStats.total)}` }}
                                icon={IconMessage}
                            />
                        </Link>
                    </Grid.Col>
                    <Grid.Col xs={12}>
                        <Link key="taxonomy" className={classes.link} href="/manage/taxonomy">
                            <MiniStatisticsCard
                                title={{ text: 'Taxonomies' }}
                                count={getConsistentValue(taxonomyStats.active)}
                                countColor="success"
                                percentage={{ color: ['dark'], text: `/ ${getConsistentValue(taxonomyStats.total)}` }}
                                icon={IconCircleDot}
                            />
                        </Link>
                    </Grid.Col>
                    <Grid.Col xs={12}>
                        <Link key="taxonomy" className={classes.link} href="/manage/taxonomy">
                            <MiniStatisticsCard
                                title={{ text: 'Categories' }}
                                count={getConsistentValue(categoriesStats.active)}
                                countColor="success"
                                percentage={{ color: ['dark'], text: `/ ${getConsistentValue(categoriesStats.total)}` }}
                                icon={IconCategory}
                            />
                        </Link>
                    </Grid.Col>
                </Grid>
            </Grid.Col>
        </Grid>
    );
}
