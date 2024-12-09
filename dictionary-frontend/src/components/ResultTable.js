import React from "react";
import WiktionaryEntryDetails from "./WiktionaryEntry";
import SutianLemmaDetails from "./SutianLemma";

function ResultTable({ results }) {
    return (
        <table className='table' style={{ padding: "10px", marginBottom: "10px" }}>
        <thead>
            <tr>
                <th style={{width: `20%`}}>Lemma</th>
                <th style={{width: `40%`}}>Wiktionary Entry</th>
                <th style={{width: `40%`}}>Sutian Entry</th>
            </tr>
        </thead>
        <tbody>
            {results.map((result, index) => (
            <tr key={index}>
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
    );
}

export default ResultTable;