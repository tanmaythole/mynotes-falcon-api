import json
import falcon
from db.storage.NoteStorage import NoteStorage

class Notes:
    def on_get(self, req, resp):
        """
        Get All notes
        """
        curr_user = req.context.get('current_user')
        notes = [note.get_dict() for note in NoteStorage().get_notes(user_id=curr_user.get('id'))]
        resp.status = falcon.HTTP_200
        resp.media = {
            "notes": notes
        }

    def on_get_note(self, req, resp, note_id):
        """
        Get one note with note_id
        """
        curr_user = req.context.get('current_user')
        notes = NoteStorage().get_notes(user_id=curr_user.get('id'), note_id=note_id).get_dict()
        resp.status = falcon.HTTP_200
        resp.media = notes

    def on_post(self, req, resp):
        """
        Create a note
        """
        curr_user = req.context.get('current_user')
        req_data = json.loads(req.stream.read())
        note = NoteStorage().add_note(
            user_id=curr_user.get('id'), 
            data=req_data
        )
        resp.status = falcon.HTTP_201
        resp.media = note.get_dict()

    def on_put_note(self, req, resp, note_id):
        """
        Update a note
        """
        curr_user = req.context.get('current_user')
        req_data = json.loads(req.stream.read())
        note = NoteStorage().update_note(curr_user.get('id'), note_id, req_data).get_dict()
        resp.status = falcon.HTTP_200
        resp.media = note

    def on_delete_note(self, req, resp, note_id):
        """
        Delete a note
        """
        curr_user = req.context.get('current_user')
        NoteStorage().delete_note(curr_user.get('id'), note_id)
        resp.status = falcon.HTTP_200
        resp.media = {
            "message": "Note Deleted Successfully!"
        }