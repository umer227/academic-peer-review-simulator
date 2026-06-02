import { useEffect, useState } from "react";

import api from "../api/client.js";

export default function Home() {
  const [health, setHealth] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/health")
      .then((response) => {
        setHealth(response.data);
        setError("");
      })
      .catch(() => {
        setError("Backend is not reachable yet.");
      });
  }, []);

  return (
    <main className="min-h-screen bg-paper text-ink">
      <section className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-6 py-8">
        <header className="flex items-center justify-between border-b border-slate-300 pb-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-thesis">
              University Demo MVP
            </p>
            <h1 className="mt-2 text-3xl font-bold text-oxford md:text-4xl">
              Multi-Agent Academic Peer Review Simulator
            </h1>
          </div>
          <div className="hidden rounded border border-slate-300 bg-white px-4 py-2 text-sm text-thesis shadow-sm md:block">
            5-Day Scaffold
          </div>
        </header>

        <div className="grid flex-1 gap-8 py-10 lg:grid-cols-[1.2fr_0.8fr]">
          <section className="flex flex-col justify-center">
            <p className="max-w-2xl text-lg leading-8 text-slate-700">
              A lightweight academic review workspace for demonstrating how
              simulated reviewers could evaluate a research paper, compare
              feedback, and support an editor decision.
            </p>

            <div className="mt-8 grid gap-4 sm:grid-cols-3">
              {["Paper Intake", "Reviewer Roles", "Editor Summary"].map((item) => (
                <div key={item} className="rounded border border-slate-300 bg-white p-4 shadow-sm">
                  <h2 className="text-base font-semibold text-oxford">{item}</h2>
                  <p className="mt-2 text-sm leading-6 text-thesis">Coming soon</p>
                </div>
              ))}
            </div>
          </section>

          <aside className="self-center rounded border border-slate-300 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-oxford">System Status</h2>
            <div className="mt-4 rounded bg-slate-50 p-4 text-sm">
              {health && (
                <dl className="space-y-3">
                  <div>
                    <dt className="font-medium text-thesis">Backend</dt>
                    <dd className="mt-1 text-green-700">{health.status}</dd>
                  </div>
                  <div>
                    <dt className="font-medium text-thesis">Service</dt>
                    <dd className="mt-1 text-slate-700">{health.service}</dd>
                  </div>
                  <div>
                    <dt className="font-medium text-thesis">Environment</dt>
                    <dd className="mt-1 text-slate-700">{health.environment}</dd>
                  </div>
                </dl>
              )}
              {!health && !error && <p className="text-thesis">Checking backend...</p>}
              {error && <p className="text-red-700">{error}</p>}
            </div>
          </aside>
        </div>
      </section>
    </main>
  );
}
