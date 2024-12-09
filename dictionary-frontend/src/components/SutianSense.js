import React from "react";

function SutianSenseDetails({ sense, index }) {
    if (!sense) {
        return <p>No sense details available.</p>;
    }

    const { lexical_category, explanation } = sense;

    return (
        <li key={index}>
            <p><strong>{lexical_category}: </strong>{explanation}</p>
        </li>
    );
}

export default SutianSenseDetails;