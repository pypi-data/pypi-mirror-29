% Author : Lee McCuller
clear classes
addpath(char(py.msurrogate.matlabpath()));

surrogate = msurrogate.PySurrogate();
surrogate.connect_cookie('cookie.json')
surrogate.test_ping()
