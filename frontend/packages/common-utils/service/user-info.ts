import { UserInfo } from './auth-service';

const userInfoKey = 'user-info';

export function setLocalUser(profile: UserInfo) {
    localStorage.setItem(userInfoKey, JSON.stringify(profile));
}

// export function setLocalUserEmail(email) {
//     const profile = { email };
//     setLocalUser(profile);
// }

// export function clearLocalUser() {
//     //localStorage.removeItem(userInfoKey);
// }

export function getLocalUser(): UserInfo | null {
    const userInfoRow = localStorage.getItem(userInfoKey);
    if (userInfoRow) {
        return JSON.parse(userInfoRow);
    }
    return null;
}

export function getLocalUserEmail() {
    const localUser = getLocalUser();
    if (localUser && localUser.email) {
        return localUser.email;
    }
    return null;
}

// export function localUserEquals(userInfo) {
//     return (JSON.stringify(userInfo) === JSON.stringify(getLocalUser()));
// }
