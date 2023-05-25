const userInfoKey = 'user-info';

export function setLocalUser(profile) {
    localStorage.setItem(userInfoKey, JSON.stringify(profile));
}

export function setLocalUserEmail(email) {
    const profile = { email };
    setLocalUser(profile);
}

export function clearLocalUser() {
    //localStorage.removeItem(userInfoKey);
}

export function getLocalUser() {
    const userInfoRow = localStorage.getItem(userInfoKey);
    if (userInfoRow) {
        return JSON.parse(userInfoRow);
    }
    return {};
}

export function getLocalUserEmail() {
    const localUser = getLocalUser();
    if (localUser && localUser.email) {
        return localUser.email;
    }
    return null;
}

export function localUserEquals(userInfo) {
    return (JSON.stringify(userInfo) === JSON.stringify(getLocalUser()));
}
