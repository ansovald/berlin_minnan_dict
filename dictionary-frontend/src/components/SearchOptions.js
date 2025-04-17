import React from "react";

function SearchOptions({ helpVisible }) {
    return (
        <div
            className={`help-text general-help-text ${helpVisible ? "visible" : "hidden"}`}
            id='general-help-text'
        >
            <p>Search Options:</p>
            <p>For the fields &quot;Hokkien&quot; and &quot;English&quot;, tick the <i>case sensitive</i> box to distinguish upper- and lowercase letters.</p>
            <p>Search terms are treated as full words in &quot;English&quot;, and as syllables in &quot;Hokkien&quot;. For example, <code>word</code> matches <match>word</match>, but not <match>words</match>. &quot;Hanzi&quot; search also matches partial lemmas.</p>
            <ul>
                <li><p><code>*</code> matches any number of arbitrary characters. For example, <code>word*</code> matches <match>word</match>, but also <match>words</match> etc.</p></li>
                <li><p><code>.</code> matches exactly one arbitary character. For example, <code>紅.</code> matches <match>紅毛</match>, <match>紅茶</match>, 粉<match>紅色</match> etc., but not <match>紅</match></p></li>
                <li><code>?</code> means the preceding character is optional. For example, <code>tsh?inn</code> matches <match>tshinn</match> and <match>tsinn</match>.</li>
            </ul>
            <p>Advanced use case: if the search term is enclosed in <code>/</code>, you can enter <a href="https://cheatography.com/davechild/cheat-sheets/regular-expressions/">regular expressions</a>.</p>
            <p>For feature requests, bug reports, comments, and feedback please open an issue on <a href="https://github.com/ansovald/berlin_minnan_dict/issues">GitHub</a> or write me a <a href="mailto:osswaldk@hu-berlin.de">mail</a>.</p>
        </div>
    );
}

export default SearchOptions;
