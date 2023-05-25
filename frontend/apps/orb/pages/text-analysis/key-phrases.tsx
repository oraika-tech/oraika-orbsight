import DefaultLayout from '../../business-logic/layout/DefaultLayout';
import KeyPhrasesAnalysis from '../../business-logic/text-analysis/key-phrases';

export default function KeyPhrasesPage() {
    return (
        <DefaultLayout>
            <KeyPhrasesAnalysis />
        </DefaultLayout>
    );
}
