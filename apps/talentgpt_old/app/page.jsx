import Link from "next/link";

export default function Page() {
  return (
    <main style={{padding:24}}>
      <h1>TalentGPT</h1>
      <p>Assistente de talentos da MindScan (MVP).</p>
      <ul>
        <li><Link href="/ping">Healthcheck da API</Link></li>
      </ul>
    </main>
  );
}




