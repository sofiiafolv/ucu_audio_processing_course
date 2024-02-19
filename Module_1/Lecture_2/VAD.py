from glob import glob
import IPython.display as ipd
import math

def peak_normalization(audio):
    peak_normalized_audio = audio / max([abs(value) for value in audio])
    return peak_normalized_audio

def frame_size(sampling_rate, frame_duration):
    return int(sampling_rate * frame_duration)

def num_frames(audio, sampling_rate, frame_duration):
    f_sz = frame_size(sampling_rate, frame_duration)
    return math.ceil(len(audio) / f_sz)

def short_term_energy(signal):
    return math.sqrt(sum([pow(abs(value), 2) for value in signal]))

def vad_algorithm(audio, sampling_rate, energy_threshold=0.075, frame_duration=0.001):
    audio = peak_normalization(audio)
    f_sz = frame_size(sampling_rate, frame_duration)
    frames = num_frames(audio, sampling_rate, frame_duration)
    energies = [short_term_energy(audio[i * f_sz : (i + 1) * f_sz]) for i in range(frames)]

    vad_segments = [1 if energy > energy_threshold else 0 for energy in energies]

    speech_start = [i * f_sz for i in range(frames) if vad_segments[i] == 1 and (i == 0 or vad_segments[i - 1] == 0)]
    speech_end = [(i + 1) * f_sz for i in range(frames - 1) if vad_segments[i] == 1 and (i == frames - 1 or vad_segments[i + 1] == 0)]

    if vad_segments[-1] == 1 and (len(speech_end) == 0 or speech_end[-1] != len(audio)):
        speech_end.append(len(audio))

    speech_timestamps = list(zip(speech_start, speech_end))

    return [{'start': start, 'end': end} for start, end in speech_timestamps]
