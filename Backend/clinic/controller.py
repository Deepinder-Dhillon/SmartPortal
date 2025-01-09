from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from clinic.patient import Patient
from clinic.note import Note
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
from clinic.dao.patient_dao_json import PatientDAOJSON

class Controller:
    def __init__(self, autosave=False) -> None:
        self.autosave = autosave
        self._patient_dao_json = PatientDAOJSON(self.autosave)
        self._patient = None

    def login(self, request, username: str, password: str) -> dict:
        """Authenticate user and return JWT token"""
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        else:
            raise InvalidLoginException("Invalid username or password")

    def is_logged(self, request) -> bool:
        """ Check if user is authenticated using JWT """
        auth = JWTAuthentication()
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split()[1]
                auth.get_validated_token(token)
                return True
        except Exception:
            return False
        return False

    def logout(self, request) -> bool:
        """Blacklist the refresh token to log out"""
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return True
        except Exception:
            raise InvalidLogoutException()

    def create_patient(self, request, phn: int, name: str, birth_date: str, phone: str, email: str, address: str) -> Patient:
        """ Creates and returns a new patient if logged in """
        if not self.is_logged(request):
            raise IllegalAccessException()

        if self._patient_dao_json.search_patient(phn):
            raise IllegalOperationException("Patient with this PHN already exists.")

        patient = Patient(phn, name, birth_date, phone, email, address, self.autosave)
        self._patient_dao_json.create_patient(patient)
        return patient

    def search_patient(self, request, phn: int) -> Patient:
        """ Returns a patient by PHN if logged in """
        if not self.is_logged(request):
            raise IllegalAccessException()

        return self._patient_dao_json.search_patient(phn)

    def retrieve_patients(self, request, name: str) -> list:
        """Returns a list of patients with a matching name if logged in"""
        if not self.is_logged(request):
            raise IllegalAccessException()

        return self._patient_dao_json.retrieve_patients(name)

    def update_patient(self, request, original_phn: int, phn: int, name: str, birth_date: str, phone: str, email: str, address: str) -> bool:
        """ Updates patient data if logged in """
        if not self.is_logged(request):
            raise IllegalAccessException()

        patient = self.search_patient(request, original_phn)
        if patient is None:
            raise IllegalOperationException("Patient not found.")

        new_patient = Patient(phn, name, birth_date, phone, email, address, self.autosave)

        if original_phn == phn:
            self._patient_dao_json.update_patient(original_phn, new_patient)
            return True

        if self._patient_dao_json.search_patient(phn):
            raise IllegalOperationException("New PHN is already in use.")

        self._patient_dao_json.delete_patient(original_phn)
        self._patient_dao_json.create_patient(new_patient)
        return True

    def delete_patient(self, request, phn: int) -> bool:
        """ Deletes a patient if logged in """
        if not self.is_logged(request):
            raise IllegalAccessException()

        patient = self._patient_dao_json.search_patient(phn)
        if patient is None:
            return False

        return self._patient_dao_json.delete_patient(phn)

    def list_patients(self, request) -> list:
        """ Returns a list of all patients if logged in """
        if not self.is_logged(request):
            raise IllegalAccessException()

        return self._patient_dao_json.list_patients()

    def set_current_patient(self, request, phn: int) -> None:
        """Sets the current patient if logged in"""
        if not self.is_logged(request):
            raise IllegalAccessException()

        patient = self._patient_dao_json.search_patient(phn)
        if patient is None:
            raise IllegalOperationException("Patient not found.")

        self._patient = patient

    def get_current_patient(self, request) -> Patient:
        """Returns the current patient if logged in"""
        if not self.is_logged(request):
            raise IllegalAccessException()

        if self._patient is None:
            raise NoCurrentPatientException("No current patient selected.")

        return self._patient

    def unset_current_patient(self, request) -> None:
        """Unsets the current patient"""
        if not self.is_logged(request):
            raise IllegalAccessException()

        self._patient = None

    def create_note(self, request, note: str) -> Note:
        """ Creates a patient note if logged in """
        if not self.is_logged(request):
            raise IllegalAccessException()

        if self._patient is None:
            raise NoCurrentPatientException("No current patient selected.")

        if not note.strip():
            raise IllegalOperationException("Note text cannot be empty.")

        note_record = self._patient.get_patient_records().add_note(note)
        return note_record

    def search_note(self, request, note_id: int) -> Note:
        """ Searches and returns a note if logged in """
        if not self.is_logged(request):
            raise IllegalAccessException()

        if self._patient is None:
            raise NoCurrentPatientException("No current patient selected.")

        return self._patient.get_patient_records().get_note_by_id(note_id)

    def retrieve_notes(self, request, text: str) -> list:
        """ Returns a list of patient notes if logged in """
        if not self.is_logged(request):
            raise IllegalAccessException()

        if self._patient is None:
            raise NoCurrentPatientException("No current patient selected.")

        return self._patient.get_patient_records().get_notes_by_text(text)

    def update_note(self, request, note_id: int, note: str) -> bool:
        """ Updates a patient note if logged in """
        if not self.is_logged(request):
            raise IllegalAccessException()

        if self._patient is None:
            raise NoCurrentPatientException("No current patient selected.")

        return self._patient.get_patient_records().update_note(note_id, note)

    def delete_note(self, request, note_id: int) -> bool:
        """ Deletes a patient note if logged in """
        if not self.is_logged(request):
            raise IllegalAccessException()

        if self._patient is None:
            raise NoCurrentPatientException("No current patient selected.")

        return self._patient.get_patient_records().delete_patient_note(note_id)

    def list_notes(self, request) -> list:
        """ Returns all patient notes if logged in """
        if not self.is_logged(request):
            raise IllegalAccessException()

        if self._patient is None:
            raise NoCurrentPatientException("No current patient selected.")

        notes = self._patient.get_patient_records().get_notes_list()
        if not notes:
            raise IllegalOperationException("No notes found.")

        return notes
