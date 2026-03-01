import React from "react";

function Footer({ onImpressumClick }) {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-content">
        <p>&copy; 2025-{currentYear} Karl Osswald • <span className="impressum-link" onClick={onImpressumClick}>Impressum</span></p>
      </div>
    </footer>
  );
}

export default Footer;
