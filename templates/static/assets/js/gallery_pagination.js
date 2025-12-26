console.log("galeria-paginacao.js carregado!");

// Aguarda o carregamento do DOM
document.addEventListener("DOMContentLoaded", () => {
  // Seleciona imagens e container da paginação
  const blocosGaleria = document.querySelectorAll('.galeria-container .item-galeria');
  const paginacao = document.getElementById('paginacao');

  const imagensPorPagina = 6; // Quantidade de imagens exibidas por página
  let paginaAtual = 1; // Página ativa

  const totalPaginas = Math.ceil(blocosGaleria.length / imagensPorPagina);

  // Lê o parâmetro da URL para definir a página inicial
  const params = new URLSearchParams(window.location.search);
  const paginaURL = parseInt(params.get('pagina'));


  if (paginaURL && !isNaN(paginaURL) && paginaURL >= 1 && paginaURL <= totalPaginas) {
    paginaAtual = paginaURL;
  }

  // Exibe imagens da página desejada
  function mostrarPagina(pagina, atualizarURL = true) {
    paginaAtual = pagina;
    const inicio = (pagina - 1) * imagensPorPagina;
    const fim = inicio + imagensPorPagina;

    // Mostra ou esconde as imagens conforme o índice
    blocosGaleria.forEach((bloco, index) => {
      bloco.style.display = (index >= inicio && index < fim) ? 'block' : 'none';
    });


    atualizarPaginacao();

    // Atualiza a URL no navegador (sem recarregar a página)
    if (atualizarURL) {
      history.pushState({ pagina: pagina }, '', `?pagina=${pagina}`);
    }

    // Scroll até o início da galeria
    document.getElementById("galeria").scrollIntoView({ behavior: "smooth" });
  }

  // Atualiza os botões de navegação da paginação
  function atualizarPaginacao() {
    paginacao.innerHTML = '';

    // Botão anterior
    if (paginaAtual > 1) {
      const btnAnterior = criarBotao('Anterior', () => mostrarPagina(paginaAtual - 1));
      paginacao.appendChild(btnAnterior);
    }

    // Botões numéricos
    for (let i = 1; i <= totalPaginas; i++) {
      const botao = criarBotao(i, () => mostrarPagina(i));
      if (i === paginaAtual) botao.classList.add('active');
      paginacao.appendChild(botao);
    }

    // Botão próximo
    if (paginaAtual < totalPaginas) {
      const btnProximo = criarBotao('Próximo', () => mostrarPagina(paginaAtual + 1));
      paginacao.appendChild(btnProximo);
    }
  }

  // Cria botão com texto e evento de clique
  function criarBotao(texto, onClick) {
    const botao = document.createElement('button');
    botao.textContent = texto;
    botao.onclick = onClick;
    return botao;
  }

  // Lida com histórico do navegador (voltar/avançar)
  window.onpopstate = function (event) {
    const pagina = event.state?.pagina || 1;
    mostrarPagina(pagina, false);
  };

  // Inicializa com a página atual
  mostrarPagina(paginaAtual, false);
});
