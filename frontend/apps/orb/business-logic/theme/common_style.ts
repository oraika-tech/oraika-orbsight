import { createStyles } from '@mantine/core';

const commonStyles = createStyles((theme) => ({
    formFrame: {
        height: 810,
        border: 'none',
        borderRadius: '0.8rem',

        [`@media (min-width: ${theme.breakpoints.xs})`]: {
            width: '510px'
        },

        [`@media (max-width: ${theme.breakpoints.xs})`]: {
            width: '90%'
        }
    }
}));

export default commonStyles;
