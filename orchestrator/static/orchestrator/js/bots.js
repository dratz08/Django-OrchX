////import { requireAuth, logout } from "./auth.js";
////
////// Bloqueia acesso de usuários não autenticados
////requireAuth();
////
////// Botão de logout
////document.getElementById("logout").addEventListener("click", () => {
////    logout();
////});
//
//// ------------------------------
//// 1. Redirecionamento do menu lateral
//// ------------------------------
//document.addEventListener("DOMContentLoaded", () => {
//    const menuItems = document.querySelectorAll(".sidebar nav ul li");
//
//    // URLs correspondentes a cada item
//    const urls = {
//        "Bots": "/bots/",
//        "Automações": "/automacoes/",
//        "Agendamentos": "/agendamentos/",
//        "Configurações": "/configuracoes/"
//    };
//
//    menuItems.forEach(item => {
//        item.addEventListener("click", () => {
//            const label = item.querySelector("span").innerText.trim();
//            if (urls[label]) {
//                window.location.href = urls[label];
//            }
//        });
//    });
//});
//
//// ------------------------------
//// 2. Atualização dinâmica do gráfico
//// ------------------------------
//document.addEventListener("DOMContentLoaded", () => {
//    const timeFilter = document.querySelector(".header select");
//    const chartPath = document.querySelector(".circle");
//    const percentageText = document.querySelector(".percentage");
//
//    // Função para buscar novos dados na API
//    async function fetchChartData(period) {
//        try {
//            const response = await fetch(`/api/dashboard-data/?period=${period}`);
//            if (!response.ok) {
//                throw new Error("Erro ao buscar dados do gráfico");
//            }
//            const data = await response.json();
//            return data; // Ex.: { success: 70, fail: 30 }
//        } catch (error) {
//            console.error("Erro na API:", error);
//            return { success: 0, fail: 0 };
//        }
//    }
//
//    // Atualiza o gráfico com os novos dados
//    async function updateChart(period) {
//        const data = await fetchChartData(period);
//        const success = data.success || 0;
//        const total = data.success + data.fail;
//        const percentage = total > 0 ? Math.round((success / total) * 100) : 0;
//
//        // Atualiza a porcentagem no centro do gráfico
//        percentageText.textContent = `${percentage}%`;
//
//        // Atualiza a barra circular
//        chartPath.style.strokeDasharray = `${percentage}, 100`;
//    }
//
//    // Evento para mudar o filtro temporal
//    timeFilter.addEventListener("change", (event) => {
//        const period = event.target.value;
//        updateChart(period);
//    });
//
//    // Atualiza o gráfico ao carregar a página
//    updateChart(timeFilter.value);
//});
//
