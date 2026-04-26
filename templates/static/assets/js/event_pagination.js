document.addEventListener("DOMContentLoaded", function () {
  const container = document.querySelector(".event-container");
  let cards = Array.from(container.querySelectorAll(".event-card"));
  const cardsPerPage = 4;
  const pagination = document.getElementById("pagination");
  const eventSection = document.getElementById("event");

  let currentPage = 1;

  // Ordena os cards
  cards.sort((a, b) => parseInt(b.dataset.id) - parseInt(a.dataset.id));

  container.innerHTML = "";
  cards.forEach(card => {
    card.style.display = "none"; // garante estado inicial correto
    container.appendChild(card);
  });

  const totalPages = Math.ceil(cards.length / cardsPerPage);

  if (cards.length <= 1) {
    pagination.style.display = "none";
    return;
  }

  function showPage(page, addToHistory = true) {
    currentPage = page;

    cards.forEach((card, index) => {
      if (
        index >= (page - 1) * cardsPerPage &&
        index < page * cardsPerPage
      ) {
        card.style.display = "flex";
      } else {
        card.style.display = "none";
      }
    });

    updatePaginationUI();

    const offset = 60;
    const topPos =
      eventSection.getBoundingClientRect().top +
      window.pageYOffset -
      offset;

    window.scrollTo({ top: topPos, behavior: "smooth" });

    if (addToHistory) {
      const url = new URL(window.location);
      url.searchParams.set("page", page);
      history.pushState({ page }, "", url);
    }
  }

  function createButton(label, onClick, disabled = false, active = false) {
    const btn = document.createElement("button");
    btn.textContent = label;
    btn.disabled = disabled;

    if (active) btn.classList.add("active");

    btn.addEventListener("click", onClick);
    return btn;
  }

  function updatePaginationUI() {
    pagination.innerHTML = "";

    // ← Anterior
    pagination.appendChild(
      createButton("←", () => showPage(currentPage - 1), currentPage === 1)
    );

    const pagesToShow = new Set();

    // mostrar sempre
    pagesToShow.add(1);
    pagesToShow.add(totalPages);

    // Atual, anterior e próxima
    pagesToShow.add(currentPage);
    pagesToShow.add(currentPage - 1);
    pagesToShow.add(currentPage + 1);

    // Filtrar páginas válidas
    const sortedPages = Array.from(pagesToShow)
      .filter(p => p >= 1 && p <= totalPages)
      .sort((a, b) => a - b);

    let lastPage = 0;

    sortedPages.forEach(page => {
      if (page - lastPage > 1) {
        const dots = document.createElement("span");
        dots.textContent = "...";
        pagination.appendChild(dots);
      }

      pagination.appendChild(
        createButton(page, () => showPage(page), false, page === currentPage)
      );

      lastPage = page;
    });

    // → Próximo
    pagination.appendChild(
      createButton(
        "→",
        () => showPage(currentPage + 1),
        currentPage === totalPages
      )
    );
  }

  const params = new URLSearchParams(window.location.search);
  const initialPage = parseInt(params.get("page")) || 1;

  showPage(initialPage);

  window.addEventListener("popstate", (event) => {
    const page = event.state?.page || 1;
    showPage(page, false);
  });
});

console.log(cards.length);