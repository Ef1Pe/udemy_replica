const navToggle = document.querySelector('.mobile-nav-toggle');
const primaryNav = document.querySelector('.primary-nav');

if (navToggle && primaryNav) {
  navToggle.addEventListener('click', () => {
    const isOpen = primaryNav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });
}

const railTrack = document.querySelector('.rail-track');
const railButtons = document.querySelectorAll('.rail-controls button');

if (railTrack && railButtons.length) {
  railTrack.setAttribute('tabindex', '-1');
  railTrack.style.scrollBehavior = 'smooth';
  railButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const dir = button.dataset.dir === 'prev' ? -1 : 1;
      railTrack.scrollLeft += dir * railTrack.clientWidth * 0.8;
    });
  });
}

const defaultCourses = [
  {
    title: 'Leading with Generative AI',
    instructor: 'Maya Brooks',
    category: 'AI & Machine Learning',
    price: '$15.99',
    oldPrice: '$89.99',
    rating: '4.9',
    reviews: '(5,421)',
    image: 'https://images.unsplash.com/photo-1529333166437-7750a6dd5a70?auto=format&fit=crop&w=400&q=60',
  },
  {
    title: 'Strategic Leadership Accelerator',
    instructor: 'Frank Kane',
    category: 'Leadership',
    price: '$17.99',
    oldPrice: '$99.99',
    rating: '4.8',
    reviews: '(9,312)',
    image: 'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=400&q=60',
  },
];

function buildCourseCard({ title, instructor, category, price, oldPrice, rating, reviews, image, injected }) {
  const article = document.createElement('article');
  article.className = 'course-card' + (injected ? ' injected' : '');
  article.innerHTML = `
    <img src="${image}" alt="${title}">
    <div class="course-content">
      <p class="course-category">${category}</p>
      <h3>${title}</h3>
      <p class="instructor">${instructor}</p>
      <div class="rating">
        <span>${rating}</span>
        <div class="stars"></div>
        <span>${reviews}</span>
      </div>
      <div class="price-row">
        <span class="price">${price}</span>
        <span class="old-price">${oldPrice}</span>
      </div>
    </div>`;
  return article;
}

function hydrateCourseGrid(data, target, markInjected = false) {
  data.forEach((item) => {
    const card = buildCourseCard({ ...item, injected: markInjected });
    target.appendChild(card);
  });
}

const courseTarget = document.querySelector('[data-inject-target="courses"]');
if (courseTarget) {
  hydrateCourseGrid(defaultCourses, courseTarget, false);
}

async function fetchInjectedContent() {
  try {
    const response = await fetch('/api/content');
    if (!response.ok) return;
    const payload = await response.json();
    const filtered = payload.content?.filter((item) => item.section === 'courses') ?? [];
    if (filtered.length && courseTarget) {
      const normalized = filtered.map((item) => ({
        title: item.title ?? 'New Udemy Course',
        instructor: item.instructor ?? 'Top Instructor',
        category: item.category ?? 'Trending',
        price: item.price ?? '$9.99',
        oldPrice: item.old_price ?? '$49.99',
        rating: item.rating ?? '4.7',
        reviews: item.reviews ?? '(1,000)',
        image: item.image_url ?? 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=400&q=60',
      }));
      hydrateCourseGrid(normalized, courseTarget, true);
    }
  } catch (err) {
    console.error('Failed to load injected content', err);
  }
}

fetchInjectedContent();

const observerTargets = document.querySelectorAll('.case-content, .report-card, .reimagine');
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
      }
    });
  },
  { threshold: 0.2 }
);
observerTargets.forEach((el) => observer.observe(el));
