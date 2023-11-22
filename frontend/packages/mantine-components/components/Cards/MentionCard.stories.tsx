import { Container, useMantineTheme } from '@mantine/core';
import { StoryFn } from '@storybook/react';
import ET_LOGO from '../../assets/images/et_logo.jpeg';
import YC_LOGO from '../../assets/images/yellow_chapter_logo.jpg';
import YS_LOGO from '../../assets/images/yourstory_logo.svg';
import MentionCard, { MentionCardProps } from './MentionCard';

export default {
    title: 'Component/Mentions',
    component: MentionCard,
    argTypes: {
        backgroundColor: { control: 'color' }
    }
};

const ycLink = 'https://yellowchapter.com/p/lalit-pagaria-co-founder-oraika'
    + '-interview-on-building-a-notification-infrastructure-tool-for-developers';
const etLink = 'https://economictimes.indiatimes.com/news/economy/finance/tone-tag-emerges-winner'
    + '-in-2-categories-of-rbis-first-global-hackathon/articleshow/91969433.cms';
const ysLink = 'https://yourstory.com/2022/06/rbi-results-first-global-hackathon-harbinger-2021-digital-payments';

const Template: StoryFn<MentionCardProps> = (args: MentionCardProps) => {
    const theme = useMantineTheme();
    return (
        <Container size="xs" bg={theme.colors.gray[0]}>
            <MentionCard {...args} />
        </Container>
    );
};

export const YellowChapter = Template.bind({});
YellowChapter.args = {
    logoUrl: YC_LOGO.src,
    logoSize: '80px',
    alt: 'Yellow Chapter',
    title: 'Yellow Chapter',
    link: ycLink
};

export const EconomicsTimes = Template.bind({});
EconomicsTimes.args = {
    logoUrl: ET_LOGO.src,
    logoSize: '80px',
    alt: 'Economics Times',
    title: 'The Economics Times',
    link: etLink
};

export const YourStory = Template.bind({});
YourStory.args = {
    logoUrl: YS_LOGO,
    logoSize: '220px',
    alt: 'YourStory',
    title: 'YourStory',
    link: ysLink
};

export const MentionWithoutTitle = Template.bind({});
MentionWithoutTitle.args = {
    logoUrl: YS_LOGO,
    logoSize: '220px',
    alt: 'YourStory',
    link: ysLink
};

export const MentionWithoutLink = Template.bind({});
MentionWithoutLink.args = {
    logoUrl: YS_LOGO,
    logoSize: '220px',
    alt: 'YourStory',
    title: 'YourStory'
};

export const MentionWithoutTitleLink = Template.bind({});
MentionWithoutTitleLink.args = {
    logoUrl: YS_LOGO,
    logoSize: '220px',
    alt: 'YourStory'
};
