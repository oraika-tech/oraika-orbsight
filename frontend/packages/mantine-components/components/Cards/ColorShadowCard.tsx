import { ReactNode } from 'react';

import classes from './ColorShadowCard.module.css';

interface ColorShadowCardProps {
    children: ReactNode
}

export default function ColorShadowCard({ children }: ColorShadowCardProps) {
    return (
        <div className={classes.shadowCard}>
            {children}
        </div>
    );
}
