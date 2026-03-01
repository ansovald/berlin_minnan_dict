import React from "react";

function Footer({ onImpressumClick }) {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-content">
        <p>&copy; 2025-{currentYear} Karl Osswald. All rights reserved.</p>
        <button onClick={onImpressumClick} className="impressum-link">
          Impressum
        </button>
      </div>
    </footer>
  );
}

export default Footer;
