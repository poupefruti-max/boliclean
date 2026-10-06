let selectedProducts = [];

const slot1El = document.getElementById("slot-1-name");
const slot2El = document.getElementById("slot-2-name");
const historyListEl = document.getElementById("history-list");
const resetBtn = document.getElementById("reset-btn");
const productCards = document.querySelectorAll(".product-card");

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

    // Adiciona o resultado retornado pelo Flask no topo do histórico
    const li = document.createElement("li");
    li.className = "history-item";
    li.innerHTML = `
      <span><strong>${data.produto1}</strong> + <strong>${data.produto2}</strong> — <em>${data.mensagem}</em></span>
      <span class="badge ${data.status.toLowerCase()}">${data.status}</span>
    `;

    historyListEl.prepend(li);

    // Exibe o aviso ao usuário com o resultado da mistura
    setTimeout(() => {
      alert(`[RESULTADO: ${data.status}]\n${data.produto1} + ${data.produto2}\n\n${data.mensagem}`);
      
      // Limpa o balde imediatamente após fechar o aviso
      limparBalde();
    }, 100);

  } catch (error) {
    console.error("Erro ao enviar para o servidor Flask:", error);
    alert("Ocorreu um erro ao processar a mistura.");
    limparBalde();
  }
}

resetBtn.addEventListener("click", limparBalde);