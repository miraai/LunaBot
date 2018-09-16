def test_allservers(cmdopt):
    if cmdopt == "allservers":
        print("ctx.message.author, toReturn")
    elif cmdopt != "allservers":
        print("You are not the bot owner!")
    assert 0  # to see what was printed