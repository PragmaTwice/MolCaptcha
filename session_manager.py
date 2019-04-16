import random
import os
import molcaptcha
import uuid


class MolSession(uuid.UUID):

    session_map = {}
    png_dir = "data/generated/question/PNG"
    answer_dir = "data/generated/answer"

    def __init__(self, session_id=uuid.uuid4()):
        super(MolSession, self).__init__(bytes=session_id.bytes)
        if self not in MolSession.session_map:
            MolSession.session_map[self] = {}

    def get_captcha(self):
        choice = random.choice(os.listdir(MolSession.png_dir))
        MolSession.session_map[self]['png_path'] = os.path.join(MolSession.png_dir, choice)
        MolSession.session_map[self]['answer_path'] = os.path.join(MolSession.answer_dir, choice)

        png = b''
        with open(MolSession.session_map[self]['png_path'], "rb") as png_file:
            png = png_file.read()

        return png

    def response_captcha(self, input_str):
        if 'answer_path' in MolSession.session_map[self]:
            return molcaptcha.mol_judge(input_str, MolSession.session_map[self]['answer_path'])
        else:
            return False


if __name__ == '__main__':

    session = MolSession()
    print(session.get_captcha())
