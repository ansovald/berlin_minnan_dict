import React from "react";

function SearchResults({ results, onSelect }) {
  return (
    <ul>
      {results.map((item) => (
        <li key={item.id} onClick={() => onSelect(item.id)}>
          {item.hant} ({item.romanization})
        </li>
      ))}
    </ul>
  );
}

export default SearchResults;