import React, { useState, useEffect } from "react";
import api from "../services/api";
import '../styles/CurrentPatientCard.css';

export function CurrentPatientCard({ refreshPatients, currentPatient }) {
  return (
    <div className="patient-card">
      <h2 className="patient-card-title">Current Patient</h2>
      {currentPatient ? (
        <div className="patient-details">
          <p><strong>PHN:</strong> {currentPatient.phn}</p>
          <p><strong>Name:</strong> {currentPatient.name}</p>
          <p><strong>Date of Birth:</strong> {currentPatient.birth_date}</p>
          <p><strong>Address:</strong> {currentPatient.address}</p>
          <p><strong>Mobile:</strong> {currentPatient.phone}</p>
          <p><strong>Email:</strong> {currentPatient.email}</p>
        </div>
      ) : (
        <p>No current patient selected.</p>
      )}
    </div>
  );
}
