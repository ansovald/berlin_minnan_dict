import React, { useState, useEffect } from "react";
import SearchBar from "./components/SearchBar";
import { fetchWiktionaryEntries } from "./services/api";
import './App.css';
import ResultTable from "./components/ResultTable";

function App() {
  const [results, setResults] = useState([]);
  const [lastEntryId, setLastEntryId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingDots, setLoadingDots] = useState("");
  const [searchParams, setSearchParams] = useState({});
  const [showBackToTop, setShowBackToTop] = useState(false); // State for "Back to top" button visibility

  const handleSearch = async (searchParams) => {
    console.log("Calling API with params:", searchParams);
    setSearchParams(searchParams); // Save the current search parameters
    setLoading(true);
    try {
      const response = await fetchWiktionaryEntries(searchParams);
      setResults(response.data.results); // Assuming response data contains results and last_entry_id
      setLastEntryId(response.data.last_entry_id);
    } catch (error) {
      console.error("Error fetching wiktionary entries:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchMoreResults = async () => {
    if (!lastEntryId || loading) return;
    setLoading(true);
    try {
      const response = await fetchWiktionaryEntries({ ...searchParams, last_entry_id: lastEntryId });
      setResults((prevResults) => [...prevResults, ...response.data.results]); // Append new results
      setLastEntryId(response.data.last_entry_id); // Update lastEntryId for next fetch
    } catch (error) {
      console.error("Error fetching more results:", error);
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
      case_insensitive: params.has("case_insensitive") ? params.get("case_insensitive") === "true" : true, // Default to true
    };
    setSearchParams(searchParams); // Update state with URL parameters

    // Trigger search only if at least one parameter other than case_insensitive is not empty
    const hasSearchableParams = Object.entries(searchParams).some(
      ([key, value]) => key !== "case_insensitive" && value !== ""
    );
    if (hasSearchableParams) {
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

  // Add scroll event listener to toggle "Back to top" button visibility
  useEffect(() => {
    const handleScroll = () => {
      setShowBackToTop(window.scrollY > 200); // Show button if scrolled down 200px
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" }); // Smooth scroll to top
  };

  return (
    <div>
      <div className="header-bar">
        <img src={`${process.env.PUBLIC_URL}/logo.svg`} alt="Logo" className="header-logo" /> {/* Reference logo from %PUBLIC_URL% */}
        <div className="header-content">
          <h1>Berlin Minnan Dictionary</h1>
          <SearchBar onSearch={handleSearch} initialSearchParams={searchParams} />
        </div>
        <img src={`${process.env.PUBLIC_URL}/placeholder.svg`} className="header-logo" /> {/* Reference logo from %PUBLIC_URL% */}
      </div>
      <div className="content-container">
        {loading && results.length === 0 ? (
          <p>Querying database{loadingDots}</p>
        ) : (
          <ResultTable
            results={results}
            fetchMoreResults={fetchMoreResults}
            hasMoreResults={!!lastEntryId} // Show "Show more results" only if there are more results
          />
        )}
      </div>
      {showBackToTop && ( // Conditionally render "Back to top" button
        <button
          onClick={scrollToTop}
          className="back-to-top"
        >
          Back to top
        </button>
      )}
    </div>
  );
}

export default App;
