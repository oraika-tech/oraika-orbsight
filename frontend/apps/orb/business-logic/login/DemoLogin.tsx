import {
    ActionIcon,
    BackgroundImage,
    Box,
    Card,
    Center,
    Image,
    Loader,
    SimpleGrid,
    Space,
    Text,
    TextInput
} from '@mantine/core';
import {
    IconBallBasketball,
    IconChartHistogram,
    IconCircleArrowRight,
    IconMail,
    IconMoodSmile
} from '@tabler/icons-react';
import image from 'assets/images/demo-login-background.png';
import brand from 'assets/images/oraika-logo.png';
import { EMAIL_FORMAT_ERROR, doDemoLogin, getProfile } from 'common-utils/service/auth-service';
import { emailValidation, getRandomNumber } from 'common-utils/utils';
import AlertMessage from 'mantine-components/components/AlertMessage';
import { UserContext } from 'mantine-components/components/Auth/AuthProvider';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useContext, useEffect, useRef, useState } from 'react';

import classes from './DemoLogin.module.css';

export default function DemoLogin() {
    const router = useRouter();
    const [isLoading, setLoading] = useState<Boolean>(false);
    const [shouldLogin, setShouldLogin] = useState(false);
    const [canSubmit, setCanSubmit] = useState<boolean>(true);
    const errorDuration = 10000;
    const [errorMessage, setErrorMessage] = useState('');
    const formRef = useRef(null);
    const { refreshPage } = useContext(UserContext);

    useEffect(() => {
        const syncUserInfo = () => getProfile()
            .then(user => {
                if (user.preferred_tenant_id) {
                    router.push(process.env.NEXT_PUBLIC_ORB_WEBSITE_URL || '/');
                } else {
                    setShouldLogin(true);
                }
            })
            .catch(() => {
                setShouldLogin(true);
            });

        syncUserInfo();
    }, []);

    if (!shouldLogin) {
        return <Center> <Loader variant="dots" /> </Center>;
    }

    const handleTextChange: React.ChangeEventHandler<HTMLInputElement> = (event) => {
        setCanSubmit(emailValidation(event.target.value));
    };

    const tryLogin = (event) => {
        event.preventDefault();
        let email;
        for (const el of event.target) {
            if (el.name === 'email') {
                email = el.value;
            }
        }
        if (!email) {
            email = `guest_${getRandomNumber(4)}@oraika.com`;
        }
        setLoading(true);
        doDemoLogin(email)
            .then(
                loginResponse => {
                    if (loginResponse) {
                        router.push('/');
                        refreshPage();
                    } else {
                        // eslint-disable-next-line no-console
                        console.log('Login Failed');
                        setErrorMessage('Login Failed, Please try again !');
                    }
                },
                error => {
                    if (error.message === EMAIL_FORMAT_ERROR) {
                        setErrorMessage('');
                        setErrorMessage('Please type a valid email!');
                    } else {
                        setErrorMessage('');
                        // eslint-disable-next-line no-console
                        console.log('Authentication failed: ', error);
                        setErrorMessage('Login Failed, Please try again !');
                    }
                }
            )
            .finally(() => {
                setLoading(false);
            });
    };

    let message = '';
    if (errorMessage) {
        message = errorMessage || 'Login Failed, Please try again !';
    }

    return (
        <BackgroundImage src={image.src} h="110vh">
            <Box mb={1} p={20} display="flex" bg="#FFFFFF">
                <Link href="https://oraika.com">
                    <Image
                        src={brand.src}
                        alt="Oraika"
                        w="11rem"
                        // bgcolor="#FFFFFF"
                        radius={10}
                        p={2}
                    />
                </Link>
            </Box>
            <Center mb={1} ml={0.5} p="0rem" pt="6vh" display="flex">
                <Text
                    component="label"
                    fw={700}
                    size="lg"
                    style={{ backgroundColor: '#FFFFFF', borderRadius: 15 }}
                    pl={20}
                    pr={20}
                    p={10}
                >
                    Proceed to Demo
                </Text>
            </Center>
            <Space h={30} />
            <SimpleGrid
                cols={{ base: 1, md: 2 }}
                spacing={{ base: 'xl', md: 'sm' }}
                p="xl"
            >
                <Card m={20} pl={40} pr={40} shadow="lg" style={{ border: '1.5px solid #000000', borderRadius: 20 }}>
                    <Text
                        component="label"
                        size="md"
                        style={{ backgroundColor: '#FFFFFF', overflow: 'auto' }}
                        p="1rem"
                    >
                        <p style={{ paddingBottom: '0.5rem' }}>
                            This demo is about the <i>Google feedback</i> for the fictional
                            <b>Jumanji Sports Arena</b>.
                            It is a popular location for sports and recreational activities,
                            with branches in <i>Bangalore</i> and <i>Mumbai</i>. <br />
                        </p>
                        The demo will focus on <br />
                        <p style={{ padding: '0.0rem', display: 'flex', alignItems: 'flex-start' }}>
                            <ActionIcon
                                variant="outline"
                                style={{ border: 2, borderRadius: 1, padding: '0.1rem', marginRight: '0.6rem' }}
                            >
                                <IconBallBasketball color="#8C52FF" />
                            </ActionIcon>
                            Feedback insights related to sports activities
                        </p>
                        <p style={{ padding: '0.0rem', display: 'flex', alignItems: 'flex-start' }}>
                            <ActionIcon
                                variant="outline"
                                style={{
                                    color: '#8C52FF',
                                    border: 1,
                                    borderRadius: 1,
                                    padding: '0.1rem',
                                    marginRight: '0.6rem'
                                }}
                            >
                                <IconMoodSmile color="#8C52FF" />
                            </ActionIcon>
                            Customer sentiments, and areas for improvement
                        </p>
                        <p style={{ padding: '0.0rem', display: 'flex', alignItems: 'flex-start' }}>
                            <ActionIcon
                                variant="outline"
                                style={{
                                    color: '#8C52FF',
                                    border: 1,
                                    borderRadius: 1,
                                    padding: '0.1rem',
                                    marginRight: '0.6rem'
                                }}
                            >
                                <IconChartHistogram color="#8C52FF" />
                            </ActionIcon>
                            Dashboard view with various filters for analyzing the data
                        </p>
                    </Text>
                </Card>
                <Card m={20} shadow="lg" style={{ border: '1.5px solid #000000', borderRadius: 20 }}>
                    <Center p="1rem" pb="1rem" display="flex">
                        <Box
                            component="form"
                            role="form"
                            ref={formRef}
                            onSubmit={tryLogin}
                            style={{ border: 1, width: '99%', borderRadius: '1rem', shadow: 5, bgcolor: '#FFFFFF' }}
                        >
                            <Box mb={2}>
                                <Center mb={1} ml={0.5} p="3rem 0rem 1rem 0rem" display="flex">
                                    <Text component="label" variant="caption" size="lg">
                                        Please provide your email
                                    </Text>
                                </Center>
                                <Center mb={1} ml={0.5} p="0rem" display="flex">
                                    <TextInput
                                        name="email"
                                        placeholder="Email"
                                        onChange={handleTextChange}
                                        leftSection={<IconMail />}
                                        rightSection={
                                            <ActionIcon type="submit">
                                                <IconCircleArrowRight />
                                            </ActionIcon>
                                        }
                                        classNames={{ input: classes.input }}
                                        style={{ width: '80%', padding: '1rem' }}
                                        size="xl"
                                        radius="md"
                                    />
                                </Center>
                                <Center mb={1} ml={0.5} display="flex">
                                    <Text
                                        component="label"
                                        variant="caption"
                                        size="md"
                                    >
                                        Or proceed as Guest (without email)
                                    </Text>
                                </Center>
                            </Box>
                            <Center mt={1} mb={1} display="flex">
                                {isLoading
                                    ? (
                                        <Box style={{ width: '100%', paddingTop: '0.1rem', paddingLeft: '45%' }}>
                                            <Loader size={80} />
                                        </Box>
                                    ) : (
                                        <ActionIcon
                                            size={100}
                                            type="submit"
                                            disabled={!canSubmit}
                                            style={{ color: '#8C52FF' }}
                                        >
                                            <IconCircleArrowRight size={80} />
                                        </ActionIcon>
                                    )
                                }
                            </Center>
                            <Box mt={3}>
                                <AlertMessage autoHideDuration={errorDuration} message={message} />
                            </Box>
                        </Box>
                    </Center>
                </Card>
            </SimpleGrid>
        </BackgroundImage>
    );
}
