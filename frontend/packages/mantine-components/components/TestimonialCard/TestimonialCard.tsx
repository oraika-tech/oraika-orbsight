import {
    Avatar,
    Blockquote,
    Card,
    Grid,
    Highlight,
    Image,
    Rating,
    Space,
    Stack,
    Text,
    Title
} from '@mantine/core';
import { useMediaQuery } from '@mantine/hooks';
import { ReactNode } from 'react';
import useStyles from './TestimonialCard.styles';

export interface TestimonialCardProps {
    reviewerPictureUrl?: string
    reviewerName: string
    reviewerTitle: string
    companyName: string
    companyLogoUrl: string
    rating?: number
    highlightedTexts: string[]
    reviewText: string
    reviewTime?: Date
    reviewSourceIcon?: ReactNode
}

export default function TestimonialCard({
    reviewerName,
    reviewerPictureUrl,
    reviewerTitle,
    companyName,
    companyLogoUrl,
    rating,

    highlightedTexts,
    reviewText,
    reviewTime,
    reviewSourceIcon }: TestimonialCardProps) {
    const mobileScreen = useMediaQuery('(max-width: 350px)');
    const { classes, theme } = useStyles();
    return (
        <Card shadow="xl" p="lg" radius={15} className={classes.card}>
            <Grid>
                {rating &&
                    <Grid.Col xs={3}>
                        <Rating value={rating} size="md" fractions={5} readOnly />
                    </Grid.Col>
                }
                <Grid.Col>
                    <Blockquote cite={reviewTime && reviewTime.toDateString()}>
                        <Highlight align={mobileScreen ? 'left' : 'justify'} highlight={highlightedTexts}>
                            {reviewText}
                        </Highlight>
                    </Blockquote>
                </Grid.Col>
                {reviewSourceIcon &&
                    <Grid.Col>
                        {reviewSourceIcon}
                    </Grid.Col>
                }

                {reviewerPictureUrl
                    ? (
                        <Grid.Col xs={1.7}>
                            <Avatar
                                className={classes.picImage}
                                radius="xl"
                                size="lg"
                                alt=""
                                src={reviewerPictureUrl}
                            />
                        </Grid.Col>
                    ) : (
                        <Grid.Col xs={1.5}>
                            <Avatar
                                className={classes.picImage}
                                variant="filled"
                                bg={theme.colorScheme === 'dark' ? theme.colors.gray[3] : theme.colors.gray[1]}
                                size="lg"
                                radius={40}
                                p="0.4rem"
                                src={companyLogoUrl}
                            />
                            {/* <Image width={50} height={20} src={companyLogoUrl} /> */}
                        </Grid.Col>
                    )
                }
                <Grid.Col xs={7}>
                    <Stack spacing={0} h="100%" justify="center" align="flex-start">
                        <Title order={5}>
                            {reviewerName}
                        </Title>
                        <Text>
                            {reviewerTitle} at {companyName}
                        </Text>
                    </Stack>
                </Grid.Col>
                <Grid.Col xs={1.7}>
                    <Space />
                </Grid.Col>
                {reviewerPictureUrl &&
                    <Grid.Col xs={1}>
                        <Image width={50} height={50} src={companyLogoUrl} />
                    </Grid.Col>
                }

            </Grid>
        </Card>
    );
}
