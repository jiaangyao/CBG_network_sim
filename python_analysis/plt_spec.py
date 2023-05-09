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

f_real, time_spec_real, sxx_real = signal.spectrogram(lfp_data_real_filt, fs=lfp_fs_real, nperseg=lfp_fs_real, return_onesided=True)

idx_f_real  = np.where(f_real <= 100)[0]
f_real = f_real[idx_f_real]
sxx_real = sxx_real[idx_f_real, :]


# now also obtain the simulated LFP signal
lfp_fs_sim = data_sim['lfp_fs']
lfp_time_sim = data_sim['lfp_time']
lfp_data_sim = data_sim['lfp_data']

f_sim, time_spec_sim, sxx_sim = signal.spectrogram(lfp_data_sim, fs=lfp_fs_sim, nperseg=lfp_fs_real, return_onesided=True)

idx_f_sim  = np.where(f_sim <= 100)[0]
f_sim = f_sim[idx_f_sim]
sxx_sim = sxx_sim[idx_f_sim, :]


# now plot the actual spectrogram signals
fig = plt.figure(figsize=(8, 10))
plt.subplot(211)
plt.pcolormesh(time_spec_real, f_real, sxx_real, shading='gouraud')
plt.title('Spectrogram for Real LFP data from STN')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
vmin_real, vmax_real = plt.gci().get_clim()
plt.clim(vmin_real, 1e-6)




plt.subplot(212)
plt.pcolormesh(time_spec_sim, f_sim, sxx_sim, shading='gouraud')
plt.title('Spectrogram for Simulated LFP data from STN')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
vmin_sim, vmax_sim = plt.gci().get_clim()
plt.clim(vmin_sim, 2e-8)

p_figure = pathlib.Path('/home/jyao/Downloads/')
plt.savefig(str(p_figure / 'spectrogram.png'), dpi=300)
plt.close(fig)

print('debug')
