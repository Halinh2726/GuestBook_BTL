(function () {
  "use strict";

  var root = document.documentElement;
  var themeButton = document.querySelector(".theme-button");
  var menuButton = document.querySelector(".menu-button");
  var navigation = document.querySelector(".main-nav");

  function savedTheme() {
    try {
      return localStorage.getItem("dau-an-theme");
    } catch (error) {
      return null;
    }
  }

  var preferredTheme = savedTheme();
  if (!preferredTheme && window.matchMedia("(prefers-color-scheme: dark)").matches) {
    preferredTheme = "dark";
  }
  root.dataset.theme = preferredTheme || "light";

  if (themeButton) {
    themeButton.addEventListener("click", function () {
      var nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
      root.dataset.theme = nextTheme;
      try {
        localStorage.setItem("dau-an-theme", nextTheme);
      } catch (error) {
        // The selected theme still applies for this visit.
      }
    });
  }

  if (menuButton && navigation) {
    menuButton.addEventListener("click", function () {
      var isOpen = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!isOpen));
      navigation.classList.toggle("is-open", !isOpen);
    });
    navigation.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        menuButton.setAttribute("aria-expanded", "false");
        navigation.classList.remove("is-open");
      });
    });
  }

  var revealItems = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var revealObserver = new IntersectionObserver(function (entries, observer) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -24px" });
    revealItems.forEach(function (item) { revealObserver.observe(item); });
  } else {
    revealItems.forEach(function (item) { item.classList.add("is-visible"); });
  }

  document.querySelectorAll(".toast").forEach(function (toast) {
    var closeButton = toast.querySelector("button");
    function closeToast() {
      toast.style.opacity = "0";
      toast.style.transform = "translateY(-10px)";
      setTimeout(function () { toast.remove(); }, 220);
    }
    if (closeButton) closeButton.addEventListener("click", closeToast);
    setTimeout(closeToast, 5000);
  });

  function normalize(value) {
    return value
      .toLocaleLowerCase("vi")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/đ/g, "d");
  }

  var searchInput = document.getElementById("entry-search");
  var entryCards = Array.prototype.slice.call(document.querySelectorAll(".entry-card"));
  var noResults = document.getElementById("no-results");
  var clearSearch = document.getElementById("clear-search");

  function filterEntries() {
    var query = normalize(searchInput.value.trim());
    var visibleCount = 0;
    entryCards.forEach(function (card) {
      var matches = normalize(card.dataset.search || "").indexOf(query) !== -1;
      card.classList.toggle("filtered-out", !matches);
      if (matches) visibleCount += 1;
    });
    if (noResults) noResults.hidden = visibleCount !== 0;
  }

  if (searchInput) searchInput.addEventListener("input", filterEntries);
  if (clearSearch) {
    clearSearch.addEventListener("click", function () {
      searchInput.value = "";
      filterEntries();
      searchInput.focus();
    });
  }

  document.querySelectorAll(".delete-form").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      var button = form.querySelector("[data-entry-name]");
      var name = button ? button.dataset.entryName : "này";
      if (!window.confirm("Xóa lời nhắn của " + name + "? Hành động này không thể hoàn tác.")) {
        event.preventDefault();
      }
    });
  });

  var nameInput = document.getElementById("name");
  var messageInput = document.getElementById("message");
  var nameCount = document.getElementById("name-count");
  var messageCount = document.getElementById("message-count");
  var previewName = document.getElementById("preview-name");
  var previewMessage = document.getElementById("preview-message");

  function updateComposePreview() {
    if (!nameInput || !messageInput) return;
    var name = nameInput.value.trim();
    var message = messageInput.value.trim();
    nameCount.textContent = nameInput.value.length + " / 80";
    messageCount.textContent = messageInput.value.length + " / 500";
    previewName.textContent = "— " + (name || "Tên của bạn");
    previewMessage.textContent = "“" + (message || "Lời nhắn của bạn sẽ xuất hiện ở đây.") + "”";
  }

  if (nameInput && messageInput) {
    nameInput.addEventListener("input", updateComposePreview);
    messageInput.addEventListener("input", updateComposePreview);
    updateComposePreview();
  }

  var guestForm = document.getElementById("guest-form");
  var submitButton = document.getElementById("submit-button");
  if (guestForm && submitButton) {
    guestForm.addEventListener("submit", function (event) {
      if (!guestForm.checkValidity()) {
        event.preventDefault();
        guestForm.reportValidity();
        return;
      }
      submitButton.classList.add("is-submitting");
      submitButton.disabled = true;
    });
  }

  var year = document.getElementById("current-year");
  if (year) year.textContent = new Date().getFullYear();
})();
