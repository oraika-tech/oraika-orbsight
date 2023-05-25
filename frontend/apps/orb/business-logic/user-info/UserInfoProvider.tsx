import { UserInfo, getProfile } from 'common-utils/service/auth-service';
import React, { useEffect } from 'react';

interface UserProfile {
    userInfo: UserInfo;
    setPreferredTenantId: (tenantId: string) => void;
}

const emptyUserInfo = {
    name: '',
    email: '',
    identifier: '',
    preferredTenantId: '',
    tenants: []
};

const emptyUserProfile = {
    userInfo: emptyUserInfo,
    setPreferredTenantId: () => { }
};

export const UserContext = React.createContext<UserProfile>(emptyUserProfile);

export default function UserInfoProvider({ children }: { children: React.ReactNode }) {
    const [userInfo, setUserInfo] = React.useState<UserInfo>(emptyUserInfo);

    useEffect(() => {
        const syncUserInfo = () => getProfile()
            .then(user => {
                setUserInfo({ ...user, preferredTenantId: user.preferred_tenant_id });
            });

        syncUserInfo();

        return () => setUserInfo(emptyUserInfo);
    }, []);

    const userProfile = {
        userInfo,
        setPreferredTenantId: (tenantId: string) => {
            setUserInfo((info) => ({ ...info, preferredTenantId: tenantId }));
        }
    };

    return (
        <UserContext.Provider value={userProfile}>
            {children}
        </UserContext.Provider>
    );
}
