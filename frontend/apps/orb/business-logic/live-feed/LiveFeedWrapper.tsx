import LiveFeed, { FeedData } from 'mantine-components/components/LiveFeed';
import { useEffect, useState } from 'react';
import { getTextAnalysisData } from '../../lib/service/text-analysis-data';

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

interface LiveFeedWrapperProps {
    isTitle?: boolean
    height: number | string
}

export default function LiveFeedWrapper({ isTitle, height }: LiveFeedWrapperProps) {
    const [feeds, setFeeds] = useState<FeedData[]>([]);

    useEffect(() => {
        const syncFeeds = () => getTextAnalysisData()
            .then(response => setFeeds(response.map(convertFeedData)));

        const timerId = setInterval(syncFeeds, 300000);

        syncFeeds();

        return () => {
            clearInterval(timerId);
            setFeeds([]);
        };
    }, []);

    return <LiveFeed isTitle={isTitle} height={height} displayCount={1} feeds={feeds} />;
}

LiveFeedWrapper.defaultProps = {
    isTitle: true
}
