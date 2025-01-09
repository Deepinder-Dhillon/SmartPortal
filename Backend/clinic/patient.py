from clinic.patient_record import PatientRecord
from clinic.note import Note


class Patient:
    def __init__(self,
                 phn: int,
                 name: str,
                 birth_date: str,
                 phone: str,
                 email: str,
                 address: str,
                 autosave = False) -> None:
        self.autosave = autosave
        self.phn = phn
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        self.patient_records = PatientRecord(phn, self.autosave)

    def __eq__(self, other) -> bool:
        """ returns true if both patient are equal"""
        if (self.phn == other.phn and self.name == other.name
                and self.birth_date == other.birth_date
                and self.phone == other.phone and self.email == other.email
                and self.address == other.address):
            return True
        
        else:
            return False
            
    def get_name(self) -> str:
        """ returns patient name"""
        return self.name

    def get_phn(self) -> int:
        """ returns patient phn"""
        return self.phn
        
    def update_data(self, name: str, birth_date: str,
                        phone: str,
                        email: str,
                        address: str ) -> None:
        """ updates patient data"""
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address

    def __str__(self) -> str:
        """ returns patient string"""
        result = ""
        result += "PHN: " + str(self.phn)
        result += " Name: " + self.name
        result += " Birth Date: " + self.birth_date
        result += " Phone: " + self.phone
        result += " Email: " + self.email
        result += " Address: " + self.address
        return result

    def get_patient_records(self) -> PatientRecord:
        """ returns patient records"""
        return self.patient_records


