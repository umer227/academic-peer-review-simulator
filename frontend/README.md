# Frontend

React + Vite frontend for the peer review simulator.

## Run

```powershell
npm install
npm run dev
```

Set `VITE_API_BASE_URL` in a local `.env` file if your backend is not on `http://127.0.0.1:8000`.

## Deploy Frontend on Vercel

Create a separate Vercel project for the frontend.

- Root Directory: `frontend`
- Framework Preset: `Vite`
- Build Command: `npm run build`
- Output Directory: `dist`

Environment variable:

```env
VITE_API_BASE_URL=https://your-backend.vercel.app
```
