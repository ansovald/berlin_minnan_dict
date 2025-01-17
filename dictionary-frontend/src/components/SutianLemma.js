import React from "react";
import SutianSenseDetails from "./SutianSense";

function SutianLemmaDetails({ lemma }) {
  if (!lemma) {
    return <p>Word not found in Sutian Dictionary.</p>;
  }

  const { 
    romanization, 
    common_variant_pronunciations, 
    other_variant_pronunciations, 
    variant_writings, 
    audio_file, 
    classification,
    senses 
} = lemma;

  return (
    <div>
        <h3>Sutian Lemma</h3>
        {variant_writings && variant_writings.length > 0 && (
            <><p>Variant Writings: <span className='hant'>{variant_writings.join(", ")}</span></p></>
        )}
        <strong className='romanization'>{romanization}</strong>
        {common_variant_pronunciations && Object.keys(common_variant_pronunciations).length > 0 && (
            <><p>Common Variant: <span className='romanization'>{common_variant_pronunciations.join(", ")}</span></p></>
        )
        }
        {other_variant_pronunciations && Object.keys(other_variant_pronunciations).length > 0 && (
            <><p>Other Variants: <span className='romanization'>{other_variant_pronunciations.join(", ")}</span></p></>
        )
        }
        {audio_file && <div><audio controls src={audio_file} /></div>}
        {classification && <p><strong>Classification:</strong> {classification}</p>}
        {senses && senses.length > 0 ? (
                <div>
                    <strong>Senses:</strong>
                    <ol>
                        {senses.map((sense, index) => (
                            <SutianSenseDetails sense={sense} index={index} key={index} />
                        ))}
                    </ol>
                </div>
            ) : (
                <p>（單字不成詞者 ，無義項）</p>
        )}
    </div>
  )
}

export default SutianLemmaDetails;