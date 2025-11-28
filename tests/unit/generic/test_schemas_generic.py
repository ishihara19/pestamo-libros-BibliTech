from app.schemas.generic_sch import GenericMessage

def test_generic_message():
    msg = GenericMessage(message="ok")
    assert msg.message == "ok"
