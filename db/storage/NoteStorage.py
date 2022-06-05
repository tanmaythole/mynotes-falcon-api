import falcon
from sqlobject import *
from db.models.NotesModel import Notes

class NoteStorage:
    def get_notes(self, user_id, note_id=None):
        """
        Get notes from db. 
        If note_id=None then get all notes of user else get a note with note_id.
        """
        if note_id is None:
            return list(Notes.select(Notes.q.user==user_id))
        else:
            try:
                note = Notes.get(note_id)
            except Exception as e:
                raise falcon.HTTPNotFound("Not Found", str(e))
            
            # check whether note is authorized with requested user or not
            if note.user.id==user_id:
                return note
            raise falcon.HTTPUnauthorized("Unauthorized") 

    def add_note(self, user_id, data={}):
        """
        Add a note
        """
        note = Notes(
            title=data.get('title'), 
            description=data.get('description'), 
            user=user_id
        )
        return note
    
    def update_note(self, user_id, note_id, note_data={}):
        """
        Update a note
        """
        note = self.get_notes(user_id, note_id)
        note_dict = note.get_dict()
        for k, v in note_data.items():
            note_dict[k] = v
        try:
            note.set(
                title=note_dict['title'],
                description=note_dict['description']
            )
            return note
        except Exception as e:
            raise falcon.HTTPBadRequest("Wrong info", str(e))

    def delete_note(self, user_id, note_id):
        """
        Delete a note
        """
        note = self.get_notes(user_id, note_id)
        try:
            note.delete(note.id)
        except Exception as e:
            raise falcon.HTTPBadRequest("Wrong info", str(e))