// import axios from "axios";

// const API_BASE_URL = "http://localhost:5000/api";

// export const fetchHello = () => axios.get(`${API_BASE_URL}/hello`);

// export async function searchCharacters(query) {
//   const response = await fetch(`${API_BASE_URL}/search?hanzi=${query}`);
//   return response.json();
// }

import axios from "axios";

// Use relative URL in production, localhost in development
const API_BASE_URL = process.env.REACT_APP_API_URL || "/api";

export const fetchWiktionaryEntries = (params) => {
    return axios.post(`${API_BASE_URL}/search`, params);
};