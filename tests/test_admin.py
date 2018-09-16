# content of test_sample.py
def test_answer(cmdopt):
    if cmdopt == "allservers":
        print("ctx.message.author, toReturn")
    elif cmdopt != "allservers":
        print("You are not the bot owner!")
    assert 0  # to see what was printed