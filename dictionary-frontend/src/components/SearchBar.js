import React, { useState } from "react";

function SearchBar({ onSearch }) {
  const [searchParams, setSearchParams] = useState({
    hokkien: "",
    english: "",
    hanzi: "",
    syllable_count: "",
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setSearchParams({ ...searchParams, [name]: value });
  };

  const handleSearch = () => {
    const queryParams = new URLSearchParams(searchParams).toString();
    window.history.pushState(null, "", `?${queryParams}`);
    onSearch(searchParams);
  };

  const handleClear = () => {
    setSearchParams({
      hokkien: "",
      english: "",
      hanzi: "",
      syllable_count: "",
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
      <div className='grid'>
        <div className='grid-item'>
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
        <div className='grid-item'>
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
        </div>
        <div className='grid-item'>
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
        <div className='grid-item'>
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
      <div className='grid-item'>
          <button type="button" onClick={handleSearch}>Search</button>
          <button type="button" onClick={handleClear}>Clear all</button>
      </div>
    </form>
  );
}

export default SearchBar;
