// import logo from './logo.svg';
// import './App.css';
// import React, { useEffect, useState } from "react";
// import SearchBar from "./components/SearchBar";
// import SearchResults from "./components/SearchResults";
// import WiktionaryEntryDetails from './components/WiktionaryEntry';
// import { fetchHello } from './services/api';


// function App() {
//   const [message, setMessage] = useState("");
//   const [results, setResults] = useState([]);
//   const [details, setDetails] = useState(null);

//   useEffect(() => {
//     fetchHello()
//       .then((response) => setMessage(response.data.message))
//       .catch((error) => console.error("Error:", error));
//   }, []);

//   const handleSearch = async (query) => {
//     // Replace with actual search API logic
//     console.log("Searching for:", query);
//   };

//   return (
//     <div className="App">
//       <header className="Berlin Minnan Dictionary">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//       <main>x
//         <SearchBar onSearch={handleSearch} />
//         <section>
//           <input type="text" id="hokkien" placeholder="Input Hokkien search term..." />
//           <input type="text" id="english" placeholder="Input English search trem..." />
//           <input type="text" id="hanzi" placeholder="Input Chinese search term..." />
//           <input type="number" id="syllable_count" />
//         </section>
//         <section>
//           <h2>Search Results</h2>
//           {/* Placeholder for search results */}
//         </section>
//       </main>
//     </div>
//   );
// }

// export default App;


import React, { useState } from "react";
import SearchBar from "./components/SearchBar";
import { fetchWiktionaryEntries } from "./services/api";
// import WiktionaryEntryDetails from "./components/WiktionaryEntry";
import './App.css';
import ResultTable from "./components/ResultTable";

function App() {
  const [results, setResults] = useState([]);

  const handleSearch = async (searchParams) => {
    console.log("Calling API with params:", searchParams);
    try {
      const response = await fetchWiktionaryEntries(searchParams);
      setResults(response.data); // Assuming response data is a list of wiktionary entries
      console.log(results)
    } catch (error) {
      console.error("Error fetching wiktionary entries:", error);
    }
  };

  return (
    <div>
      <h1>Berlin Minnan Dictionary</h1>
      <SearchBar onSearch={handleSearch} />
      <div>
        <h3>Search Results</h3>
        <ResultTable results={results} />
        
      </div>
    </div>
  );
}

export default App;
