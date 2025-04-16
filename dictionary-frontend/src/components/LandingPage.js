import React, { useState } from "react";
import './LandingPage.css'; // Optional: Add styles for the landing page

function LandingPage({ onAuthenticate }) {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    const correctPassword = process.env.REACT_APP_CORRECT_PASSWORD;
    if (password === correctPassword) {
      onAuthenticate(); // Notify parent component of successful authentication
    } else {
      setError("Incorrect password. Please try again.");
    }
  };

  return (
    <div className="landing-page">
      <h1>Welcome to Berlin Minnan Dictionary</h1>
      <p>This dictionary is still in the alpha testing phase. Please enter password to continue.</p>
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          placeholder="Enter password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Enter</button>
      </form>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
}

export default LandingPage;
