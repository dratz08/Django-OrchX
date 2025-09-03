import { requireAuth, logout } from "./auth.js";

// Bloqueia acesso de usuários não autenticados
requireAuth();

// Botão de logout
document.getElementById("logout").addEventListener("click", () => {
    logout();
});
