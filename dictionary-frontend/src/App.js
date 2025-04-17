import React, { useState, useEffect } from "react";
import SearchBar from "./components/SearchBar";
import { fetchWiktionaryEntries } from "./services/api";
import './App.css';
import ResultTable from "./components/ResultTable";
import LandingPage from "./components/LandingPage"; // Import the new LandingPage component

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false); // State to track authentication
  const [results, setResults] = useState([]);
  const [lastEntryId, setLastEntryId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingDots, setLoadingDots] = useState("");
  const [searchParams, setSearchParams] = useState({});
  const [showBackToTop, setShowBackToTop] = useState(false); // State for "Back to top" button visibility
  const [helpVisible, setHelpVisible] = useState(false); // State to track help visibility

  const toggleHelp = () => {
    setHelpVisible((prev) => !prev); // Toggle help visibility
  };

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
    const updateSearchParamsFromURL = () => {
      const params = new URLSearchParams(window.location.search);
      const searchParams = {
        hokkien: params.get("hokkien") || "",
        english: params.get("english") || "",
        hanzi: params.get("hanzi") || "",
        syllable_count: params.get("syllable_count") || "",
        case_sensitive_en: params.has("case_sensitive_en") ? params.get("case_sensitive_en") === "false" : false, // Default to true
        case_sensitive_nan: params.has("case_sensitive_nan") ? params.get("case_sensitive_nan") === "false" : false, // Default to true
      };
      setSearchParams(searchParams); // Update state with URL parameters

      // Trigger search only if at least one parameter, other than case_sensitive_en and case_sensitive_nan, is not empty
      const hasSearchableParams = Object.entries(searchParams).some(
        ([key, value]) => key !== "case_sensitive_en" && key !== "case_sensitive_nan" && value.trim() !== ""
      );
      if (hasSearchableParams) {
        handleSearch(searchParams);
      }
    };

    // Initial load
    updateSearchParamsFromURL();

    // Listen for browser history changes
    const handlePopState = () => {
      updateSearchParamsFromURL();
    };
    window.addEventListener("popstate", handlePopState);

    return () => {
      window.removeEventListener("popstate", handlePopState);
    };
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

  if (!isAuthenticated) {
    return <LandingPage onAuthenticate={() => setIsAuthenticated(true)} />; // Render LandingPage if not authenticated
  }

  return (
    <div>
      <div className="header-bar">
        <img src={`${process.env.PUBLIC_URL}/logo.svg`} alt="Logo" className="header-logo" /> {/* Reference logo from %PUBLIC_URL% */}
        <div className="header-content">
          <h1>Berlin Minnan Dictionary</h1>
          <SearchBar
            onSearch={handleSearch}
            initialSearchParams={searchParams}
            helpVisible={helpVisible} // Pass helpVisible state
            toggleHelp={toggleHelp} // Pass toggleHelp function
          />
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
            helpVisible={helpVisible} // Pass helpVisible state
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
