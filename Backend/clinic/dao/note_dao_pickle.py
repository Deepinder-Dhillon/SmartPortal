from clinic.dao.note_dao import NoteDAO
from clinic.note import Note
import pickle

class NoteDAOPickle(NoteDAO):
    def __init__(self, phn: str, autosave: False):
        self.autosave = autosave
        self.phn = phn
        self.auto_counter = 0
        self.notes = []
        self.filepath =  f'./clinic/records/{self.phn}.dat'

        if autosave:
            self.load_notes()

    def load_notes(self) -> None:
        """ load notes data from binary pickle file"""
        try:
            with open(self.filepath, 'rb') as file:
                self.notes = pickle.load(file)
                if self.notes:
                    self.auto_counter = max(note.code for note in self.notes)
        except (FileNotFoundError, EOFError):
            self.notes = []

    def save_notes(self) -> None:
        """ Save patient notes data in pickle binary file """
        with open(self.filepath, 'wb') as file:
            pickle.dump(self.notes, file)
        print(f"Notes saved for patient {self.phn} in {self.filepath}")  # Debugging output

    def search_note(self, key: int) -> Note:
        """ returns note by given id"""
        for note in self.notes:
            if note.code == key:
                return note
        return None

    def create_note(self, text: str) -> Note:
        """ Creates a new note for the patient """
        self.auto_counter += 1
        patient_note = Note(self.auto_counter, text)
        self.notes.append(patient_note)

        if self.autosave:
            self.save_notes()
        print(f"Note created: {patient_note.code} - {patient_note.text}")  # Debugging output
        return patient_note

    def retrieve_notes(self, search_string: str) -> [Note]:
        """ returns a list of notes with given search string"""
        result = []
        for note in self.notes:
            if search_string.lower() in note.text.lower():
                result.append(note)
        return result

    def update_note(self, key: int, text: str) -> bool:
        """ updates patient note by id"""
        patient_note = self.search_note(key)

        if patient_note:
            patient_note.update_note(text)
            if self.autosave:
                self.save_notes()
            return True

        return False

    def delete_note(self, key: int) -> bool:
        """ delete patient note by id"""
        patient_note = self.search_note(key)

        if patient_note:
            self.notes.remove(patient_note)
            if self.autosave:
                self.save_notes()
            return True

        return False

    def list_notes(self) -> [Note]:
        """ returns a list of all the patient notes """
        temp = []
        for note in self.notes:
            temp.append(note.code)
        temp.sort()
        result = []
        for i in range(len(temp) - 1, -1, -1):
            result.append(self.search_note(temp[i]))

        return result




