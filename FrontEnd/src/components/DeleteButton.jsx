import { Button } from "./ui/button";
import api from "../services/api";
import React, { useState } from "react";
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from "./ui/dialog";

const DeleteButton = ({ selectedPhn, refreshPatients, setCurrentPatient, setSelectedPatient }) => {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleDelete = async () => {
    if (!selectedPhn) return;

    setLoading(true);
    try {
      await api.delete(`/patients/${selectedPhn}/delete/`);
      refreshPatients(); 
      setCurrentPatient(null); 
      setSelectedPatient(null); 
      setOpen(false);
    } catch (error) {
      console.error("Error deleting patient:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Button 
        className="bg-destructive text-destructive-foreground"
        onClick={() => setOpen(true)} 
        disabled={!selectedPhn || loading} 
      >
        Delete Patient
      </Button>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Confirm Deletion</DialogTitle>
          </DialogHeader>
          <p>Are you sure you want to delete this patient?</p>

          <DialogFooter>
            <Button variant="secondary" onClick={() => setOpen(false)} disabled={loading}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleDelete} disabled={loading}>
              {loading ? "Deleting..." : "Delete"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
};

export default DeleteButton;
