import React, { useState, useEffect } from "react";
import SearchBar from "./components/SearchBar";
import { fetchWiktionaryEntries } from "./services/api";
// import WiktionaryEntryDetails from "./components/WiktionaryEntry";
import './App.css';
import ResultTable from "./components/ResultTable";

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingDots, setLoadingDots] = useState("");

  const handleSearch = async (searchParams) => {
    console.log("Calling API with params:", searchParams);
    setLoading(true);
    try {
      const response = await fetchWiktionaryEntries(searchParams);
      setResults(response.data); // Assuming response data is a list of wiktionary entries
      console.log(results);
    } catch (error) {
      console.error("Error fetching wiktionary entries:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const searchParams = {
      hokkien: params.get("hokkien") || "",
      english: params.get("english") || "",
      hanzi: params.get("hanzi") || "",
      syllable_count: params.get("syllable_count") || "",
    };
    if (Object.values(searchParams).some((param) => param !== "")) {
      handleSearch(searchParams);
    }
  }, []);

  useEffect(() => {
    if (loading) {
      const interval = setInterval(() => {
        setLoadingDots((prev) => (prev.length < 5 ? prev + "." : ""));
      }, 1000);
      return () => clearInterval(interval);
    } else {
      setLoadingDots("");
    }
  }, [loading]);

  return (
    <div>
      <h1>Berlin Minnan Dictionary</h1>
      <SearchBar onSearch={handleSearch} />
      <div>
        <h3>Search Results</h3>
        {loading ? (
          <p>Querying database{loadingDots}</p>
        ) : (
          <ResultTable results={results} />
        )}
      </div>
    </div>
  );
}

export default App;
