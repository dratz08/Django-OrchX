// static/js/auth.js

// 1. Recupera o token armazenado
export function getAccessToken() {
    return localStorage.getItem("access");
}

// 2. Verifica se o usuário está autenticado
export function isAuthenticated() {
    const token = getAccessToken();
    return token !== null;
}

// 3. Redireciona para o login se não estiver autenticado
export function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = "/login/";
    }
}

// 4. Remove os tokens do usuário → Logout
export function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    window.location.href = "/login/";
}

// 5. Decodifica o payload do JWT para verificar expiração
function parseJwt(token) {
    try {
        return JSON.parse(atob(token.split(".")[1]));
    } catch (e) {
        return null;
    }
}

export function isTokenValid() {
    const token = getAccessToken();
    if (!token) return false;

    const payload = parseJwt(token);
    if (!payload) return false;

    // O campo exp do JWT está em segundos
    const now = Math.floor(Date.now() / 1000);
    return payload.exp > now;
}

export function requireAuth() {
    if (!isTokenValid()) {
        // Se o token expirou, apaga e redireciona
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        window.location.href = "/login/";
    }
}
