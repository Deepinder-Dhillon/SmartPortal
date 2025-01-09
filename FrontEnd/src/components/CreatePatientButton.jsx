"use client";

import { useState } from "react";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import api from "@/services/api"; 

import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";

const formSchema = z.object({
  phn: z.string().length(6, { message: "PHN must be 6 digits." }).regex(/^\d+$/, { message: "PHN must be a number." }),
  name: z.string().min(3, { message: "Name must be at least 3 characters." }).regex(/^[A-Za-z\s]+$/, { message: "Name must contain only letters." }),
  phone: z.string().length(10, { message: "Phone number must be 10 digits." }).regex(/^\d+$/, { message: "Phone must contain only numbers." }),
  email: z.string().email({ message: "Invalid email format." }),
  birthDate: z.string().refine(
    (date) => new Date(date) < new Date(),
    { message: "Date of Birth must be in the past." }
  ),
  address: z.string().min(5, { message: "Address must be at least 5 characters." }), 
});

export function CreatePatientButton({ refreshPatients }) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false); 
  const [success, setSuccess] = useState(false); 
  const [error, setError] = useState(null); 

  // React Hook Form with Zod Validation
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      phn: "",
      name: "",
      phone: "",
      email: "",
      birthDate: "",
      address: "",
    },
  });

  async function onSubmit(values) {
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      await api.post("/patients/create/", values); 
      console.log("Patient Created:", values);
      
      form.reset();
      setSuccess(true); 
      setTimeout(() => setOpen(false), 1000); 
      
      refreshPatients(); 
    } catch (err) {
      console.error("Error creating patient:", err);
      setError(err.response?.data?.message || "Failed to create patient.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Button onClick={() => setOpen(true)}>Create Patient</Button>

      {/* Modal */}
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Create New Patient</DialogTitle>
          </DialogHeader>

          {success && <p className="text-green-500 text-sm">Patient created successfully!</p>}

          {error && <p className="text-red-500 text-sm">{error}</p>}

    
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField control={form.control} name="phn" render={({ field }) => (
                <FormItem>
                  <FormLabel>PHN</FormLabel>
                  <FormControl><Input placeholder="123456" {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )} />

              <FormField control={form.control} name="name" render={({ field }) => (
                <FormItem>
                  <FormLabel>Name</FormLabel>
                  <FormControl><Input placeholder="John Doe" {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )} />

              <FormField control={form.control} name="phone" render={({ field }) => (
                <FormItem>
                  <FormLabel>Phone</FormLabel>
                  <FormControl><Input placeholder="1234567890" {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )} />

              <FormField control={form.control} name="email" render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl><Input type="email" placeholder="email@example.com" {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )} />

              <FormField control={form.control} name="birthDate" render={({ field }) => (
                <FormItem>
                  <FormLabel>Date of Birth</FormLabel>
                  <FormControl><Input type="date" {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )} />

    
              <FormField control={form.control} name="address" render={({ field }) => (
                <FormItem>
                  <FormLabel>Address</FormLabel>
                  <FormControl><Input placeholder="123 Main St, City" {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )} />

              <DialogFooter>
                <Button variant="secondary" onClick={() => setOpen(false)} disabled={loading}>Cancel</Button>
                <Button type="submit" disabled={loading}>
                  {loading ? "Creating..." : "Create"}
                </Button>
              </DialogFooter>
            </form>
          </Form>
        </DialogContent>
      </Dialog>
    </>
  );
}
