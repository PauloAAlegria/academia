// Seletores
const navbar = document.getElementById('navbar');
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');
const mobileDropdownToggle = document.getElementById('mobileDropdownToggle');
const mobileDropdown = document.getElementById('mobileDropdown');

// Scroll: altera cor do menu quando a página é rolada
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 0); // Adiciona a classe "scrolled" quando a rolagem é maior que 0
  hamburger.classList.toggle('scrolled', window.scrollY > 0); // Adiciona a classe "scrolled" ao hamburger para mudar a cor das barras
});

// Menu mobile toggle: Alterna a exibição do menu mobile
hamburger.addEventListener('click', () => {
  mobileMenu.classList.toggle('open');  // Alterna a classe "open" no menu mobile
  hamburger.classList.toggle('open');  // Alterna o ícone hamburger para "X"
});

// Dropdown mobile toggle: Exibe/oculta o menu dropdown mobile
mobileDropdownToggle.addEventListener('click', () => {
  const isVisible = mobileDropdown.style.display === 'block';
  mobileDropdown.style.display = isVisible ? 'none' : 'block';  // Alterna a exibição do menu dropdown
});

// Fecha menu mobile ao clicar nos links de navegação
document.querySelectorAll('.mobile-menu a').forEach(link => {
  link.addEventListener('click', () => {
    mobileMenu.classList.remove('open'); // Fecha o menu mobile
    hamburger.classList.remove('open');  // Retorna o ícone do hamburger ao estado inicial
    mobileDropdown.style.display = 'none'; // Fecha o dropdown mobile
  });
});

// Fecha o menu hamburger se clicar fora dele
document.addEventListener('click', (e) => {
  const isClickInsideMenu = mobileMenu.contains(e.target) || hamburger.contains(e.target);
  if (!isClickInsideMenu) {
    mobileMenu.classList.remove('open'); // Fecha o menu mobile
    hamburger.classList.remove('open');  // Retorna o ícone ao estado inicial
  }
});

// forçar a rolagem manualmente com um ajuste mais direto, usando window.scrollTo
// para garantir que a posição seja exata na escolha da seção do menu
document.addEventListener('DOMContentLoaded', function() {
  const links = document.querySelectorAll('a[href^="#"]');

  links.forEach(function(link) {
    link.addEventListener('click', function(e) {
      e.preventDefault();

      const targetId = link.getAttribute('href');
      const targetSection = document.querySelector(targetId);

      if (targetSection) {
        const topOffset = targetSection.offsetTop; // Obtém a posição no topo da seção
        window.scrollTo({
          top: topOffset - 60, // Ajuste aqui para compensar a altura do cabeçalho fixo (60px é apenas um exemplo)
          behavior: 'smooth'
        });
      }
    });
  });
});

// Remove qualquer #hash da URL após carregamento
window.addEventListener("load", () => {
  if (window.location.hash) {
    history.replaceState(null, null, window.location.pathname + window.location.search);
  }
});

// Também remove o hash após qualquer clique em link com #
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', (e) => {
    // Permite o scroll suave normalmente
    e.preventDefault();
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
      // Remove o hash da URL logo depois
      history.replaceState(null, null, window.location.pathname + window.location.search);
    }
  });
});