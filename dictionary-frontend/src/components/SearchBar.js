import React, { useState, useEffect } from "react";

function SearchBar({ onSearch, initialSearchParams }) {
  const [searchParams, setSearchParams] = useState({
    hokkien: "",
    english: "",
    hanzi: "",
    syllable_count: "",
    case_insensitive: true, // Default to true
    ...initialSearchParams, // Initialize with values from props
  });

  useEffect(() => {
    setSearchParams((prev) => ({ ...prev, ...initialSearchParams })); // Update fields when props change
  }, [initialSearchParams]);

  const handleInputChange = (event) => {
    const { name, value, type, checked } = event.target;
    setSearchParams({
      ...searchParams,
      [name]: type === "checkbox" ? checked : value, // Handle checkbox changes
    });
  };

  const handleSearch = () => {
    const queryParams = new URLSearchParams();
    for (const key in searchParams) {
      if (searchParams[key]) {
        queryParams.append(key, searchParams[key]);
      }
    }
    window.history.pushState(null, "", `?${queryParams.toString()}`);
    onSearch(searchParams);
  };

  const handleClear = () => {
    setSearchParams({
      hokkien: "",
      english: "",
      hanzi: "",
      syllable_count: "",
      case_insensitive: true, // Reset to true
    });
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      event.preventDefault(); // Prevent form submission or page reload
      handleSearch();
    }
  };

  return (
    <form onSubmit={(e) => e.preventDefault()}>
      <div className='search-bar'>
        <div className='search-bar-item'>
          <div><label htmlFor="hokkien">Hokkien:</label></div>
          <input
            className='text-input'
            id="hokkien"
            type="text"
            name="hokkien"
            value={searchParams.hokkien}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
          />
        </div>
        <div className='search-bar-item'>
          <div><label htmlFor="english">English:</label></div>
          <input
            className='text-input'
            id="english"
            type="text"
            name="english"
            value={searchParams.english}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
          />
          <div>
            <label className="checkbox-label">
              <input
                className="checkbox"
                type="checkbox"
                name="case_insensitive"
                checked={searchParams.case_insensitive}
                onChange={handleInputChange}
              />
              Case insensitive search
            </label>
          </div>
        </div>
        <div className='search-bar-item'>
          <div><label htmlFor="hanzi">Hanzi:</label></div>
          <input
            className='text-input'
            id="hanzi"
            type="text"
            name="hanzi"
            value={searchParams.hanzi}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
          />
        </div>
        <div className='search-bar-item'>
          <div><label htmlFor="syllable_count">Syllable Count:</label></div>
          <input
            className='text-input'
            id="syllable_count"
            type="text"
            name="syllable_count"
            value={searchParams.syllable_count}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
          />
        </div>
      </div>
      <div className='search-bar-item search-bar-buttons'>
          <button type="button" onClick={handleSearch}>Search</button>
          <button type="button" onClick={handleClear}>Clear all</button>
      </div>
    </form>
  );
}

export default SearchBar;
