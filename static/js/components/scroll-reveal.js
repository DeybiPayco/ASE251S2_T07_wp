class ScrollReveal {
  constructor() {
    this.elements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale');
    this.header = document.querySelector('.header');
    this.init();
  }

  init() {
    this.animateHeader();
    this.observeElements();
    this.addMicrointeractions();
  }

  animateHeader() {
    if (this.header) {
      this.header.classList.add('slide-in-down');
      setTimeout(() => {
        this.header.classList.add('animated');
      }, 100);
    }
  }

  observeElements() {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
        }
      });
    }, observerOptions);

    this.elements.forEach(element => {
      observer.observe(element);
    });
  }

  addMicrointeractions() {
    // Botones con efecto bounce (excepto botones de envío de formulario)
    const buttons = document.querySelectorAll('.btn:not([type="submit"])');
    buttons.forEach(button => {
      button.addEventListener('click', (e) => {
        e.preventDefault();
        button.classList.add('bounce');
        setTimeout(() => {
          button.classList.remove('bounce');
        }, 1000);
      });
    });

    // Tarjetas con hover effect
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
      card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-8px) scale(1.02)';
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) scale(1)';
      });
    });

  
    // Animación de typewriter en títulos
    this.typewriterEffect();
  }

  typewriterEffect() {
    const titles = document.querySelectorAll('.section-title, .kicker');
    titles.forEach((title, index) => {
      const text = title.textContent;
      title.textContent = '';
      title.style.opacity = '1';

      setTimeout(() => {
        let i = 0;
        const typeInterval = setInterval(() => {
          if (i < text.length) {
            title.textContent += text.charAt(i);
            i++;
          } else {
            clearInterval(typeInterval);
            title.classList.add('typewriter-complete');
          }
        }, 50);
      }, index * 500);
    });
  }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  new ScrollReveal();
});

// CSS adicional para animación del header
const headerAnimationCSS = `
@keyframes slideInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-in-down {
  animation: slideInDown 0.8s ease both;
}

.typewriter-complete::after {
  content: '|';
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(249, 168, 212, 0.3);
}

.btn:active {
  transform: translateY(0);
}
`;

// Agregar CSS dinámicamente
const style = document.createElement('style');
style.textContent = headerAnimationCSS;
document.head.appendChild(style);