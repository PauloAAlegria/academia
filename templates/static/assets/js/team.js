document.addEventListener("DOMContentLoaded", function () {
  const section = document.getElementById("team");
  const docenteHeader = document.getElementById("docente-header");
  const staffHeader = document.getElementById("staff-header");

  const categoryTitles = document.querySelectorAll("#team .category-title");
  const paginationContainer = document.createElement("div");
  paginationContainer.id = "team-pagination";
  paginationContainer.style.textAlign = "center";
  paginationContainer.style.marginTop = "40px";

  const categories = [];

  window.addEventListener("resize", () => {
    renderCategoryButtons(); // Re-renderiza os botões ao redimensionar a tela
  });

  // Agrupa títulos e containers
  categoryTitles.forEach((title) => {
    const container = title.nextElementSibling;
    if (container && container.classList.contains("team-container")) {
      categories.push({ title, container });
    }
  });

  // Variáveis para a navegação entre categorias
  // const maxVisibleCategoryButtons = 3;
  function getMaxVisibleCategoryButtons() {
    if (window.innerWidth <= 768) {
      return 2; // Telas pequenas: exibe 2 botões
    }
    return 3; // Telas maiores: exibe 3 botões
  }
  let startIndex = 0;
  let currentCategoryIndex = 0;

  const navLeft = document.createElement("button");
  navLeft.textContent = "←";
  navLeft.style.marginRight = "10px";
  navLeft.addEventListener("click", () => {
    if (currentCategoryIndex > 0) {
      currentCategoryIndex--;
      showCategory(currentCategoryIndex);
    }
  });

  const navRight = document.createElement("button");
  navRight.textContent = "→";
  navRight.style.marginLeft = "10px";
  navRight.addEventListener("click", () => {
    if (currentCategoryIndex < categories.length - 1) {
      currentCategoryIndex++;
      showCategory(currentCategoryIndex);
    }
  });

  const buttonsWrapper = document.createElement("span");
  paginationContainer.appendChild(navLeft);
  paginationContainer.appendChild(buttonsWrapper);
  paginationContainer.appendChild(navRight);

  function renderCategoryButtons() {
    buttonsWrapper.innerHTML = "";
    const maxVisibleButtons = getMaxVisibleCategoryButtons(); // 4 no seu caso
    // Ajusta botão inicial para garantir que currentCategoryIndex esteja visível
    if (currentCategoryIndex < startIndex) {
        startIndex = currentCategoryIndex;
    } else if (currentCategoryIndex > startIndex + maxVisibleButtons - 1) {
        startIndex = currentCategoryIndex - maxVisibleButtons + 1;
    }
    
    const end = Math.min(startIndex + maxVisibleButtons, categories.length);
    for (let i = startIndex; i < end; i++) {
        const btn = document.createElement("button");
        btn.textContent = categories[i].title.textContent;
        if (i === currentCategoryIndex) btn.classList.add("active-category");
        btn.addEventListener("click", () => {
        showCategory(i);
        // Quando clicar no último botão visível, avança o startIndex para mostrar próximos
        if (i === end - 1 && end < categories.length) {
            startIndex++;
            renderCategoryButtons();
        }
        // Se clicar no primeiro botão visível e startIndex > 0, retrocede para mostrar anteriores
        else if (i === startIndex && startIndex > 0) {
            startIndex--;
            renderCategoryButtons();
        }
        });
        buttonsWrapper.appendChild(btn);
    }

    navLeft.disabled = currentCategoryIndex === 0;
    navRight.disabled = currentCategoryIndex === categories.length - 1;
  }

  // Função de paginação interna, retorna função para controlar página externa
  function paginateContainer(container, itemsPerPage = 8, initialPage = 1) {
    const members = container.querySelectorAll(".team-member");
    if (members.length <= itemsPerPage) {
      // Mostrar todos e não criar paginação
      members.forEach(m => m.style.display = "block");
      // Remove paginação caso exista
      const existingPagination = container.parentElement.querySelector(".internal-pagination");
      if (existingPagination) existingPagination.remove();
      return () => {};
    }

    // Variáveis internas de estado
    const totalPages = Math.ceil(members.length / itemsPerPage);
    const maxVisibleButtons = 3;
    let currentPage = initialPage;
    let buttonStart = 1;

    // Criar ou reutilizar div de paginação
    let paginationDiv = container.parentElement.querySelector(".internal-pagination");
    if (!paginationDiv) {
      paginationDiv = document.createElement("div");
      paginationDiv.className = "internal-pagination";
      paginationDiv.style.textAlign = "center";
      paginationDiv.style.marginTop = "20px";
      container.parentElement.appendChild(paginationDiv);
    }
    paginationDiv.innerHTML = ""; // limpa antes

    function adjustButtonWindow(page) {
      if (page < buttonStart) {
        buttonStart = page;
      } else if (page > buttonStart + maxVisibleButtons - 1) {
        buttonStart = page - maxVisibleButtons + 1;
      }
    }

    function showPage(page, updateHistory = true) {
      currentPage = page;
      members.forEach((member, i) => {
        member.style.display = (i >= (page - 1) * itemsPerPage && i < page * itemsPerPage) ? "block" : "none";
      });

      // Ajusta janela de botões para deslizar automaticamente
      if (page === buttonStart + maxVisibleButtons - 1 && buttonStart + maxVisibleButtons - 1 < totalPages) {
        buttonStart++;
      } else if (page === buttonStart && buttonStart > 1) {
        buttonStart--;
      }

      renderButtons();

      if (updateHistory) {
        const categoryName = categories[currentCategoryIndex].title.textContent.trim().toLowerCase().replace(/\s+/g, "-");
        const url = new URL(window.location);
        url.searchParams.set("categoria", categoryName);
        url.searchParams.set("pagina", page);
        history.pushState({ categoria: categoryName, pagina: page }, "", url);
      }

      // Aqui: rolar para o topo da seção #team, com offset (60 px)
        const offset = 60;
        const topPos = section.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top: topPos, behavior: "smooth" });
    }

    function renderButtons() {
      // Garante que o currentPage está visível
      if (currentPage < buttonStart) {
        buttonStart = currentPage;
      } else if (currentPage > buttonStart + maxVisibleButtons - 1) {
        buttonStart = currentPage - maxVisibleButtons + 1;
      }

      paginationDiv.innerHTML = "";

      const navLeft = document.createElement("button");
      navLeft.textContent = "←";
      navLeft.disabled = currentPage === 1;
      navLeft.addEventListener("click", () => {
        if (currentPage > 1) {
          showPage(currentPage - 1);
        }
      });
      paginationDiv.appendChild(navLeft);

      const buttonEnd = Math.min(buttonStart + maxVisibleButtons - 1, totalPages);
      for (let i = buttonStart; i <= buttonEnd; i++) {
        const btn = document.createElement("button");
        btn.textContent = i;
        if (i === currentPage) btn.classList.add("active");
        btn.addEventListener("click", () => showPage(i));
        paginationDiv.appendChild(btn);
      }

      const navRight = document.createElement("button");
      navRight.textContent = "→";
      navRight.disabled = currentPage === totalPages;
      navRight.addEventListener("click", () => {
        if (currentPage < totalPages) {
          showPage(currentPage + 1);
        }
      });
      paginationDiv.appendChild(navRight);
    }

    showPage(currentPage, false);

    // Retorna função para mudar página externamente
    return showPage;
  }

  // Controla a função da paginação interna da categoria atual
  let currentShowPageFunc = () => {};

  function showCategory(index, updateHistory = true) {
    currentCategoryIndex = index;

    categories.forEach((cat, i) => {
      const visible = i === index;
      cat.title.style.display = visible ? "block" : "none";
      cat.container.style.display = visible ? "flex" : "none";
    });

    const titleText = categories[index].title.textContent.trim().toLowerCase();
    const isDocente = titleText === "direção" || titleText === "professores";
    docenteHeader.style.display = isDocente ? "block" : "none";
    staffHeader.style.display = isDocente ? "none" : "block";

    renderCategoryButtons();

    // Cria paginação e guarda função controle
    currentShowPageFunc = paginateContainer(categories[index].container);

    if (updateHistory) {
      const categoryName = titleText.replace(/\s+/g, "-");
      const url = new URL(window.location);
      url.searchParams.set("categoria", categoryName);
      url.searchParams.delete("pagina"); // reset pagina ao trocar categoria
      history.pushState({ categoria: categoryName }, "", url);
    }

    const offset = 60;
    const topPos = section.getBoundingClientRect().top + window.pageYOffset - offset;
    window.scrollTo({ top: topPos, behavior: "smooth" });
  }

  // Mostra navegação por categorias só se houver mais de 1 categorias
  if (categories.length > 1) {
    section.appendChild(paginationContainer);
    renderCategoryButtons();
  }

  // Inicializa com base no URL
  const params = new URLSearchParams(window.location.search);
  const categoriaSlug = params.get("categoria");
  const paginaParam = parseInt(params.get("pagina") || "1", 10);

  let initialIndex = 0;
  if (categoriaSlug) {
    const foundIndex = categories.findIndex(cat =>
      cat.title.textContent.trim().toLowerCase().replace(/\s+/g, "-") === categoriaSlug
    );
    if (foundIndex !== -1) initialIndex = foundIndex;
  }

  showCategory(initialIndex, false);

  // Aplica paginação inicial com página da URL
  setTimeout(() => {
    if (currentShowPageFunc) currentShowPageFunc(paginaParam, false);
  }, 100);

  // Controla histórico do navegador para categoria + paginação
  window.addEventListener("popstate", (event) => {
    const slug = event.state?.categoria || "";
    const pagina = parseInt(event.state?.pagina || "1", 10);

    const foundIndex = categories.findIndex(cat =>
      cat.title.textContent.trim().toLowerCase().replace(/\s+/g, "-") === slug
    );

    const categoryIndex = foundIndex !== -1 ? foundIndex : 0;

    // Mostra categoria sem atualizar o histórico
    showCategory(categoryIndex, false);

    setTimeout(() => {
      if (currentShowPageFunc) currentShowPageFunc(pagina, false);
    }, 50);
  });
});
