import { createStyles } from '@mantine/core';
import { ReactNode } from 'react';

const useStyles = createStyles((theme) => ({
    shadowCard: {
        height: '100%',
        width: '100%',
        borderRadius: '5px',
        '&::before': {
            content: '""',
            position: 'absolute',
            height: '12%',
            width: '32%',
            background: 'linear-gradient(90deg, purple, green, hotpink)',
            zIndex: -1,
            filter: 'blur(10px)'
        }
    }
}));

interface ColorShadowCardProps {
    children: ReactNode
}

export default function ColorShadowCard({ children }: ColorShadowCardProps) {
    const { classes } = useStyles();
    return (
        <div className={classes.shadowCard}>
            {children}
        </div>
    );
}
