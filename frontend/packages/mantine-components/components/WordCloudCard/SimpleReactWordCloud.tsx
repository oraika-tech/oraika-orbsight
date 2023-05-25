import ReactWordcloud, { Optional, Options } from 'react-wordcloud';

interface WordCloudTag {
    term: string
    weight: number
}

interface Props {
    data: Array<WordCloudTag>
}

export default function SimpleReactWordcloud({ data }: Props) {
    const words = data.slice(0, 30).map((word) => ({
        text: word.term,
        value: word.weight
    }));

    const options: Optional<Options> = {
        rotations: 0, // 0 - off, > 0 - division of angle range
        rotationAngles: [-30, -30],
        transitionDuration: 0,
        fontSizes: [24, 96],
        enableTooltip: false,
        padding: 2
    };

    return (
        <ReactWordcloud
            words={words}
            options={options}
        />
    );
}
