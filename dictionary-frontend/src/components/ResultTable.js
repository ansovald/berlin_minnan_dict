import React from "react";
import WiktionaryEntryDetails from "./WiktionaryEntry";
import SutianLemmaDetails from "./SutianLemma";
import SearchOptions from "./SearchOptions";

function ResultTable({ results, fetchMoreResults, hasMoreResults, helpVisible }) {
    return (
        <div>
            <SearchOptions helpVisible={helpVisible} />
            {results.length === 0 ? (
                <p>No results found matching your query</p>
            ) : (
                <>
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
                            {results.map((result, index) => (
                                <tr key={index}>
                                    <td>{index + 1}</td>
                                    <td className='hant hant-lemma' dangerouslySetInnerHTML={{ __html: result.lemma.replace(/\*\*\*(.*?)\*\*\*/g, '<match>$1</match>') }}></td>
                                    <td>
                                        <WiktionaryEntryDetails entry={result.wiktionary_entry} />
                                    </td>
                                    <td>
                                        <SutianLemmaDetails lemma={result.sutian_lemma} />
                                    </td>
                                </tr>
                            ))}
                            {hasMoreResults && (
                                <tr onClick={fetchMoreResults} style={{ cursor: "pointer", textAlign: "center" }}>
                                    <td colSpan="4">Show more results</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </>
            )}
        </div>
    );
}

export default ResultTable;