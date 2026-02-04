document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll(".event-card");
  const cardsPerPage = 4;
  const minCardsForPagination = 1;
  const pagination = document.getElementById("pagination");
  const eventSection = document.getElementById("event");
  const totalPages = Math.ceil(cards.length / cardsPerPage);

  if (cards.length <= minCardsForPagination) {
    pagination.style.display = "none";
    return;
  }

  function showPage(page, addToHistory = true) {
    cards.forEach((card, index) => {
      if (index >= (page - 1) * cardsPerPage && index < page * cardsPerPage) {
        card.style.display = "flex";
      } else {
        card.style.display = "none";
      }
    });

    const buttons = pagination.querySelectorAll("button");
    buttons.forEach(btn => btn.classList.remove("active"));
    if (buttons[page - 1]) {
      buttons[page - 1].classList.add("active");
    }

    const offset = 60;
    const topPos = eventSection.getBoundingClientRect().top + window.pageYOffset - offset;
    window.scrollTo({ top: topPos, behavior: "smooth" });

    // Atualiza a URL sem recarregar a página
    if (addToHistory) {
      const url = new URL(window.location);
      url.searchParams.set("page", page);
      history.pushState({ page }, "", url);
    }
  }

  function createPaginationButtons() {
    for (let i = 1; i <= totalPages; i++) {
      const btn = document.createElement("button");
      btn.textContent = i;
      btn.addEventListener("click", () => showPage(i));
      pagination.appendChild(btn);
    }
  }

  // Lê a página da URL ao carregar
  const params = new URLSearchParams(window.location.search);
  const initialPage = parseInt(params.get("page")) || 1;

  createPaginationButtons();
  showPage(initialPage);

  // Suporte ao botão "Voltar" do navegador
  window.addEventListener("popstate", (event) => {
    const page = event.state?.page || 1;
    showPage(page, false);
  });
});