import { createStyles } from '@mantine/core';

export default createStyles((theme) => ({
    card: {
        width: '100%'
    },
    picImage: {
        border: '2px solid orange',
        background: 'linear-gradient(to right, red, purple);'
    },
    highlight: {
        [`@media (max-width: ${theme.breakpoints.sm}px)`]: {
            textAlign: 'left'
        },
    }
}));
