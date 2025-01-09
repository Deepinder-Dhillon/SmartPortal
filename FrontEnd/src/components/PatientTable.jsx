import React, { useState, useEffect } from "react";
import api from "../services/api";
import "../styles/PatientTable.css";
import { CreatePatientButton } from "./CreatePatientButton";
import DeleteButton from "./DeleteButton";
import { UpdatePatientButton } from "./UpdatePatientButton";

const PatientTable = ({ patients, refreshPatients, setCurrentPatient }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredPatients, setFilteredPatients] = useState(patients);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  useEffect(() => {
    setFilteredPatients(patients); 
  }, [patients]);

  const handleSearch = async () => {
    try {
      const response = await api.get(`/patients/search/?search=${searchTerm}`);
      setFilteredPatients(response.data.results);
      setCurrentPage(1); 
    } catch (error) {
      console.error("Error fetching search results:", error);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  const handleSelectPatient = async (patient) => {
    try {
      await api.post(`/patients/${patient.phn}/set-current/`);
      setSelectedPatient(patient);
      setCurrentPatient(patient); 
      refreshPatients(); 
    } catch (error) {
      console.error("Error setting current patient:", error);
    }
  };

  // Pagination logic
  const indexOfLastPatient = currentPage * itemsPerPage;
  const indexOfFirstPatient = indexOfLastPatient - itemsPerPage;
  const currentPatients = filteredPatients.slice(indexOfFirstPatient, indexOfLastPatient);

  const totalPages = Math.ceil(filteredPatients.length / itemsPerPage);

  const handleNext = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePrevious = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  return (
    <div className="patient-container">
      <div className="create-button">
        <CreatePatientButton refreshPatients={refreshPatients} />
      </div>

      <h2 className="section-title">Patients</h2>

      <div className="search-container">
        <input
          type="text"
          placeholder="Search by name"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyDown={handleKeyPress}
          className="search-input"
        />
      </div>

      <table className="patient-table">
        <thead>
          <tr>
            <th>PHN</th>
            <th>Name</th>
            <th>Date of Birth</th>
            <th>Address</th>
          </tr>
        </thead>
        <tbody>
          {currentPatients.map((patient) => (
            <tr
              key={patient.phn}
              className={selectedPatient && selectedPatient.phn === patient.phn ? "selected" : ""}
              onClick={() => handleSelectPatient(patient)}
            >
              <td>{patient.phn}</td>
              <td><strong>{patient.name}</strong></td>
              <td>{patient.birth_date}</td>
              <td>{patient.address}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="bottom-controls">
        <div className="left-controls">
          <UpdatePatientButton 
            selectedPatient={selectedPatient} 
            refreshPatients={refreshPatients} 
            disabled={!selectedPatient} 
          />
          <DeleteButton 
            selectedPhn={selectedPatient ? selectedPatient.phn : null} 
            refreshPatients={refreshPatients} 
            setCurrentPatient={setCurrentPatient} 
            setSelectedPatient={setSelectedPatient} 
            disabled={!selectedPatient} 
          />
        </div>

        <div className="pagination">
          <button 
            className="pagination-btn" 
            onClick={handlePrevious} 
            disabled={currentPage === 1}
          >
            Previous
          </button>
          <span>
            Page {currentPage} of {totalPages}
          </span>
          <button 
            className="pagination-btn" 
            onClick={handleNext} 
            disabled={currentPage === totalPages}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default PatientTable;
