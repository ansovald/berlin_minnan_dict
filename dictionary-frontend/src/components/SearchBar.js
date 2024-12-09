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
    onSearch(searchParams);
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
                <div><label for={`hokkien`}>Hokkien:</label></div>
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
                <div><label for={`english`}>English:</label></div>
                <input
                    className='text-input'
                    type="text"
                    name="english"
                    value={searchParams.english}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyDown}
                />
            </div>
            <div className='grid-item'>
                <div><label for={`hanzi`}>Hanzi:</label></div>
                <input
                    className='text-input'
                    type="text"
                    name="hanzi"
                    value={searchParams.hanzi}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyDown}
                />
            </div>
            <div className='grid-item'>
                <div><label for={`syllable_count`}>Syllable Count:</label></div>
                <input
                    className='text-input'
                    type="text"
                    name="syllable_count"
                    value={searchParams.syllable_count}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyDown}
                />
            </div>
        </div>
        <button onClick={handleSearch}>Search</button>
    </form>
  );
}

export default SearchBar;
