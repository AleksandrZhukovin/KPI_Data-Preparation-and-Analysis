import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider, CheckButtons
import scipy.signal as sc


"""Create plots"""
noise_loc = 0
noise = np.random.normal(0, noise_loc, 1000)
t = np.linspace(0, 1, 1000)
fig, (ax1, ax2) = plt.subplots(1, 2)
line, = ax1.plot(t, 5 * np.sin(5 * t + 1), lw=2)
line1, = ax1.plot(t, 5 * np.sin(5 * t + 1), lw=2, visible=False, alpha=0.5)
filter_line, = ax2.plot(t, 5 * np.sin(5 * t + 1), lw=2)
fig.subplots_adjust(left=0.15, bottom=0.3)


"""Create interface elements"""
axfreq = fig.add_axes([0.25, 0.2, 0.55, 0.03])
freq_slider = Slider(
    ax=axfreq,
    label='Frequency',
    valmin=0.1,
    valmax=30,
    valinit=5,
)

axamp = fig.add_axes([0.05, 0.25, 0.0225, 0.63])
amp_slider = Slider(
    ax=axamp,
    label="Amplitude",
    valmin=0,
    valmax=10,
    valinit=5,
    orientation="vertical"
)

axorder = fig.add_axes([0.95, 0.25, 0.0225, 0.63])
filter_order_slider = Slider(
    ax=axorder,
    label="Filter Order",
    valmin=0.1,
    valmax=20,
    valinit=1,
    orientation="vertical"
)

axfs = fig.add_axes([0.25, 0.05, 0.55, 0.03])
sampling_rate_slider = Slider(
    ax=axfs,
    label='Sampling Rate',
    valmin=0.1,
    valmax=30,
    valinit=5,
)

axwn = fig.add_axes([0.25, 0.15, 0.55, 0.03])
Wn_slider = Slider(
    ax=axwn,
    label='Wn',
    valmin=0.1,
    valmax=10,
    valinit=0.1
)

axamp1 = fig.add_axes([0.25, 0.1, 0.55, 0.03])
noise_slider = Slider(
    ax=axamp1,
    label="Noise",
    valmin=0,
    valmax=2,
    valinit=0,
    orientation="horizontal"
)

rax = ax1.inset_axes([0.0, 0.0, 0.3, 0.1])
check = CheckButtons(
    ax=rax,
    labels=['Show Noise'],
    actives=[False]
)

rax1 = ax2.inset_axes([0.0, 0.0, 0.3, 0.1])
use_own = CheckButtons(
    ax=rax1,
    labels=['Use Own'],
    actives=[False]
)

resetax = fig.add_axes([0.9, 0.025, 0.1, 0.04])
reset_button = Button(resetax, 'Reset', hovercolor='0.975')


"""Display function"""
def harmonic_with_noise(amplitude, frequency, phase=1, noise_mean=0, show_noise=False, filter_order=1.0, Wn=.1, fs=.1,
                        own_filter=False):
    b, a = sc.iirfilter(int(filter_order), Wn=Wn, fs=fs, btype="low", ftype="butter")
    filtered_data = sc.lfilter(b, a, amplitude * np.sin(frequency * t + phase) + noise_mean)
    if show_noise:
        line.set_ydata(amplitude * np.sin(frequency * t + phase))
        line1.set_ydata(amplitude * np.sin(frequency * t + phase) + noise_mean)
        line1.set_visible(True)
    else:
        line.set_ydata(amplitude * np.sin(frequency * t + phase))
        line1.set_visible(False)
    if own_filter:
        filter_line.set_ydata(my_own_filter(amplitude * np.sin(frequency * t + phase) + noise_mean))
    else:
        filter_line.set_ydata(filtered_data)
    fig.canvas.draw_idle()


def my_own_filter(data, buffer_size=7):
    res = np.zeros(len(data))
    for n in range(len(data)-buffer_size):
        res[n] += sum(data[n:n+7])
    res /= buffer_size
    return res


"""Plot updating"""
def update(val):
    global noise_loc
    global noise
    if noise_loc != noise_slider.val:
        noise_loc = noise_slider.val
        noise = np.random.normal(0, noise_loc, 1000)
    Wn_slider.valmax = sampling_rate_slider.val / 2 - 0.01
    harmonic_with_noise(amp_slider.val, freq_slider.val, noise_mean=noise,
                        show_noise=check.get_status()[0], filter_order=filter_order_slider.val, Wn=Wn_slider.val,
                        fs=sampling_rate_slider.val, own_filter=use_own.get_status()[0])


freq_slider.on_changed(update)
amp_slider.on_changed(update)
filter_order_slider.on_changed(update)
noise_slider.on_changed(update)
Wn_slider.on_changed(update)
check.on_clicked(update)
sampling_rate_slider.on_changed(update)
use_own.on_clicked(update)

Wn_slider.valmax = sampling_rate_slider.val / 2 - 0.01


"""Resetting data"""
def reset(event):
    freq_slider.reset()
    amp_slider.reset()
    noise_slider.reset()
    if check.get_status()[0]:
        check.set_active(0)


reset_button.on_clicked(reset)
plt.show()
