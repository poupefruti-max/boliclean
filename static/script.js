let selectedProducts = [];

const slot1El = document.getElementById("slot-1-name");
const slot2El = document.getElementById("slot-2-name");
const historyListEl = document.getElementById("history-list");
const resetBtn = document.getElementById("reset-btn");
const clearHistoryBtn = document.getElementById("clear-history-btn");
const productCards = document.querySelectorAll(".product-card");

// Carregar histórico do localStorage ao abrir a página
document.addEventListener("DOMContentLoaded", carregarHistoricoLocalStorage);

productCards.forEach(card => {
  card.addEventListener("click", () => {
    const id = card.getAttribute("data-id");

    if (selectedProducts.length < 2) {
      selectedProducts.push(id);
      updateSlots();

      if (selectedProducts.length === 2) {
        enviarParaFlask();
      }
    }
  });
});

function updateSlots() {
  slot1El.textContent = selectedProducts[0] || "Vazio";
  slot2El.textContent = selectedProducts[1] || "Vazio";
}

function limparBalde() {
  selectedProducts = [];
  updateSlots();
}

// Envia a requisição POST para a API do Flask
async function enviarParaFlask() {
  try {
    const response = await fetch('/api/misturar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        produto1: selectedProducts[0],
        produto2: selectedProducts[1]
      })
    });

    const data = await response.json();

    // Salva a experiência no localStorage
    salvarNoLocalStorage(data);

    // Alerta o resultado
    setTimeout(() => {
      alert(`[RESULTADO: ${data.status}]\n${data.produto1} + ${data.produto2}\n\n${data.mensagem}`);
      limparBalde();
    }, 100);

  } catch (error) {
    console.error("Erro ao enviar para o servidor Flask:", error);
    alert("Ocorreu um erro ao processar a mistura.");
    limparBalde();
  }
}

// Funções para manipular o LocalStorage
function salvarNoLocalStorage(item) {
  let historico = JSON.parse(localStorage.getItem("historico_misturas")) || [];
  historico.unshift(item); // Adiciona no início da lista
  localStorage.setItem("historico_misturas", JSON.stringify(historico));
  renderizarHistorico();
}

function carregarHistoricoLocalStorage() {
  renderizarHistorico();
}

function renderizarHistorico() {
  let historico = JSON.parse(localStorage.getItem("historico_misturas")) || [];
  historyListEl.innerHTML = "";

  historico.forEach(item => {
    const li = document.createElement("li");
    li.className = "history-item";
    li.innerHTML = `
      <span><strong>${item.produto1}</strong> + <strong>${item.produto2}</strong> — <em>${item.mensagem}</em></span>
      <span class="badge ${item.status.toLowerCase()}">${item.status}</span>
    `;
    historyListEl.appendChild(li);
  });
}

resetBtn.addEventListener("click", limparBalde);

// Botão opcional para limpar o histórico do navegador
if (clearHistoryBtn) {
  clearHistoryBtn.addEventListener("click", () => {
    localStorage.removeItem("historico_misturas");
    renderizarHistorico();
  });
}

// Elementos do Modal
const customModal = document.getElementById("custom-modal");
const modalBox = customModal.querySelector(".modal-box");
const modalIcon = document.getElementById("modal-icon");
const modalStatus = document.getElementById("modal-status");
const modalProducts = document.getElementById("modal-products");
const modalMessage = document.getElementById("modal-message");
const modalCloseBtn = document.getElementById("modal-close-btn");

// Mapeamento de ícones por status
const STATUS_ICONS = {
  PODE: "✅",
  CUIDADO: "⚠️",
  INIBE: "🔄",
  NAO_PODE: "🚫"
};

// Exibe o modal formatado
function mostrarModal(data) {
  const statusKey = data.status.toUpperCase();
  
  // Limpa classes anteriores e adiciona a nova do status
  modalBox.className = "modal-box " + data.status.toLowerCase();
  
  modalIcon.textContent = STATUS_ICONS[statusKey] || "🧪";
  modalStatus.textContent = data.status.replace("_", " ");
  modalProducts.textContent = `${data.produto1} + ${data.produto2}`;
  modalMessage.textContent = data.mensagem;

  customModal.classList.remove("hidden");
}

// Fecha o modal e limpa o balde
modalCloseBtn.addEventListener("click", () => {
  customModal.classList.add("hidden");
  limparBalde();
});

// Envia a requisição POST para o Flask
async function enviarParaFlask() {
  try {
    const response = await fetch('/api/misturar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        produto1: selectedProducts[0],
        produto2: selectedProducts[1]
      })
    });

    const data = await response.json();

    // Salva no LocalStorage
    salvarNoLocalStorage(data);

    // Abre o aviso bonitinho
    mostrarModal(data);

  } catch (error) {
    console.error("Erro ao enviar para o servidor Flask:", error);
    mostrarModal({
      status: "NAO_PODE",
      produto1: "Erro",
      produto2: "Conexão",
      mensagem: "Não foi possível processar a mistura no momento."
    });
  }
}
const bucketCard = document.getElementById("bucket-card");

async function enviarParaFlask() {
  try {
    // Liga a animação de balanço no balde
    if (bucketCard) bucketCard.classList.add("mixing");

    const response = await fetch('/api/misturar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        produto1: selectedProducts[0],
        produto2: selectedProducts[1]
      })
    });

    const data = await response.json();

    // Desliga a animação após receber a resposta
    if (bucketCard) bucketCard.classList.remove("mixing");

    salvarNoLocalStorage(data);
    mostrarModal(data);

  } catch (error) {
    if (bucketCard) bucketCard.classList.remove("mixing");
    console.error("Erro ao enviar para o servidor Flask:", error);
  }
}