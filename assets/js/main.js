// En-tête qui s'opacifie au défilement, apparitions douces, lecture de la vidéo au clic.
(() => {
  document.documentElement.classList.add('js');

  const entete = document.querySelector('.entete');
  const majEntete = () => entete.classList.toggle('defile', scrollY > 20);
  addEventListener('scroll', majEntete, { passive: true });
  majEntete();

  const elements = document.querySelectorAll('.revele');
  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver((entrees) => {
      for (const e of entrees) {
        if (e.isIntersecting) {
          e.target.classList.add('vu');
          obs.unobserve(e.target);
        }
      }
    }, { rootMargin: '0px 0px -8% 0px' });
    elements.forEach((el) => obs.observe(el));
  } else {
    elements.forEach((el) => el.classList.add('vu'));
  }

  const video = document.getElementById('demo');
  const bouton = document.querySelector('.video-lancer');
  if (video && bouton) {
    bouton.addEventListener('click', () => {
      bouton.parentElement.classList.add('lance');
      video.play();
    });
    video.addEventListener('play', () => bouton.parentElement.classList.add('lance'));
  }
})();
