
from clinic.note import Note
from clinic.dao.note_dao_pickle import NoteDAOPickle


class PatientRecord:
    def __init__(self, phn: int, autosave = False ) -> None:
        self.autosave = autosave
        self.phn = str(phn)
        self._note_dao = NoteDAOPickle(self.phn, self.autosave)
    
    def add_note(self, note: str) -> Note:
        """returns and adds a new note to the list of notes"""
        return self._note_dao.create_note(note)

    def get_note_by_id(self, id: int) -> Note:
        """ returns the note with the given id"""
        return self._note_dao.search_note(id)

    def get_notes_by_text(self, text: str) -> [Note]:
        """ returns list of notes with the given text"""

        return self._note_dao.retrieve_notes(text)

    def update_note(self, id: int, note: str) -> bool:
        """ return and updates the note with the given id if it exists"""
        return self._note_dao.update_note(id, note)

    def delete_patient_note(self, id: int) -> bool:
        """ returns true and deletes the note with the given id from the list of notes if it exists"""
        return self._note_dao.delete_note(id)

    def get_notes_list(self) -> [Note]:
        """ returns list of notes in reverse order"""
        return self._note_dao.list_notes()











