import {
    Box,
    Center,
    Loader
} from '@mantine/core';
import { UserInfo, getProfile } from 'common-utils/service/auth-service';
import { useRouter } from 'next/router';
import { createContext, useEffect, useState } from 'react';
import LoginPage from './LoginPage';

export interface UserProfile {
    userInfo: UserInfo;
    setPreferredTenantId: (tenantId: string) => void;
    clearUserInfo: () => void;
    refreshPage: () => void;
    isLoggedIn: () => boolean;
}

const emptyUserInfo: UserInfo = {
    name: '',
    email: '',
    identifier: '',
    preferredTenantId: '',
    tenants: []
};

const emptyUserProfile = {
    userInfo: emptyUserInfo,
    setPreferredTenantId: () => { },
    clearUserInfo: () => { },
    refreshPage: () => { },
    isLoggedIn: () => false
};

export const UserContext = createContext<UserProfile>(emptyUserProfile);

export interface LoginProps {
    refreshPage: () => void
}

interface AuthProviderProps {
    loginUrl: string
    redirectUrl?: string
    publicPaths?: Set<string>
    children?: React.ReactNode
}

export default function AuthProvider({ loginUrl, redirectUrl, publicPaths, children }: AuthProviderProps) {
    const router = useRouter();
    const [userInfo, setUserInfo] = useState<UserInfo>(emptyUserInfo);
    const [shouldLogin, setShouldLogin] = useState<boolean | null>(null);
    const [key, setKey] = useState(Math.random());

    if (publicPaths && publicPaths.has(router.asPath)) {
        return children;
    }

    const refreshPage = () => {
        setKey(Math.random()); // change key state to re-render page
    };

    useEffect(() => {
        const handleSuccess = (user: UserInfo) => {
            setUserInfo(user);
            if (redirectUrl) {
                router.push(redirectUrl);
            } else {
                setShouldLogin(false);
            }
        };

        const syncUserInfo = () => getProfile()
            .then(user => {
                if (user.preferred_tenant_id) {
                    handleSuccess({ ...user, preferredTenantId: user.preferred_tenant_id });
                } else {
                    setUserInfo(emptyUserInfo);
                    setShouldLogin(true);
                    // router.push(loginUrl);
                }
            })
            .catch(() => {
                setShouldLogin(true);
                // router.push(loginUrl);
            });

        syncUserInfo();

        return () => setUserInfo(emptyUserInfo);
    }, [key]);

    if (shouldLogin === true) {
        // todo: add support demo login also
        // todo: pass refresh key instead of shouldlogin. currently passing shouldlogin to do refersh
        return <LoginPage setShouldLogin={setShouldLogin} />;

    } else {
        let page = null;
        if (loginUrl.endsWith(router.asPath)) {
            page = children;
        } else {
            switch (shouldLogin) {
                case null: // loading
                    page = <Center> <Loader variant="dots" /> </Center>;
                    break;

                // case true: // login require
                //     return <LoginPage />;
                //     // page = <Center> <Loader variant="bars" /> </Center>;
                //     break;

                case false: // already logged in
                    page = children;
                    break;
            }
        }

        const userProfile = {
            userInfo,
            refreshPage,
            setPreferredTenantId: (tenantId: string) => {
                setUserInfo((info) => ({ ...info, preferredTenantId: tenantId }));
            },
            clearUserInfo: () => {
                setUserInfo(emptyUserInfo);
            },
            isLoggedIn: () => !!userInfo.email
        };

        return (
            <UserContext.Provider value={userProfile}>
                <Box key={key}>
                    {page}
                </Box>
            </UserContext.Provider>
        );
    }
}
