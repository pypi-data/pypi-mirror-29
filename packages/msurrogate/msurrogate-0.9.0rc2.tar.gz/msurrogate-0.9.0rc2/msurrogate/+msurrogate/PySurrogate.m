%% @deftypefn  {Function File} {} polynomial ()
%% @deftypefnx {Function File} {} polynomial (@var{a})
%% Create a polynomial object representing the polynomial
%%
%% @example
%% @end example
%%
%% @noindent
%% @end deftypefn
classdef PySurrogate < handle
  properties
    proc = [];
    workspace = [];
    auto_stop = false;
  end
  methods (Access = public)

    function self = PySurrogate()
    end

    function delete(self)
      try
        if self.auto_stop
          self.stop();
        end
      catch
      end
    end

    function b = attached(self)
      if isempty(self.workspace) && ~isa(self.workspace, 'containers.Map')
        b = false;
      else
        b = true;
      end
    end

    function stop(self)
      import msurrogate.*
      if ~self.attached()
        return
      end
      if self.workspace.isKey('workspace_close')
        self.workspace_close();
      end
      if ~isempty(self.proc)
        self.proc.stop()
      end
      self.proc = [];
      self.workspace = [];
      self.auto_stop = false;
    end

    function workspace_close(self)
      if self.workspace.isKey('workspace_close')
        %TODO, need to catch the connection receive error
        %subsref is never used from within the class
        s = struct('type', '()', 'subs', {'workspace_close',});
        close_call = subsref(self, s);
        close_call.oneway_();
      else
        error('This workspace connection does not expose workspace_close')
      end

    end

    function connect_subprocess(self, module_name, varargin)
      import msurrogate.*
      if self.auto_stop
        self.stop();
      end

      [args, kwargs] = collectargs(varargin);
      call = msurrogate.pywrap(@py.msurrogate.SurrogateSubprocess, []);

      if isfield(kwargs, 'auto_stop')
        auto_stop = kwargs.auto_stop
        %remove so that it is not passed to the proc call itself
        rmfield(kwargs, auto_stop)
      else
        auto_stop = true;
      end

      if ~isfield(kwargs, 'python_call')
        pycall = self.set_python_call();
        if ~isempty(pycall)
          kwargs.python_call = pycall
        end
      end

      if ~isfield(kwargs, 'env')
        pyenv = self.set_python_env();
        if ~isempty(pyenv)
          kwargs.python_call = pyenv
        end
      end

      proc = call(args, kwargs, 'module_name', module_name);

      workspace = py.msurrogate.cookie_setup(pyraw(proc.cookie_dict));
      self.auto_stop = auto_stop;
      self.workspace = dict2map(workspace);
    end

    function connect_cookie(self, fname, varargin)
      import msurrogate.*
      if self.auto_stop
        self.stop();
      end
      [args, kwargs] = collectargs(varargin);

      raw = getfielddefault(kwargs, 'rawtext', false);
      auto_stop = getfielddefault(kwargs, 'auto_stop', false);

      if raw
        text = fname;
      else
        text = fileread(fname);
      end

      %setup can take text
      workspace = py.msurrogate.cookie_setup(text);
      self.auto_stop = auto_stop;
      self.workspace = dict2map(workspace);
    end

    function [varargout] = subsref(self, ref)
      import msurrogate.*
      switch ref(1).type
          case '.'
            name = ref(1).subs;

            if any(strcmp(name, builtin('methods', self)))
              [varargout{1:nargout}] = builtin('subsref', self, ref);
              return
            end

            uri = self.workspace(name);
            val = pyrowrap(py.Pyro4.Proxy(uri), false, self);

            if not(isempty(ref(2:end)))
              [varargout{1:nargout}] = subsref(val, ref(2:end));
             else
               [varargout{1:nargout}] = val;
            end
          case '()'
            args_raw = ref(1).subs;
            name = args_raw;
            uri = self.workspace(name);
            val = pyrowrap(py.Pyro4.Proxy(uri), false, self);

            if not(isempty(ref(2:end)))
              [varargout{1:nargout}] = subsref(val, ref(2:end));
            else
              [varargout{1:nargout}] = val;
            end
          otherwise
            error('only indexes as an object');
       end
    end
  end

  methods (Static)
    function val = set_python_call(callstr_new)
      persistent callstr
      switch nargin
      case 0
        val = callstr;
      case 1
        val = callstr;
        callstr = callstr_new;
      end
    end

    function env = set_python_env(varargin)
      persistent envmap

      if isempty(envmap)
        envmap = containers.Map();
      end

      s = struct(varargin{:});
      fields = fieldnames(s);
      for idx = 1:numel(fields)
        field = fields{idx};
        v = s.(field);
        envmap(field) = v;
      end

      env = envmap;
    end
  end

  methods (Access = protected)
  end

  %methods
  %end
end



