import React, { useState } from "react";
import WiktionaryEntryDetails from "./WiktionaryEntry";
import SutianLemmaDetails from "./SutianLemma";

function ResultTable({ results }) {
    const [visibleResults, setVisibleResults] = useState(20);

    const handleShowMore = () => {
        setVisibleResults((prev) => prev + 20);
    };

    return (
        <div>
            {results.length === 0 ? (
                <p>No results found matching your query</p>
            ) : (
                <>
                    <p>Number of results: {results.length}</p>
                    <table className='table'>
                        <thead>
                            <tr>
                                <th style={{width: `4%`}}>#</th>
                                <th style={{width: `20%`}}>Lemma</th>
                                <th style={{width: `38%`}}>Wiktionary Entry</th>
                                <th style={{width: `38%`}}>Sutian Entry</th>
                            </tr>
                        </thead>
                        <tbody>
                            {results.slice(0, visibleResults).map((result, index) => (
                                <tr key={index}>
                                    <td>{index + 1}</td>
                                    <td className='hant hant-lemma'>{result.lemma}</td>
                                    <td>
                                        <WiktionaryEntryDetails entry={result.wiktionary_entry} />
                                    </td>
                                    <td>
                                        <SutianLemmaDetails lemma={result.sutian_lemma} />
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    {visibleResults < results.length && (
                        <div className='show-more-row'
                            onClick={handleShowMore}
                            style={{ cursor: "pointer" }}
                        >
                            Show more results
                        </div>
                    )}
                </>
            )}
        </div>
    );
}

export default ResultTable;