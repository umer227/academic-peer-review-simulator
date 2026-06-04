const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    });
  } catch {
    throw new Error(
      `Cannot reach the backend API at ${API_BASE_URL}. Check that the backend is running or set VITE_API_BASE_URL to your deployed backend URL.`,
    );
  }

  if (!response.ok) {
    let message = "";
    try {
      const data = await response.json();
      message = data.detail || data.message || JSON.stringify(data);
    } catch {
      message = await response.text();
    }
    throw new Error(message || `Backend request failed with status ${response.status}`);
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
