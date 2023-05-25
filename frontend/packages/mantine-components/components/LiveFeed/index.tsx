import { Card, Grid, Title } from '@mantine/core';
import { useEffect, useRef, useState } from 'react';
import FeedCard from './FeedCard';

export interface FeedData {
    rawDataId: number
    eventTime?: Date
    emotion?: string
    entityName: string
    observerType: string
    rawText: string
    textLang?: string
    authorName?: string
    categories: string[]
    taxonomies: string[]
}

interface LiveFeedProps {
    height?: string
    feeds: FeedData[]
    displayCount: number
}

export default function LiveFeed({ height, feeds, displayCount }: LiveFeedProps) {
    const totalFeedSize = 30; // not able to take it from feeds.length
    const containerRef = useRef(null);
    const [feedIndex, setFeedIndex] = useState(0);

    const cycleSelectArray = (list: any[], size: number, index: number) => {
        const newIndex = (index >= list.length) ? 0 : index;
        const newList = list.slice(newIndex, newIndex + size);
        const remainingSize = size - newList.length;
        if (remainingSize > 0) {
            return newList.concat(list.slice(0, remainingSize));
        }
        return newList;
    };

    const doSlide = () => {
        setFeedIndex((index) => (index + 1) >= totalFeedSize ? 0 : index + 1);
    };

    useEffect(() => {
        setInterval(doSlide, 10000);
    }, []);

    const style = height ? { height } : {};

    return (
        <Card padding='lg' sx={{ ...style, overflow: 'scroll' }} ref={containerRef}>
            <Grid sx={{ justifyContent: 'stretch' }}>
                <Grid.Col xs={12}>
                    <Title order={4} sx={{ height: '3rem', padding: '1rem' }}>Recent Review</Title>
                </Grid.Col>
                {cycleSelectArray(feeds, displayCount, feedIndex).map(feed => (
                    <Grid.Col key={feed.rawDataId} sx={{ padding: '0.5rem' }}>
                        <FeedCard {...feed} />
                    </Grid.Col>
                ))}
            </Grid>
        </Card>
    );
}

LiveFeed.defaultProps = {
    height: null
};
