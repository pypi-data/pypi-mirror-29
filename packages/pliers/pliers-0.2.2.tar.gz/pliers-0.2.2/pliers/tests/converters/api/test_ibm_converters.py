from os.path import join
from ...utils import get_test_data_path
from pliers.converters import IBMSpeechAPIConverter
from pliers.stimuli import AudioStim, TextStim, ComplexTextStim
import pytest

AUDIO_DIR = join(get_test_data_path(), 'audio')


@pytest.mark.skipif("'IBM_USERNAME' not in os.environ or "
                    "'IBM_PASSWORD' not in os.environ")
def test_IBMSpeechAPIConverter():
    stim = AudioStim(join(AUDIO_DIR, 'homer.wav'), onset=4.2)
    conv = IBMSpeechAPIConverter()
    out_stim = conv.transform(stim)
    assert isinstance(out_stim, ComplexTextStim)
    first_word = next(w for w in out_stim)
    assert isinstance(first_word, TextStim)
    assert first_word.duration > 0
    assert first_word.onset is not None
    second_word = [w for w in out_stim][1]
    assert second_word.onset > 4.2
    num_words = len(out_stim.elements)
    full_text = [elem.text for elem in out_stim]
    assert 'thermodynamics' in full_text or 'obey' in full_text

    conv2 = IBMSpeechAPIConverter(resolution='phrases')
    out_stim = conv2.transform(stim)
    assert isinstance(out_stim, ComplexTextStim)
    first_phrase = next(w for w in out_stim)
    assert isinstance(first_phrase, TextStim)
    full_text = first_phrase.text
    assert len(full_text.split()) > 1
    assert 'thermodynamics' in full_text or 'obey' in full_text
    assert len(out_stim.elements) < num_words
