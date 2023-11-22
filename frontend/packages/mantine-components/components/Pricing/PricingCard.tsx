import {
    ActionIcon,
    Badge,
    Card,
    Center,
    Group,
    Image,
    List,
    MantineColor,
    Space,
    Stack,
    Text,
    Title
} from '@mantine/core';
import { IconCheck } from '@tabler/icons-react';
import { StaticImageData } from 'next/image';
import classes from './PricingCard.module.css';

interface PricingCardProps {
    icon: StaticImageData
    bgColor?: MantineColor
    title: string
    subtitle: string
    priceTitle: string
    priceSubtitle: string
    featureList: string[]
    showTrialBadge?: boolean
}

export default function PricingCard({ icon, bgColor, title, subtitle, priceTitle,
    priceSubtitle, featureList, showTrialBadge }: PricingCardProps) {
    const featureItems = featureList.map((feature) => <List.Item key={feature}>{feature}</List.Item>);

    return (
        <div className={classes.cardWrapper}>
            <Card className={classes.card} shadow="xl" radius="lg" withBorder bg={bgColor}>
                <Stack gap={8}>
                    <Center>
                        <Image w={90} src={icon.src} alt="" />
                    </Center>
                    <Center>
                        <Title>{title}</Title>
                    </Center>
                    <Center>
                        <Group>
                            <Title order={2}>{priceTitle}</Title>
                            <Title order={6}>{priceSubtitle}</Title>
                        </Group>
                    </Center>
                    <Center>
                        <Text fz="sm">{subtitle}</Text>
                    </Center>
                    <Center>
                        <List
                            spacing="xs"
                            center
                            size="sm"
                            icon={
                                <ActionIcon
                                    className={classes.actionButton}
                                    color="dark"
                                    size={24}
                                    radius="xl"
                                >
                                    <IconCheck size={16} />
                                </ActionIcon>
                            }
                        >
                            {featureItems}
                        </List>
                    </Center>
                    <Space h={20} />
                    {showTrialBadge &&
                        <Center>
                            <Badge className={classes.badge} style={{ padding: 15 }}>
                                <Text className={classes.text} size="sm">
                                    Start with one month free trial
                                </Text>
                            </Badge>
                        </Center>
                    }
                </Stack>
            </Card>
        </div>
    );
}

PricingCard.defaultProps = {
    showTrialBadge: false
};
