#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import webrtcvad
from librosa.core import resample
from librosa.util import frame


def vad(data, fs, fs_vad=16000, hoplength=30, vad_mode=0):
    """ Voice activity detection.
    This was implementioned for easier use of py-webrtcvad.
    Parameters
    ----------
    data : ndarray
        numpy array of mono (1 ch) speech data.
        1-d or 2-d, if 2-d, shape must be (1, time_length) or (time_length, 1).
        if data type is int, -32768 < data < 32767.
        if data type is float, -1 < data < 1.
    fs : int
        Sampling frequency of data.
    fs_vad : int, optional
        Sampling frequency for webrtcvad.
        fs_vad must be 8000, 16000, 32000 or 48000.
        Default is 16000.
    hoplength : int, optional
        Step size[milli second].
        hoplength must be 10, 20, or 30.
        Default is 0.1.
    vad_mode : int, optional
        set vad aggressiveness.
        As vad_mode increases, it becomes more aggressive.
        vad_mode must be 0, 1, 2 or 3.
        Default is 0.

    Returns
    -------
    vact : ndarray
        voice activity. time length of vact is same as input data.
        If 0, it is unvoiced, 1 is voiced.
    """

    # check argument
    if fs_vad not in [8000, 16000, 32000, 48000]:
        raise ValueError('fs_vad must be 8000, 16000, 32000 or 48000.')

    if hoplength not in [10, 20, 30]:
        raise ValueError('hoplength must be 10, 20, or 30.')

    if vad_mode not in [0, 1, 2, 3]:
        raise ValueError('vad_mode must be 0, 1, 2 or 3.')

    # check data
    if data.dtype.kind == 'i':
        if data.max() > 2**15 - 1 or data.min() < -2**15:
            raise ValueError(
                'when data type is int, data must be -32768 < data < 32767.')
        data = data.astype('f')

    elif data.dtype.kind == 'f':
        if np.abs(data).max() >= 1:
            raise ValueError(
                'when data type is float, data must be -1.0 < data < 1.0.')
        data = (data * 2**15).astype('f')
    else:
        raise ValueError('data dtype must be int or float.')

    data = data.squeeze()
    if not data.ndim == 1:
        raise ValueError('data must be mono (1 ch).')

    # resampling
    if fs != fs_vad:
        resampled = resample(data, fs, fs_vad)
    else:
        resampled = data

    resampled = resampled.astype('int16')

    hop = fs_vad * hoplength // 1000
    framelen = resampled.size // hop + 1
    padlen = framelen * hop - resampled.size
    paded = np.lib.pad(resampled, (0, padlen), 'constant', constant_values=0)
    framed = frame(paded, frame_length=hop, hop_length=hop).T

    vad = webrtcvad.Vad()
    vad.set_mode(vad_mode)
    valist = [vad.is_speech(tmp.tobytes(), fs_vad) for tmp in framed]

    hop_origin = fs * hoplength // 1000
    va_framed = np.zeros([len(valist), hop_origin])
    va_framed[valist] = 1

    return va_framed.reshape(-1)[:data.size]
