import Image, { StaticImageData } from 'next/image';
import classes from './IconComponent.module.css';

export interface IconComponentProps {
    height?: number
    src: StaticImageData
    alt: string
}

export default function IconComponent({ height, src, alt }: IconComponentProps) {
    // const width = 70;
    // const height = (src.height * width) / src.width;
    return (
        <div className={classes.imageDiv}>
            {/* <Image className={classes.image} width={width} height={height} alt={alt} src={src.src} /> */}
            <Image height={height} className={classes.image} alt={alt} src={src} />
        </div>
    );
}
