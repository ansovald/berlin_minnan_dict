import React from "react";

function SearchOptions({ helpVisible }) {
    return (
        <div
            className={`help-text general-help-text ${helpVisible ? "visible" : "hidden"}`}
            id='general-help-text'
        >
            <p>Search Options:</p>
            <p>For the fields &quot;Hokkien&quot; and &quot;English&quot;, tick the <i>case sensitive</i> box to distinguish upper- and lowercase letters.</p>
            <p>Search terms are treated as full words in English, and as syllables in Hokkien. For example, <code>word</code> matches <match>word</match>, but not <match>words</match>.</p>
            <p><code>*</code> matches any number of arbitrary characters. For example, <code>word*</code> matches <match>word</match>, but also <match>words</match> etc.</p>
            <p><code>.</code> matches exactly one arbitary character. For example, <code>紅.</code> matches <match>紅毛</match>, <match>紅茶</match>, etc., but not <match>紅</match></p>
            <p>When combining &quot;Hanzi&quot; search with &quot;Syllable Count&quot;, make sure to </p>
            <p>All search fields (except for `Syllable Count`) accept Regular Expressions. These are mainly useful for &quot;Hokkien&quot; and &quot;Hanzi&quot; search fields:</p>
            <ul>
                <li><code>^</code> marks the beginning and <code>$</code> the end of a string:
                    <ul>
                        <li><code>^紅</code> in search field &quot;Hanzi&quot; matches <match>紅</match>, <match>紅毛</match>, <match>紅茶</match>; etc., but <b>not</b> <match>粉紅</match>.</li>
                        <li><code>n$</code> in search field Hokkien matches all Hokkien words ending with &quot;n&quot; in Tâi-lô romanization, e.g. <match>khián</match>, <match>Hok-kiàn</match>, etc.</li>
                    </ul>
                </li>
                <li><code>.</code> matches exactly one (arbitrary) character. For example, <code>^.毛</code> matches <match>紅毛</match>, <match>紅毛人</match>, <match>羽毛</match> etc., but not <match>毛</match>, <match>毛病</match>, etc.</li>
                <li><code>?</code> means the preceding character is optional. For example, <code>^tsh?in</code> matches <match>tshinn</match>, but also <match>tsîng</match>, <match>tsinn</match>, etc.</li>
                <li><code>*</code></li>
            </ul>
            <p>Advanced use case: if the search term is enclosed in <code>/</code>, you can enter <a href="https://cheatography.com/davechild/cheat-sheets/regular-expressions/">regular expressions</a>.</p>
        </div>
    );
}

export default SearchOptions;
