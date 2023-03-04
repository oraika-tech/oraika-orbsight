import { createStyles } from '@mantine/core';
import Image, { StaticImageData } from 'next/image';

export interface IconComponentProps {
    height?: number
    src: StaticImageData
    alt: string
}

const useStyles = createStyles((theme) => ({
    imageDiv: {
        width: '100%',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        // border: '1px solid'
    },
    image: {
        layout: 'responsive',
        objectFit: 'contain',
        width: '100%'
    }
}));

export default function IconComponent({ height, src, alt }: IconComponentProps) {
    const { classes } = useStyles();
    // const width = 70;
    // const height = (src.height * width) / src.width;
    return (
        <div className={classes.imageDiv}>
            {/* <Image className={classes.image} width={width} height={height} alt={alt} src={src.src} /> */}
            <Image height={height} className={classes.image} alt={alt} src={src} />
        </div>
    );
}
