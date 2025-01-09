import datetime
class Note:
    def __init__(self, code: int, text: str) -> None:
        self.code = code
        self.text = text
        self.timestamp = datetime.datetime.now()

    def __eq__(self, other) -> bool:
        """ returns true if two notes are equal"""
        return self.code == other.code and self.text == other.text

    def __str__(self) -> str:
        """ returns a string of the note"""
        result = ""
        result += "id: " + str(self.code) + "\n"
        result += self.text
        return result

    def update_note(self, txt: str) -> None:
        """ updates the note with the given string and its timestamp"""
        self.timestamp = datetime.datetime.now()
        self.text = txt