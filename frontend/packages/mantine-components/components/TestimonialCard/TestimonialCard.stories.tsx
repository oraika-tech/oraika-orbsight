import { Container, useMantineTheme } from '@mantine/core';
import { StoryFn } from '@storybook/react';
import MY_PIC from '../../assets/images/girish-picture.jpg';
import ORAIKA_LOGO from '../../assets/images/oraika-logo.png';
import PLAY_LOGO from '../../assets/images/play-logo.png';
import TestimonialCard, { TestimonialCardProps } from './TestimonialCard';

export default {
    title: 'Component/Testimonial',
    component: TestimonialCard,
    parameters: {
        layout: 'centered'
    },
    argTypes: {
        backgroundColor: { control: 'color' }
    }
};

const Template: StoryFn<TestimonialCardProps> = (args: TestimonialCardProps) => {
    const theme = useMantineTheme();
    return (
        <Container size="xs" bg={theme.colors.gray[0]}>
            <TestimonialCard {...args} />
        </Container>
    );
};

const reviewTextLong = 'Must say we were interacting with Mr Nilesh on a constant basis to help get our reports and ' +
    'CRM in place and we have always had a positive solution to everything. The most important part that ' +
    'Mr Nilesh and team has helped us with is our customer feedback through reviews on Google. He not only ' +
    'helped filter out the reports but also had a special way to showcase our strengths mentioned collectively ' +
    'and negatives. This helped us not only tackle the negatives but organically increase our overall rating on ' +
    'google. We highly recommend his services all around as there is always a good solution with him.Thank you team';

const reviewTextShort = "Oraika has been crucial in managing our Google reviews. With Oraika, we've not only been " +
    'able to filter out negative feedback but also highlight our strengths and weaknesses. This has resulted in an ' +
    'organic increase in our overall rating and allowed us to maintain a rating of 4.5 or above every month. We ' +
    'highly recommend Oraika for their effective solutions and excellent service. Thank you, team!';

export const RichFrame = Template.bind({});
RichFrame.args = {
    reviewerPictureUrl: MY_PIC.src,
    reviewerName: 'Girish Patel',
    reviewerTitle: 'Software Developer',
    companyName: 'Oraika Tech',
    companyLogoUrl: ORAIKA_LOGO.src,
    rating: 3.4,
    highlightedTexts: ['Nilesh', 'Google'],
    reviewText: reviewTextLong,
    reviewTime: new Date()
};

export const MinimumFrame = Template.bind({});
MinimumFrame.args = {
    reviewerName: 'Linda Joseph',
    reviewerTitle: 'Department Head',
    companyName: 'PLaY Arena',
    companyLogoUrl: PLAY_LOGO.src,
    rating: 5,
    highlightedTexts: ['increase in our overall rating', 'highly recommend'],
    reviewText: reviewTextShort
};
