"use client";

import { useState } from "react";

import AlignmentForm from "./components/AlignmentForm";
import AlignmentResult from "./components/AlignmentResult";

import { AlignmentResult as AlignmentResultType } from "./lib/api";

export default function Home() {

  const [result, setResult] =
    useState<AlignmentResultType | null>(null);

  return (
    <main className="min-h-screen bg-gray-50 px-6 py-10">

      <div className="mx-auto max-w-6xl">

        <header className="mb-10">
          <h1 className="text-4xl font-bold">
            DNA Sequence Alignment
          </h1>

          <p className="mt-3 text-gray-600">
            Alinhamento global e local de duas
            sequências de DNA.
          </p>
        </header>

        <section className="rounded-xl bg-white p-6 shadow">
          <AlignmentForm
            onResult={setResult}
          />
        </section>

        {result && (
          <section className="mt-10">
            <AlignmentResult result={result} />
          </section>
        )}

      </div>

    </main>
  );
}