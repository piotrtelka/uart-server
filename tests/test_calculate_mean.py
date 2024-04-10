from app.routers.device import calc_mean, Message, Mean


def test_calc_mean_empty():
    messages = []
    result = calc_mean(messages)
    assert result == Mean(pressure=0, temperature=0, velocity=0)


def test_calc_mean_single():
    message = Message(pressure=10, temperature=20, velocity=30)
    messages = [message]
    result = calc_mean(messages)
    assert result == Mean(pressure=10, temperature=20, velocity=30)


def test_calc_mean_multiple():
    messages = [
        Message(pressure=5, temperature=15, velocity=25),
        Message(pressure=10, temperature=20, velocity=30),
        Message(pressure=15, temperature=25, velocity=35),
    ]
    result = calc_mean(messages)
    assert result == Mean(pressure=10, temperature=20, velocity=30)
