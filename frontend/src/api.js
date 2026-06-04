const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with ${response.status}`);
  }

  return response.json();
}

export function submitPaper(payload) {
  return request("/api/review-paper", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function fetchReviews() {
  return request("/api/reviews");
}

export function fetchReview(paperId) {
  return request(`/api/reviews/${paperId}`);
}

export function fetchHealth() {
  return request("/health");
}
