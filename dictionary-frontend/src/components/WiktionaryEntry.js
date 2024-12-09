import React from "react";

function WiktionaryEntryDetails({ entry }) {
  if (!entry) {
    return <p>No entry details available.</p>;
  }

  const { word, pos, etymology, glosses, raw_glosses, pronunciations, sutian_lemma } = entry;

  return (
    <div>
        <p><b>POS: </b>{pos}</p>

        {/* Give out `Hokkien-TL` and `Mandarin`, if these keys are available */}
        {Object.entries(pronunciations).map(([lang, pronunciations], index) => (
            (lang === 'Hokkien-TL' || lang === 'Mandarin') ? (
                <p><b>{lang}: </b><span className='romanization'>{pronunciations.join(", ")}</span></p>
            ) : null
        ))}

        {/* {pronunciations && Object.keys(pronunciations).length > 0 && (
            <div>
            <strong>Pronunciations:</strong>
            <ul>                
                {Object.entries(pronunciations).map(([lang, pronunciations], index) => (
                <li key={index}>
                    {lang}: <p className='romanization'>{pronunciations.join(", ")}</p>
                </li>
                ))}
            </ul>
            </div>
        )} */}
        
        {etymology && <p><strong>Etymology:</strong> {etymology}</p>}

        {glosses && glosses.length > 0 && (
            <div>
            <strong>Glosses:</strong>
            <ul>
                {glosses.map((gloss, index) => (
                <li key={index}>{gloss}</li>
                ))}
            </ul>
            </div>
        )}

        {raw_glosses && raw_glosses.length > 0 && (
            <div>
            <strong>Raw Glosses:</strong>
            <ul>
                {raw_glosses.map((rawGloss, index) => (
                <li key={index}>{rawGloss}</li>
                ))}
            </ul>
            </div>
        )}
    </div>
  );
}

export default WiktionaryEntryDetails;
