# Research website

React + TypeScript, built with Vite. This is a local starter, not a deployed website. TypeScript strict mode is enabled. The starter links sources and marks episode findings pending; it does not contain invented analytical results.

Use root commands: `npm install`, `npm run dev`, `npm run check`, `npm run build`, `npm run preview`.

Reviewed public research artifacts live in `data/published/`. Root dev/build commands sync JSON/CSV files into generated `public/research/`. Other data directories and all Python code remain outside the website's public assets. Never put credentials, raw observations or unreviewed results in `public/`.

Add episode visualizations under `src/features/` when actual research outputs are available. Keep shared UI under `src/components/` once multiple pages require it. The initial scope does not require a backend or database.
