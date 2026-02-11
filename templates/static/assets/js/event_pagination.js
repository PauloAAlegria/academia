document.addEventListener("DOMContentLoaded", function () {
  const container = document.querySelector(".event-container");
  let cards = Array.from(container.querySelectorAll(".event-card"));
  const cardsPerPage = 4;
  const pagination = document.getElementById("pagination");
  const eventSection = document.getElementById("event");

  // Ordena os cards pelo ID do evento (assumindo que o ID está no atributo data-id)
  cards.sort((a, b) => parseInt(b.dataset.id) - parseInt(a.dataset.id));

  // Atualiza o container com os cards na nova ordem
  container.innerHTML = "";
  cards.forEach(card => container.appendChild(card));

  const totalPages = Math.ceil(cards.length / cardsPerPage);
  if (cards.length <= 1) {
    pagination.style.display = "none";
    return;
  }

  function showPage(page, addToHistory = true) {
    cards.forEach((card, index) => {
      card.style.display = (index >= (page - 1) * cardsPerPage && index < page * cardsPerPage) ? "flex" : "none";
    });

    const buttons = pagination.querySelectorAll("button");
    buttons.forEach(btn => btn.classList.remove("active"));
    if (buttons[page - 1]) buttons[page - 1].classList.add("active");

    const offset = 60;
    const topPos = eventSection.getBoundingClientRect().top + window.pageYOffset - offset;
    window.scrollTo({ top: topPos, behavior: "smooth" });

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

  const params = new URLSearchParams(window.location.search);
  const initialPage = parseInt(params.get("page")) || 1;

  createPaginationButtons();
  showPage(initialPage);

  window.addEventListener("popstate", (event) => {
    const page = event.state?.page || 1;
    showPage(page, false);
  });
});
