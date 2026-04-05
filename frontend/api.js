const BASE_URL = "http://localhost:8000";
const TOKEN = "securetoken";

// Public endpoints
async function getFacilities() {
  const res = await fetch(`${BASE_URL}/facilities`, {
    headers: {
      "Authorization": `Bearer ${TOKEN}`
    }
  });
  return res.json();
}

async function getTransport() {
  const res = await fetch(`${BASE_URL}/transport`);
  return res.json();
}

// Protected endpoints
async function getClubs() {
  const res = await fetch(`${BASE_URL}/clubs`, {
    headers: {
      "Authorization": `Bearer ${TOKEN}`
    }
  });
  return res.json();
}

async function getEvents() {
  const res = await fetch(`${BASE_URL}/events`, {
    headers: {
      "Authorization": `Bearer ${TOKEN}`
    }
  });
  return res.json();
}

async function getSecureData() {
  const res = await fetch(`${BASE_URL}/secure-data`, {
    headers: {
      "Authorization": `Bearer ${TOKEN}`
    }
  });
  return res.json();
}

window.api = {
  getFacilities,
  getTransport,
  getClubs,
  getEvents,
  getSecureData
};
