document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("message");

    try {
        const response = await fetch("/api/token/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            // Salva os tokens no localStorage
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);

            message.style.color = "green";
            message.textContent = "Login realizado com sucesso!";

            // Redireciona para o dashboard (exemplo)
            setTimeout(() => window.location.href = "/dashboard/", 1000);
        } else {
            message.style.color = "red";
            message.textContent = data.detail || "Credenciais inválidas!";
        }
    } catch (error) {
        message.style.color = "red";
        message.textContent = "Erro ao conectar com o servidor.";
    }
});