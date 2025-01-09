"use client";

import { useState } from "react";
import api from "@/services/api"; 
import { Button } from "@/components/ui/button";

export function SetCurrentPatientButton({ selectedPatient, refreshPatients }) {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  async function handleSetCurrentPatient() {
    if (!selectedPatient) return;
    
    setLoading(true);
    setSuccess(false);
    setError(null);

    try {
      await api.post(`/patients/${selectedPatient.phn}/set-current/`);
      setSuccess(true);
      refreshPatients(); 
    } catch (err) {
      console.error("Error setting current patient:", err);
      setError(err.response?.data?.error || "Failed to set current patient.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col items-start space-y-2">
      <Button
        onClick={handleSetCurrentPatient}
        disabled={!selectedPatient || loading}
        className="bg-green-600 hover:bg-green-700 text-white"
      >
        {loading ? "Setting..." : "Set as Current"}
      </Button>
    </div>
  );
}
