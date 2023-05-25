import { Card } from '@mantine/core';
import SimpleReactWordcloud from './SimpleReactWordCloud';

interface WordCloudCardProps {
    data: any[]
}

function WordCloudCard(props: WordCloudCardProps) {
    return (
        <Card sx={{ height: '40vh', backgroundColor: 'lightcyan' }}>
            <SimpleReactWordcloud data={props.data} />
        </Card>
    );
}

export default WordCloudCard;
