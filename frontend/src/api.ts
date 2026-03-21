const BASE = "http://127.0.0.1:8000/api";

export async function fetchCompanies() {
  const res = await fetch(`${BASE}/companies`);
  return res.json();
}

export async function fetchCompany(ticker: string) {
  const res = await fetch(`${BASE}/companies/${ticker}`);
  return res.json();
}

export async function fetchPredictions() {
  const res = await fetch(`${BASE}/predictions`);
  return res.json();
}

export async function fetchStats() {
  const res = await fetch(`${BASE}/stats`);
  return res.json();
}
