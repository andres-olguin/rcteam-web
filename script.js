(() => {
  "use strict";
  const header = document.querySelector(".site-header");
  const nav = document.getElementById("main-nav");
  const toggle = document.querySelector(".menu-toggle");
  const backdrop = document.querySelector(".menu-backdrop");
  const setScrolled = () => header?.classList.toggle("is-scrolled", window.scrollY > 25);
  setScrolled();
  window.addEventListener("scroll", setScrolled, { passive: true });

  const closeMenu = () => {
    nav?.classList.remove("is-open");
    backdrop?.classList.remove("is-visible");
    document.body.classList.remove("menu-open");
    toggle?.setAttribute("aria-expanded", "false");
    toggle?.setAttribute("aria-label", "Abrir menú");
  };
  toggle?.addEventListener("click", () => {
    const open = toggle.getAttribute("aria-expanded") !== "true";
    nav?.classList.toggle("is-open", open);
    backdrop?.classList.toggle("is-visible", open);
    document.body.classList.toggle("menu-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  });
  nav?.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
  backdrop?.addEventListener("click", closeMenu);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      const wasOpen = toggle?.getAttribute("aria-expanded") === "true";
      closeMenu();
      if (wasOpen) toggle?.focus();
    }
    if (event.key === "Tab" && toggle?.getAttribute("aria-expanded") === "true") {
      const items = [toggle, ...nav.querySelectorAll("a")];
      const first = items[0], last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  });
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".nav-shell")) closeMenu();
  });
  window.matchMedia("(min-width: 851px)").addEventListener?.("change", closeMenu);

  const animated = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    document.documentElement.classList.add("reveal-enabled");
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          obs.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -35px 0px", threshold: .08 });
    animated.forEach((node) => observer.observe(node));
  } else {
    animated.forEach((node) => node.classList.add("in-view"));
  }

  const filters = document.querySelectorAll("[data-filter]");
  const tiles = document.querySelectorAll("[data-category]");
  const mediaGrid = document.querySelector(".media-grid");
  const filterStatus = document.getElementById("filter-status");
  filters.forEach((filter) => filter.addEventListener("click", () => {
    const selected = filter.dataset.filter;
    filters.forEach((btn) => {
      const active = btn === filter;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", String(active));
    });
    let visible = 0;
    tiles.forEach((tile) => {
      tile.hidden = selected !== "all" && tile.dataset.category !== selected;
      if (!tile.hidden) visible += 1;
    });
    mediaGrid?.classList.toggle("is-filtered", selected !== "all");
    if (filterStatus) {
      filterStatus.textContent = "Mostrando " + visible + (visible === 1 ? " categoría de medios." : " categorías de medios.");
    }
  }));

  // GitHub Pages is a public demo: prepare a local email draft instead of
  // making an unapproved live submission to the client's FormSubmit endpoint.
  const form = document.getElementById("contact-form");
  const feedback = document.getElementById("form-feedback");
  form?.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const name = String(data.get("nombre") || "").trim();
    const email = String(data.get("email") || "").trim();
    const message = String(data.get("mensaje") || "").trim();
    const phone = String(data.get("telefono") || "").trim();
    const project = String(data.get("proyecto") || "").trim();
    if (!name || !email || !message) return;
    const subject = "Consulta web RC Team - " + name;
    const body = "Nombre: " + name + "\nCorreo: " + email
      + (phone ? "\nTeléfono: " + phone : "")
      + (project ? "\nProyecto: " + project : "")
      + "\n\nMensaje:\n" + message;
    const url = "mailto:contacto@rcteam.cl?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    feedback.textContent = "Se preparará un borrador en tu aplicación de correo. El envío queda a tu cargo.";
    window.location.href = url;
  });

  const year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();