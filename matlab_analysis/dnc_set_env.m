function dnc_set_env(userDir)
if exist(userDir, 'dir')==7
    % Defaults
    project = 'CBG_network_sim';
    setenv('D_USER', userDir);
    setenv('D_PROJECT', fullfile(getenv('D_USER'), 'local', 'data', 'starrlab'));
    setenv('D_DATA_IN', fullfile(getenv('D_PROJECT'), 'CBG_network_sim'));
    setenv('D_DATA_OUT', fullfile(getenv('D_PROJECT'), 'proc_data'));
    setenv('STR_DATA_TYPE', 'neural data');
    setenv('STR_DATA_FOLDER', 'Combined');
    setenv('D_PROC_DATA', fullfile(getenv('D_PROJECT'), 'proc_data'));
    setenv('D_FIGURE', fullfile(getenv('D_PROJECT'), 'figures'));
    setenv('D_ANALYZE_RCS', fullfile(getenv('D_USER'), 'local', 'gitprojects', 'Analysis-rcs-data'));
end
end