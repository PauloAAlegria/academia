/* galeria */

// Espera o carregamento completo do DOM para executar o código
document.addEventListener("DOMContentLoaded", () => {
  // Seleciona todos os elementos com a classe "imagem" (imagens/vídeos da galeria)
  const imagens = document.querySelectorAll(".imagem");

  // Seleciona elementos do modal para mostrar imagens ou vídeos
  const modal = document.getElementById("modal");
  const imagemModal = document.getElementById("imagem-modal");
  const videoModal = document.getElementById("video-modal");

  // Botões para fechar modal, navegar para a imagem anterior e próxima
  const fechar = document.getElementById("fechar");
  const prev = document.getElementById("prev");
  const next = document.getElementById("next");

  // Container para os "dots" (indicadores da imagem atual)
  const dotsContainer = document.getElementById("dotsContainer");

  // Índice da imagem/vídeo atualmente exibido no modal
  let indexAtual = 0;

  // Função para abrir o modal na imagem com o índice especificado
  function abrirModal(index) {
    indexAtual = index;
    modal.style.display = "flex"; // Exibe o modal

    // Pausa todos os vídeos da galeria
    document.querySelectorAll("video.imagem").forEach((video) => {
      video.pause();
      video.currentTime = 0;
    });

    // Se ainda não criou os dots, cria agora
    if (dotsContainer.childElementCount === 0) {
      criarDots();
    }

    // Atualiza o conteúdo do modal para a imagem/vídeo atual
    atualizarImagemModal();
  }

  // Função para fechar o modal e pausar o vídeo, se estiver tocando
  function fecharModal() {
    modal.style.display = "none"; // Esconde o modal
    videoModal.pause(); // Pausa vídeo (caso esteja tocando)
    videoModal.src = ""; // Remove a fonte do vídeo para liberar memória

    // Também pausa vídeos da galeria se ainda estiverem tocando por algum motivo
    document.querySelectorAll("video.imagem").forEach((video) => {
      video.pause();
      video.currentTime = 0;
    });
  }

  // Função para mostrar a imagem/vídeo anterior (navegação circular)
  function imagemAnterior() {
    indexAtual = (indexAtual - 1 + imagens.length) % imagens.length;
    atualizarImagemModal();
  }

  // Função para mostrar a imagem/vídeo seguinte (navegação circular)
  function imagemProxima() {
    indexAtual = (indexAtual + 1) % imagens.length;
    atualizarImagemModal();
  }

  // Atualiza o modal para mostrar a imagem ou vídeo do índice atual
  function atualizarImagemModal() {
    const item = imagens[indexAtual];
    
    // Usar apenas o src do atributo para evitar que o navegador reproduza automaticamente
    const src = item.getAttribute("src");

    if (item.tagName.toLowerCase() === "img") {
      // Se for imagem, mostra imagem e esconde vídeo
      imagemModal.style.display = "block";
      imagemModal.src = src;

      videoModal.pause();
      videoModal.style.display = "none";
      videoModal.src = "";
    } else if (item.tagName.toLowerCase() === "video") {
      // Se for vídeo, mostra vídeo e esconde imagem
      videoModal.style.display = "block";
      videoModal.src = src;
      videoModal.currentTime = 0;
      videoModal.play();

      imagemModal.style.display = "none";
      imagemModal.src = "";
    }

    // Atualiza o destaque dos dots para indicar imagem atual
    atualizarDots();
  }

  // Impede que o clique no vídeo ative o player da galeria
  imagens.forEach((item, index) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      abrirModal(index);
    });
  });

  // Evento para fechar o modal ao clicar no botão de fechar
  fechar.addEventListener("click", fecharModal);

  // Fecha o modal se clicar fora da imagem/vídeo (na área do modal)
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      fecharModal();
    }
  });

  // Navegação por teclado quando o modal está aberto
  document.addEventListener("keydown", (e) => {
    if (modal.style.display === "flex") {
      if (e.key === "Escape") {
        fecharModal();
      } else if (e.key === "ArrowLeft") {
        imagemAnterior();
      } else if (e.key === "ArrowRight") {
        imagemProxima();
      }
    }
  });

  // Botões para navegar para imagem anterior e próxima
  prev.addEventListener("click", imagemAnterior);
  next.addEventListener("click", imagemProxima);

  // Suporte a swipe (deslize) para navegação em dispositivos touch
  let touchStartX = 0;
  let touchEndX = 0;

  // Área do modal onde o swipe será detectado
  const areaSwipe = document.querySelector(".modal-conteudo");

  // Registra a posição inicial do toque
  areaSwipe.addEventListener("touchstart", (e) => {
    touchStartX = e.changedTouches[0].screenX;
  });

  // Registra a posição final do toque e chama a função para tratar o swipe
  areaSwipe.addEventListener("touchend", (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  });

  // Função que identifica a direção do swipe e muda a imagem de acordo
  function handleSwipe() {
    const swipeDist = 50; // Distância mínima para considerar um swipe
    if (touchEndX < touchStartX - swipeDist) {
      imagemProxima();
    } else if (touchEndX > touchStartX + swipeDist) {
      imagemAnterior();
    }
  }

  // Cria os "dots" indicadores da posição atual da imagem no modal
  function criarDots() {
    dotsContainer.innerHTML = ""; // Limpa os dots existentes

    imagens.forEach((_, i) => {
      const dot = document.createElement("span");
      dot.classList.add("dot");

      // Marca o dot atual como ativo
      if (i === indexAtual) dot.classList.add("active");

      // Adiciona evento para ir direto para a imagem do dot clicado
      dot.addEventListener("click", () => {
        indexAtual = i;
        atualizarImagemModal();
        scrollDotIntoView(i);
      });

      dotsContainer.appendChild(dot);
    });
  }

  // Atualiza os dots para refletir a imagem atual
  function atualizarDots() {
    const dots = dotsContainer.querySelectorAll(".dot");
    dots.forEach((dot, i) => {
      dot.classList.toggle("active", i === indexAtual);
    });
    scrollDotIntoView(indexAtual);
  }

  // Faz o scroll automático dos dots para manter o dot ativo centralizado na visualização
  function scrollDotIntoView(index) {
    const dot = dotsContainer.querySelectorAll(".dot")[index];
    if (dot) {
      const scrollLeft = dot.offsetLeft - dotsContainer.offsetWidth / 2 + dot.offsetWidth / 2;
      dotsContainer.scrollTo({
        left: scrollLeft,
        behavior: "smooth" // animação suave do scroll
      });
    }
  }
});


/* end galeria */
