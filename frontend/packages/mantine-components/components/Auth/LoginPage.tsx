import {
    Anchor,
    Button,
    Center,
    Checkbox,
    Container,
    Group,
    Loader,
    Paper,
    PasswordInput,
    Text,
    TextInput,
    Title
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { doLogin, getProfile } from 'common-utils/service/auth-service';
import AlertMessage from 'mantine-components/components/AlertMessage';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

interface LoginPageProps {
    isForgetPassword?: boolean
}

export default function LoginPage({ isForgetPassword }: LoginPageProps) {
    const router = useRouter();
    const [errorMessage, setErrorMessage] = useState('');
    const [shouldLogin, setShouldLogin] = useState(false);
    const form = useForm({
        initialValues: {
            username: '',
            password: ''
        },

        validate: {
            username: (value) => value.length >= 255
                ? 'Email is very long'
                : (/^[\w]([\w\-.+&'/]*)@([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,22}$/.test(value)
                    ? null
                    : 'Invalid email'),
            password: (value) => value.length >= 255 ? 'Name is very long' : null
        }
    });

    useEffect(() => {
        const syncUserInfo = () => getProfile()
            .then(user => {
                if (user.preferred_tenant_id) {
                    const orbUrl = process.env.NEXT_PUBLIC_ORB_WEBSITE_URL;
                    if (orbUrl) {
                        router.push(orbUrl);
                    }
                } else {
                    setShouldLogin(true);
                }
            })
            .catch(() => setShouldLogin(true));

        syncUserInfo();
    }, []);

    const submitForm = (values: { username: string, password: string }) => {
        doLogin(values.username, values.password)
            .then(
                loginResponse => {
                    if (loginResponse.status) {
                        router.push(process.env.NEXT_PUBLIC_ORB_WEBSITE_URL || '/');
                    } else {
                        // setErrorMessage();
                        setErrorMessage('Login Failed, Please try again !');
                    }
                },
                error => {
                    // setErrorMessage();
                    setErrorMessage('Login Failed, Please try again !');
                    console.log(error);
                }
            );
    };

    if (!shouldLogin) {
        return <Center> <Loader variant="dots" /> </Center>;
    }

    return (
        <Container w={500} size="md" my={80}>
            <Title
                ta="center"
                style={(theme) => ({ fontFamily: `Greycliff CF, ${theme.fontFamily}`, fontWeight: 900 })}
            >
                Welcome back!
            </Title>
            <Text c="dimmed" size="sm" ta="center" mt={5}>
                Do not have an account yet?{' '}
                <Anchor href="/signup" size="sm">
                    Create account
                </Anchor>
            </Text>

            <Paper withBorder shadow="md" p={50} mt={50} radius="md">
                <form
                    id="form"
                    name="form"
                    acceptCharset="UTF-8"
                    onSubmit={form.onSubmit((values) => submitForm(values))}
                >
                    <TextInput
                        name="username"
                        label="Email"
                        placeholder="Your email"
                        size="md"
                        required
                        {...form.getInputProps('username')}
                    />
                    <PasswordInput
                        name="password"
                        label="Password"
                        placeholder="Your password"
                        required
                        mt="lg"
                        {...form.getInputProps('password')}
                    />
                    {isForgetPassword && (
                        <Group justify="space-between" mt="lg">
                            <Checkbox label="Remember me" />
                            <Anchor component="button" size="sm">
                                Forgot password?
                            </Anchor>
                        </Group>
                    )}
                    <Button type="submit" fullWidth mt="xl">
                        Sign in
                    </Button>
                </form>
                <AlertMessage autoHideDuration={10000} message={errorMessage} />
            </Paper>
        </Container>
    );
}

LoginPage.defaultProps = {
    isForgetPassword: false
};
