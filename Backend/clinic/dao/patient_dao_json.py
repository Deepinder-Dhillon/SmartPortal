import json
from json import JSONDecodeError
from clinic.dao.patient_decoder import PatientDecoder
from clinic.dao.patient_encoder import PatientEncoder
from clinic.patient import Patient
from clinic.dao.patient_dao import PatientDAO



class PatientDAOJSON(PatientDAO):
    def __init__(self, autosave = False):
        self._autosave = autosave
        self.patients = {}
        self.filepath = "./clinic/patients.json"

        if self._autosave:
            self.patients = self.load_patients()


    def load_patients(self) -> dict[int, Patient]:
        """ loads the Patients from patient json file"""
        patients = {}
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file, cls=PatientDecoder)
                for phn, patient in data.items():
                    patients[int(phn)] = patient

        except FileNotFoundError or EOFError or JSONDecodeError:
            patients = {}

        return patients

    def save_patients(self):
        """ saves the Patients to patient json file"""
        with open(self.filepath, "w") as file:
            json.dump(self.patients, file, cls=PatientEncoder)

    def create_patient(self, patient: Patient) -> Patient:
        """ creates a new patient and adds it to the database."""
        phn = patient.phn
        self.patients[phn] = patient
        if self._autosave:
            self.save_patients()

        return patient

    def search_patient(self, key: int) -> Patient:
        """ returns the patient by PHN if found, else None."""
        if key in self.patients:
            return self.patients[key]
        else:
            return None

    def retrieve_patients(self, name: str) -> [Patient]:
        """ returns a list of patients matching the given name."""
        result = []
        for phn in self.patients:

            patient = self.patients[phn]
            patient_name = patient.get_name().lower()
            name = name.lower()

            if name in patient_name:
                result.append(patient)

        result.reverse()

        return result

    def update_patient(self, key: int, updated_patient: Patient) -> bool:
        """ updates a patient's information if they exist, using the provided Patient object."""
        if key not in self.patients:
            return False

        existing_patient = self.patients[key]
        existing_patient.update_data(
            updated_patient.name,
            updated_patient.birth_date,
            updated_patient.phone,
            updated_patient.email,
            updated_patient.address
        )

        if self._autosave:
            self.save_patients()
        return True

    def delete_patient(self, phn: int) -> bool:
        """ deletes a patient by PHN if found."""
        if phn in self.patients:

            del self.patients[phn]
            if self._autosave:
                self.save_patients()
            return True

        return False

    def list_patients(self) -> [Patient]:
        """ returns a list of all patients."""
        result = list(self.patients.values())

        return result
