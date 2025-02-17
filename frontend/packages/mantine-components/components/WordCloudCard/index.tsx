import { Card } from '@mantine/core';
import SimpleReactWordcloud from './SimpleReactWordCloud';

interface WordCloudCardProps {
    height?: string | number;
    bgColor?: string;
    data: any[]
}

interface WordCloudStyle {
    height?: number | string
    backgroundColor?: string
}

function WordCloudCard(props: WordCloudCardProps) {
    const style: WordCloudStyle = {};
    if (props.height) {
        style.height = props.height;
    }
    if (props.bgColor) {
        style.backgroundColor = props.bgColor;
    }
    return (
        <Card m={10} style={{ ...style }}>
            <SimpleReactWordcloud data={props.data} />
        </Card>
    );
}

export default WordCloudCard;
