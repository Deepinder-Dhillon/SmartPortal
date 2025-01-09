import React, { useState, useEffect } from "react";
import Header from "../components/header";
import PatientTable from "../components/PatientTable";
import { CurrentPatientCard } from "../components/CurrentPatientCard";
import api from "../services/api";
import "../styles/Home.css";

const Home = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [currentPatient, setCurrentPatient] = useState(null);

  const fetchPatients = async () => {
    setLoading(true);
    try {
      const response = await api.get("/patients/search/");
      setPatients(response.data.results);
      setError(""); 
    } catch (err) {
      setError("Failed to load patients.");
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  return (
    <>
      <Header />
      <div className="home-container">
        <div className="dashboard">
          <div className="patient-table-container">
            <PatientTable 
              patients={patients} 
              refreshPatients={fetchPatients} 
              setCurrentPatient={setCurrentPatient} 
            />
          </div>
          <div className="current-patient-card">
            <CurrentPatientCard 
              refreshPatients={fetchPatients} 
              currentPatient={currentPatient} 
            />
          </div>
        </div>
        {error && <p className="text-red-500 text-sm">{error}</p>}
      </div>
    </>
  );
};

export default Home;
