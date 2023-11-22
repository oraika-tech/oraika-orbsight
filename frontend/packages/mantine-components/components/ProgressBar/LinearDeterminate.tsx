import { Box, Progress } from '@mantine/core';
import { useEffect, useState } from 'react';

interface LinearDeterminateProps {
    period: number
}

export default function LinearDeterminate({ period }: LinearDeterminateProps) {
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        const interval = 1; // sec
        const chunkProgress = (interval * 100) / period;

        const timer = setInterval(() => {
            setProgress((oldProgress) => {
                if (oldProgress === 100) {
                    return 0;
                }
                return Math.floor(Math.min(oldProgress + chunkProgress, 100));
            });
        }, interval * 1000);

        return () => {
            clearInterval(timer);
        };
    }, []);

    return (
        <Box style={{ width: '100%' }}>
            <Progress variant="determinate" value={progress} />
        </Box>
    );
}
