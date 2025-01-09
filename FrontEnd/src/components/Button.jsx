import React from "react";
import "../styles/Button.css";

const Button = ({ text, onClick, className = "btn", disabled = false }) => {
  return (
    <button className={className} onClick={onClick} disabled={disabled}>
      {text}
    </button>
  );
};

export default Button;
