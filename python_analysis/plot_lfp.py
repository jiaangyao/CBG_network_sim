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


# now also obtain the simulated LFP signal
lfp_fs_sim = data_sim['lfp_fs']
lfp_time_sim = data_sim['lfp_time']
lfp_data_sim = data_sim['lfp_data']

# now plot the actual LFP signals

fig = plt.figure(figsize=(10, 10))
plt.subplot(211)
plt.plot(lfp_time_real[90000:92500], lfp_data_real_filt[90000:92500])
plt.title('Real LFP data from STN')
plt.xlabel('Time')
plt.ylabel('Amplitude (mV)')

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# plot the simulated data
plt.subplot(212)
plt.plot(lfp_time_sim[40000:50000], lfp_data_sim[40000:50000])

plt.title('Simulated LFP data from STN')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (mV)')
plt.ylim([-4e-3, 4e-3])

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

p_figure = pathlib.Path('/home/jyao/Downloads/')
plt.savefig(str(p_figure / 'RCS02_LFP_comparison.png'))
plt.close(fig)

print('debug')