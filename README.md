# Udemy.com Replica

A medium-fidelity, production-ready replica of the Udemy homepage with supporting subpages, Tailwind-inspired styling, and a Flask backend that supports dynamic course injection.

## 📁 Project Structure
```
├── index.html                # Hero landing page replica
├── [courses|categories|business|learningpaths|resources|enterprise|support|teams|about].html
│                             # Subpages stitched to the homepage nav
├── css/
│   └── styles.css            # Design system + responsive layout
├── js/
│   └── main.js               # Navigation, sliders, API-ready course insertion
├── server.py                 # Flask server + injection helpers
├── metadata.py               # Agenticverse-style metadata schema
├── entity.py                 # Entity wrapper that boots the server
└── README.md
```

## 🚀 Quick Start
1. **Install dependencies**
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install flask
   ```
2. **Run the replica**
   ```bash
   python server.py  # serves at http://localhost:5000
   ```
3. **Inject custom content (optional)**
   ```python
   from server import start_server
   start_server(content_data={
       "section": "courses",
       "title": "AI Product Strategist",
       "category": "AI",
       "instructor": "Ivy Hills",
       "price": "$12.99",
       "old_price": "$79.99",
       "rating": "4.9",
       "reviews": "(3,201)",
       "image_url": "https://images.unsplash.com/photo-1518779578993-ec3579fee39f?auto=format&fit=crop&w=400&q=60",
       "badge_text": "Featured",
   })
   ```
   Every item appended this way is rendered server-side at the `<!-- COURSE_INJECTION_POINT -->` marker inside `index.html` and also exposed through `GET /api/content` for client-side hydration.

## 🧩 Key Features
- **Pixel-faithful hero + page sections** mirroring the screenshot (announcement band, hero, category rail, testimonials, enterprise CTAs, footer, etc.).
- **Nine supplementary pages** (`courses.html`, `business.html`, etc.) that reuse the global shell for seamless navigation flows.
- **Responsive layout system** powered by CSS custom properties, modern grid/flex utilities, and motion states for scroll-triggered sections.
- **Dynamic course grid** with dual support:
  - Client-side hydration through `js/main.js` (mock data + `/api/content` fetch)
  - Server-side injection via `server.py` to guarantee SSR-friendly renders
- **API-ready metadata** defined in `metadata.py`, ensuring compatibility with Agenticverse or other orchestration layers.

## 🧪 Testing & Verification
- Validate layout locally on desktop + mobile breakpoints (Chrome DevTools responsive view).
- Hit `http://localhost:5000/api/content` to confirm injected payloads.
- Run `python server.py` while providing `content_data` to confirm SSR injection order.

## 📌 Known Notes
- External assets (logos + hero imagery) rely on public CDNs/Unsplash and require network access.
- No real Udemy APIs are called; data is mocked to keep the project self-contained yet API-ready.
- Tailwind is not used directly but the utility naming + spacing system mirrors Tailwind conventions for clarity.
