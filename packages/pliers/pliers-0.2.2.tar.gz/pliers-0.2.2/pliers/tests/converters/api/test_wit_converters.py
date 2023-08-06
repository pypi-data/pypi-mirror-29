from os.path import join
from ...utils import get_test_data_path
from pliers.converters import WitTranscriptionConverter
from pliers.stimuli import AudioStim, TextStim, ComplexTextStim
import pytest

AUDIO_DIR = join(get_test_data_path(), 'audio')


@pytest.mark.skipif("'WIT_AI_API_KEY' not in os.environ")
def test_WitTranscriptionConverter():
    stim = AudioStim(join(AUDIO_DIR, 'homer.wav'), onset=4.2)
    conv = WitTranscriptionConverter()
    out_stim = conv.transform(stim)
    assert type(out_stim) == ComplexTextStim
    first_word = next(w for w in out_stim)
    assert type(first_word) == TextStim
    assert first_word.onset == 4.2
    second_word = [w for w in out_stim][1]
    assert second_word.onset == 4.2
    text = [elem.text for elem in out_stim]
    assert 'thermodynamics' in text or 'obey' in text
