import pytest


class TestGetResponseText:
    @pytest.mark.parametrize(
        "message",
        [
            ("つらい"),
            ("辛い"),
            ("頑張る"),
            ("がんばる"),
            ("がむばる"),
            ("がむぱる"),
        ],
    )
    def test_negative_pattern(self, message):
        from lib.messages import get_response_text

        assert get_response_text(message) == "ぱにゃにゃんだー🐼😺"

    @pytest.mark.parametrize(
        "message",
        [
            ("褒めて"),
            ("ほめて"),
            ("頑張った"),
            ("がんばった"),
            ("がむばった"),
            ("がむぱった"),
        ],
    )
    def test_compliment_pattern(self, message):
        from lib.messages import get_response_text

        assert get_response_text(message) == "えらい！！！"

    def test_maxim(self):
        from lib.messages import get_response_text

        assert get_response_text("maxim") != "maxim"

    def test_choice(self):
        from lib.messages import get_response_text

        choices = ["hoge", "fuga", "piyo"]
        actual = get_response_text("choice " + ",".join(choices))

        expected = [f"I choose this 👉 {e}" for e in choices]
        assert actual in expected
