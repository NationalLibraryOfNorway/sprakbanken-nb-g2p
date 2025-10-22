import pytest
from pathlib import Path
from nb_g2p import utils


# Mock dependencies for isolated testing
class DummyPhonetisaurus:
    @staticmethod
    def predict(words, model_path=None):
        # Return each word with a dummy phoneme list
        return [(word, [f"{word}_PH"]) for word in words]


def dummy_nofabet_to_syllables(transcription):
    # Split on spaces as dummy syllables
    return transcription.split()


def dummy_nofabet_to_ipa(nofabet):
    return f"IPA({nofabet})"


@pytest.fixture(autouse=True)
def patch_dependencies(monkeypatch):
    monkeypatch.setattr(utils, "phonetisaurus", DummyPhonetisaurus)
    monkeypatch.setattr(utils, "nofabet_to_syllables", dummy_nofabet_to_syllables)
    monkeypatch.setattr(utils, "nofabet_to_ipa", dummy_nofabet_to_ipa)
    # Patch download_g2p_model to avoid file IO
    monkeypatch.setattr(
        utils, "download_g2p_model", lambda dialect, style: Path("/dummy/model.fst")
    )


def test_is_punctuation():
    assert utils.is_punctuation(".")
    assert not utils.is_punctuation("a")


def test_strip_redundant_whitespace():
    assert utils.strip_redundant_whitespace("a   b\nc") == "a b c"
    assert utils.strip_redundant_whitespace("   ") == ""


def test_strip_punctuation():
    assert utils.strip_punctuation("Hei, verden!") == "Hei verden"
    assert utils.strip_punctuation("...") == ""


def test_format_transcription():
    assert utils.format_transcription(["a", "b", "c"]) == "a b c"


def test_syllabify():
    # Each word gets a dummy phoneme list, which is joined and split as syllables
    transcription = [("hei", ["h", "ei"]), ("verden", ["v", "e", "r", "d", "e", "n"])]
    # convert_to_syllables will join the phonemes and split on spaces
    result = utils.syllabify(transcription)
    assert isinstance(result, list)
    assert all(isinstance(s, str) for s in result)


@pytest.mark.xfail
def test_convert_to_syllables_nofabet():
    phonemes = "V AEH1 R D NX0"
    result = utils.convert_to_syllables(phonemes, ipa=False)
    assert result == [["V", "AEH1", "R"], ["D", "NX0"]]


def test_convert_to_syllables_ipa():
    # Should call dummy_nofabet_to_ipa and split on "."
    phonemes = ["V", "AEH1", "R", "D", "NX0"]

    # Patch nofabet_to_ipa to return a string with dots
    def fake_nofabet_to_ipa(nofabet):
        return "'vær.dn̩"

    utils.nofabet_to_ipa = fake_nofabet_to_ipa
    result = utils.convert_to_syllables(phonemes, ipa=True)
    assert result == ["'vær", "dn̩"]


def test_transcribe_basic():
    text = "hei verden"
    result = list(utils.transcribe(text))
    assert result[0][0] == "hei"
    assert isinstance(result[0][1], str)


def test_transcribe_full_annotation():
    text = "hei"
    result = list(utils.transcribe(text, full_annotation=True))
    assert isinstance(result[0], dict)
    assert "word" in result[0]
    assert "nofabet" in result[0]
    assert "syllables" in result[0]
    assert "ipa" in result[0]


def test_annotate_transcriptions():
    transcription = [("hei", ["H", "AEJ1"])]
    result = list(utils.annotate_transcriptions(transcription))
    assert isinstance(result[0], dict)
    assert result[0]["word"] == "hei"


def test_transcribe_words():
    words = ["hei", "verden"]
    result = list(utils.transcribe_words(words))
    assert result[0][0] == "hei"
    assert isinstance(result[0][1], list)


def test_split_paragraphs():
    text = "Line1\nLine2\n\nPara2Line1\nPara2Line2"
    result = utils.split_paragraphs(text)
    assert isinstance(result, list)
    assert isinstance(result[0], list)
    assert result[0][0] == "Line1"
    assert result[1][1] == "Para2Line2"


def test_transcribe_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hei\nverden\n\n")
    result = utils.transcribe_file(file)
    assert result["text_id"] == "test"
    assert "line_0" in result
    assert isinstance(result["line_0"], list)
    assert result["line_2"] == []
