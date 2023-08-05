% Author : Lee McCuller
clear classes
addpath(char(py.msurrogate.matlabpath()));

%call = msurrogate.pywrap(@py.msurrogate.subproc_server.ServerSubprocess, []);
%proc = call('module_name', 'msurrogate.ping_test');
%
%disp(pyraw(proc.cookie_dict))
%disp(proc.cookie_dict{'workspace'}{'test_ping'})

%import numpy_cast.*
%qb = py.iirrational.testing.iirrational_data('simple2');
%mqb = py2mat(qb);
%
%pyro_config = py2mat(py.Pyro4.config);
%pyro_config.SERIALIZER = 'dill';
%pyro_config.REQUIRE_EXPOSE = false;
%
%conftext = fileread('iirrational_pyro_con.json');
%conf = iirrational.json.jsondecode(conftext);
%
%factory = py2mat(py.Pyro4.Proxy(conf.v1));
%
%obj = factory.rationalize.async({mqb});
%disp(obj.fitter.xfer_fit)
%obj.pyrosuper_getattr({'fitter'}).pyrosuper_call({'optimize'})


surrogate = msurrogate.PySurrogate();
surrogate.connect_subprocess('msurrogate.ping_test')
