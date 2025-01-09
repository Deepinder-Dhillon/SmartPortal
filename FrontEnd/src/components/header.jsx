import React from "react";
import "../styles/Header.css";
import Button from "./Button"; 

const Header = () => {
  return (
    <header className="header">
      <div className="header-left">
        <span className="title">Smart Portal</span>
      </div>
      <nav className="nav">
        <a href="/">Home</a>
      </nav>
      <div className="header-right">
    
        <Button text="Logout" onClick={() => window.location.href = "http://127.0.0.1:5173/logout"} className="logout-btn" />
      </div>
    </header>
  );
};

export default Header;

