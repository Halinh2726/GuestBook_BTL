// main.js - GuestBook Interactive Enhancements

// Mobile Nav Toggle
var navToggle = document.getElementById('nav-toggle');
var navLinks  = document.getElementById('nav-links');
if (navToggle && navLinks) {
  navToggle.addEventListener('click', function() {
    navLinks.classList.toggle('open');
  });
  navLinks.querySelectorAll('.nav-link').forEach(function(link) {
    link.addEventListener('click', function() { navLinks.classList.remove('open'); });
  });
}

// Auto-dismiss Flash Messages after 4 seconds
document.querySelectorAll('.flash').forEach(function(flash) {
  setTimeout(function() {
    flash.style.transition = 'opacity 0.4s, transform 0.4s';
    flash.style.opacity = '0';
    flash.style.transform = 'translateX(40px)';
    setTimeout(function() { flash.remove(); }, 400);
  }, 4000);
});

// Delete Confirmation
function confirmDelete(id) {
  return confirm('Ban co chac muon xoa loi nhan so ' + id + ' khong?');
}

// Character Counter helper
function setupCharCounter(inputId, counterId, max) {
  var input   = document.getElementById(inputId);
  var counter = document.getElementById(counterId);
  if (!input || !counter) return;
  function update() {
    var len = input.value.length;
    counter.textContent = len + ' / ' + max;
    if (len > max * 0.9)       counter.style.color = '#F59E0B';
    else if (len > max * 0.75) counter.style.color = '#94A3B8';
    else                        counter.style.color = '#64748B';
  }
  input.addEventListener('input', update);
  update();
}
setupCharCounter('name',    'name-count', 80);
setupCharCounter('message', 'msg-count',  500);

// Form Submit Spinner
var form      = document.getElementById('guest-form');
var submitBtn = document.getElementById('submit-btn');
if (form && submitBtn) {
  form.addEventListener('submit', function() {
    var text    = submitBtn.querySelector('.btn-text');
    var spinner = submitBtn.querySelector('.btn-spinner');
    if (text && spinner) {
      text.classList.add('hidden');
      spinner.classList.remove('hidden');
      submitBtn.disabled = true;
    }
  });
}

// Animate Leaderboard Bars on Load
var bars = document.querySelectorAll('.lb-bar');
if (bars.length > 0) {
  bars.forEach(function(bar, i) {
    var target = bar.style.width;
    bar.style.width = '0';
    setTimeout(function() { bar.style.width = target; }, 100 + i * 80);
  });
}

// Entry Card Stagger Animation
document.querySelectorAll('.entry-card').forEach(function(card, i) {
  card.style.animationDelay = (i * 0.06) + 's';
});

// Smooth Delete with Fade
document.querySelectorAll('.delete-form').forEach(function(f) {
  f.addEventListener('submit', function() {
    var card = this.closest('.entry-card');
    if (card) {
      card.style.transition = 'opacity 0.3s, transform 0.3s';
      card.style.opacity = '0';
      card.style.transform = 'scale(0.95)';
    }
  });
});
