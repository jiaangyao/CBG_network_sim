%% Envrionment setup

clearvars -except nothing;
clc;
close all;

set_env;


%% Setting the path to actual data

p_data_in = getenv('D_DATA_IN');
p_data_in_full = fullfile(p_data_in, 'Simulation_Output_Results', ...
    'Controller_Simulations', 'Amp', 'standard_PID_Controller');


vec_pfe_data = glob(fullfile(p_data_in_full, '/**/', '*LFP.mat'));
vec_pfe_stim = glob(fullfile(p_data_in_full, '/**/', 'DBS*'));


%% First load the DBS stim signal

% load in the DBS current signal and reconstruct the time
load(vec_pfe_stim{1}, 'block')

dbs_fs = block.segments{1}.analogsignals{1}.sampling_rate * 1e3;
dbs_time = block.segments{1}.analogsignals{2}.signal(2:end) / 1e3;
dbs_data = block.segments{1}.analogsignals{1}.signal(2:end);

% % quick plot for illustration
% plot(dbs_time(200000:260000), dbs_data(200000:260000))
% xlabel('Time (s)')
% ylabel('DBS Amplitude (mA)')
% title('DBS Stim Signal')


%% Next load the LFP signal

% laod in the LFP signal and reconstruct the time
load(vec_pfe_data{1}, 'block')
data_struct = block.segments{1}.analogsignals{1};

% note that the LFP data are in units of mV
lfp_fs = 1 / (0.5 * 1e-3);
lfp_data = data_struct.signal;
lfp_time = 0: (1/lfp_fs): ((size(lfp_data, 1) - 1)/lfp_fs);
lfp_time = lfp_time + dbs_time(1);

%% Now form the output variable

% obtain the DBS fields
output.dbs_fs = dbs_fs;
output.dbs_time = dbs_time;
output.dbs_data = dbs_data;

% obtain the LFP signals
output.lfp_fs = lfp_fs;
output.lfp_time = lfp_time;
output.lfp_data = lfp_data;

p_output = fullfile(p_data_in, 'python_data/');
f_output = 'sim_data.mat';

save(fullfile(p_output, f_output), 'output', '-v7.3')