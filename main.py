import matplotlib.pyplot as plt
import numpy as np
import soundcard as sc

default_mic = sc.all_microphones(include_loopback=False)[0]

# define as faixas de frequência
freq_bins = np.fft.rfftfreq(1024, 1/48000)
print(freq_bins)
bin_size = freq_bins[1] - freq_bins[0]
print(bin_size)
freq_ranges = np.arange(0, len(freq_bins), 20)
print(freq_ranges)

with default_mic.recorder(samplerate=48000) as mic:
    data = mic.record(numframes=1024)

    channel_l = data[:, 0]
    channel_r = data[:, 1]
    x = np.arange(len(freq_ranges))

    plt.ion()
    fig, (ax_l, ax_r) = plt.subplots(ncols=2, figsize=(10, 5))
    rects_l = ax_l.bar(x, np.zeros(len(freq_ranges)), color='red')
    rects_r = ax_r.bar(x, np.zeros(len(freq_ranges)))
    ax_l.set_ylim(0, 10)
    ax_r.set_ylim(0, 10)

    while True:
        mic.flush()
        data = mic.record(numframes=1024)

        channel_l = data[:, 0]
        channel_r = data[:, 1]

        # calcula a transformada de Fourier dos canais
        fft_l = np.abs(np.fft.rfft(channel_l))
        fft_r = np.abs(np.fft.rfft(channel_r))

        # agrupa as frequências em faixas e calcula a média das amplitudes
        grouped_l = [np.mean(fft_l[freq_ranges[i]:freq_ranges[i+1]]) for i in range(len(freq_ranges)-1)]
        grouped_r = [np.mean(fft_r[freq_ranges[i]:freq_ranges[i+1]]) for i in range(len(freq_ranges)-1)]

        for rect, h in zip(rects_l, grouped_l):
            rect.set_height(h)

        for rect, h in zip(rects_r, grouped_r):
            rect.set_height(h)

        fig.canvas.draw()
        fig.canvas.flush_events()
