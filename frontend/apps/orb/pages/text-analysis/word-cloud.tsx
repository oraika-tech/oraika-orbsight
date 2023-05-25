import DefaultLayout from '../../business-logic/layout/DefaultLayout';
import WordCloudAnalysis from '../../business-logic/text-analysis/word-cloud';

export default function WordCloudPage() {
    return (
        <DefaultLayout>
            <WordCloudAnalysis />
        </DefaultLayout>
    );
}
