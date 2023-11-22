import { Progress } from '@mantine/core';
import { useInterval } from '@mantine/hooks';
import { useRouter } from 'next/router';
import { ReactNode, useEffect, useState } from 'react';

interface WithRouteProps {
    children: ReactNode
}

export default function WithRoute({ children }: WithRouteProps) {
    const [loaded, setLoaded] = useState(false);
    const [progress, setProgress] = useState(0);
    const progressTimer = useInterval(() => {
        setProgress((value) => value + 5);
    }, 50);
    const router = useRouter();
    useEffect(() => {
        progressTimer.start();
        if (router.asPath === '/') {
            setLoaded(true);
        } else {
            router.replace(router.asPath);
        }

        // return progressTimer.stop();
    }, []);

    useEffect(() => {
        if (progress > 100) {
            setLoaded(true);
            progressTimer.stop();
            router.replace('/');
        }
    }, [progress]);

    if (loaded) {
        return <>{children}</>;
    }
    return <><Progress animated value={progress} /></>;
}
