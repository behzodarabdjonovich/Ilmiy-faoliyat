from aiogram.fsm.state import State, StatesGroup
class LetterForm(StatesGroup):
    letter_type=State(); recipient=State(); recipient_person=State(); recipient_position=State(); subject=State(); content=State(); request=State(); extra=State(); signer=State(); signer_position=State(); attachments=State(); confirm=State(); revise=State()
