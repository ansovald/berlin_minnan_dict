import React, { useState, useEffect } from "react";

function Impressum({ onClose }) {
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch the impressum config from the external file
    fetch(`${process.env.PUBLIC_URL}/impressum-config.json`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load impressum configuration");
        }
        return response.json();
      })
      .then((data) => {
        setConfig(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error loading impressum config:", err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="impressum-overlay" onClick={onClose}>
      <div className="impressum-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>
          ×
        </button>
        <h1>Impressum</h1>
        <div className="impressum-body">
          {loading ? (
            <p>Loading...</p>
          ) : error ? (
            <p>Error loading impressum information: {error}</p>
          ) : config ? (
            <>
              <h2>Information according to §5 DDG und §10 Abs. 3 MDStV</h2>
              <p>
                <strong>{config.title}</strong>
              </p>
              <p>
                {config.name}<br />
                {config.organization}<br />
                {config.department1}<br />
                {config.department2}<br />
                {config.department3}<br />
                {config.street}<br />
                {config.postalCode}<br />
              </p>

              <h2>Contact</h2>
              <p>
                E-Mail: {config.email}<br />
              </p>

              <h2>Responsible for content</h2>
              <p>
                {config.name}<br />
                <i>Contact details as above</i>
              </p>

              <h2>Disclaimer</h2>
              <h3>Liability for Content</h3>
              <p>
                The contents of our pages were created with the greatest care. However, we cannot guarantee the contents' accuracy, completeness, or topicality. According to statutory provisions, we are furthermore responsible for our own content on these web pages. In this matter, please note that we are not obliged to monitor the transmitted or saved information of third parties, or investigate circumstances pointing to illegal activity.
              </p>

              <h3>Liability for Links</h3>
              <p>
                Our offer contains links to external third-party websites. We have no influence on the contents of those websites, therefore we cannot guarantee for those contents. Providers or administrators of linked websites are always responsible for their own contents.
              </p>

              <h3>Copyright</h3>
              <p>
                The content and works published on this website are governed by the copyright laws of Germany. Any duplication, processing, distribution, or any form of commercialization of such material beyond the scope of the copyright law shall require the prior written consent of its respective author or creator.
              </p>
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
}

export default Impressum;
