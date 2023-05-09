import pickle
import pathlib

import mat73
import numpy as np
import scipy
import scipy.signal as signal
import matplotlib.pyplot as plt

from easydict import EasyDict as edict


# define the path to data
p_data = pathlib.Path('/home/jyao/local/data/starrlab/CBG_network_sim/python_data/')
f_data_sim = 'sim_data.mat'
f_data_real = 'RCS02_neural_data.pkl'

# now load the actual human data
time_domain_data, stn_features_out, cortex98_features_out, cortex1110_features_out = pickle.load(open(str(p_data / f_data_real), 'rb'))

# also load the simulated data
data_sim = mat73.loadmat(str(p_data / f_data_sim))['output']


# obtain the actual human LFP signal and perform simple processing
lfp_fs_real = 500
lfp_time_real = time_domain_data.time
lfp_data_real = time_domain_data.STN

hpf = signal.firwin(lfp_fs_real* 2 + 1, 0.5, fs=lfp_fs_real, pass_zero='highpass')
lfp_data_real_filt = signal.filtfilt(hpf, [1], lfp_data_real)

# take out a section of around 30 seconds in the real signal
lfp_data_real_filt = lfp_data_real_filt[90000:105000]
f_real, pxx_real = signal.welch(lfp_data_real_filt, fs=lfp_fs_real, nperseg=lfp_fs_real)

# now also obtain the simulated LFP signal
lfp_fs_sim = data_sim['lfp_fs']
lfp_time_sim = data_sim['lfp_time']
lfp_data_sim = data_sim['lfp_data']

f_sim, pxx_sim = signal.welch(lfp_data_sim, fs=lfp_fs_sim, nperseg=lfp_fs_sim)

# now plot the actual PSD signals
fig = plt.figure(figsize=(5.5, 10))

plt.subplot(211)
plt.semilogy(f_real, pxx_real)
plt.title('PSD for Real LFP data from STN')
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD (mV^2/Hz)')
plt.xlim([0, 100])
plt.ylim([1e-9, 1e-5])

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)


# plot the simulated data
plt.subplot(212)
plt.semilogy(f_sim, pxx_sim)
plt.title('PSD for Simulated LFP data from STN')
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD (mV^2/Hz)')
plt.xlim([0, 100])
plt.ylim([5e-10, 5e-8])

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

p_figure = pathlib.Path('/home/jyao/Downloads/')
f_figure = 'psd_comparison.png'
plt.savefig(str(p_figure / f_figure), dpi=300)
plt.close(fig)


print('debug')