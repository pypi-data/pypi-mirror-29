%% @deftypefn  {Function File} {} polynomial ()
%% @deftypefnx {Function File} {} polynomial (@var{a})
%% Create a polynomial object representing the polynomial
%%
%% @example
%% @end example
%%
%% @noindent
%% @end deftypefn
classdef pyrowrap < handle
  properties
    async
    object
    handle
  end
  methods (Access = public)

    function self = pyrowrap(object, async, handle)
      self.handle = handle;
      self.async = async;
      self.object = object;
    end

    function delete(self)
      %should inform pyro that the object is "done"
      try
        %TODO deal with async
        self.object.pyrometa_done()
      catch
        %pass
      end
    end

    function [varargout] = subsref(self, ref)
      import msurrogate.*
      switch ref(1).type
          case '.'
            name = ref(1).subs;

            %this is the method-call form, so don't do the usual subsref recursion and instead do the direct method call
            if all(length(ref) == 2) && all(ref(2).type == '()')
              %check first if this is a direct call that is async or oneway
              switch name
              case 'async_'
                args_raw = ref(2).subs;
                [args, kwargs] = collectargs(args_raw);

                %insert py.None to the args to mean a direct call
                args = mat2py({py.None, args{:}});
                kwargs = mat2py(kwargs);

                             %too dynamic for matlab's interface, so use getattr
                py.Pyro4.async(self.internal(), true);
                call = py.getattr(self.internal(), 'pyrometa_call');
                val = pyapply(call, args, kwargs);
                py.Pyro4.async(self.internal(), false);

                [varargout{1:nargout}] = pyrowrap(val, true, self.handle);
                return
              case 'oneway_'
                args_raw = ref(2).subs;
                [args, kwargs] = collectargs(args_raw);

                %insert name to the args here as indexing is different once a python object
                args = mat2py({py.None, args{:}});
                kwargs = mat2py(kwargs);

                             %too dynamic for matlab's interface, so use getattr
                call = py.getattr(self.internal(), 'pyrometa_call_oneway');
                pyapply(call, args, kwargs);
                varargout{:} = {};
                return
              otherwise
                args_raw = ref(2).subs;
                [args, kwargs] = collectargs(args_raw);

                %insert name to the args here as indexing is different once a python object
                args = mat2py({name, args{:}});
                kwargs = mat2py(kwargs);

                %too dynamic for matlab's interface, so use getattr
                call = py.getattr(self.internal(), 'pyrometa_call');
                val = pyapply(call, args, kwargs);
                [varargout{1:nargout}] = py2mat(val, self.handle);
                return
              end
            elseif (length(ref) == 3) && all(ref(2).type == '.') && all(ref(3).type == '()')
              switch ref(2).subs
              case 'async_'
                args_raw = ref(3).subs;
                [args, kwargs] = collectargs(args_raw);

                %insert name to the args here as indexing is different once a python object
                args = mat2py({name, args{:}});
                kwargs = mat2py(kwargs);

                %too dynamic for matlab's interface, so use getattr
                py.Pyro4.async(self.internal(), true);
                call = py.getattr(self.internal(), 'pyrometa_call');
                val = pyapply(call, args, kwargs);
                py.Pyro4.async(self.internal(), false);

                [varargout{1:nargout}] = pyrowrap(val, true, self.handle);
                return
             case 'oneway_'
                args_raw = ref(3).subs;
                [args, kwargs] = collectargs(args_raw);

                %insert name to the args here as indexing is different once a python object
                args = mat2py({name, args{:}});
                kwargs = mat2py(kwargs);

                %too dynamic for matlab's interface, so use getattr
                call = py.getattr(self.internal(), 'pyrometa_call_oneway');
                pyapply(call, args, kwargs);
                varargout{:} = {};
                return
              end
            end

            %otherwise it is just a typical indexing operation

            call = py.getattr(self.internal(), 'pyrometa_getattr');
            val = pyapply(call, {name}, struct());

            if not(isempty(ref(2:end)))
              val = py2mat(val, self.handle);
              [varargout{1:nargout}] = subsref(val, ref(2:end));
             else
               [varargout{1:nargout}] = py2mat(val, self.handle);
            end

          case '()'
            % function call semantics!
            args_raw = ref(1).subs;

            [args, kwargs] = collectargs(args_raw);

            %add None to form the direct call on the object
            args = mat2py({py.None, args{:}});
            kwargs = mat2py(kwargs);

            call = py.getattr(self.internal(), 'pyrometa_call');
            val = pyapply(call, args, kwargs);
            val = py2mat(val, self.handle);

            if not(isempty(ref(2:end)))
              [varargout{1:nargout}] = subsref(val, ref(2:end));
            else
              varargout{1} = val;
            end
          case '{}'
            % array access semantics!
            args_raw = ref(1).subs;

            if length(args_raw) == 1
              args_raw = args_raw{1};
            end

            args = mat2py(args_raw);
            call = py.getattr(self.internal(), 'pyrometa_getitem');
            val = pyapply(call, args, struct());
            val = py2mat(val, self.handle);

            if not(isempty(ref(2:end)))
              [varargout{1:nargout}] = subsref(val, ref(2:end));
            else
              [varargout{1:nargout}] = val;
            end
          otherwise
            error('only indexes as a struct/object');
       end
    end

    function self = subsasgn(self, ref, val)
      import msurrogate.*

      if not(isempty(ref(2:end)))
        subself = subsref(self, ref(1:1));
        subsasgn(subself, ref(2:end), val);
        return
      end

      switch ref(1).type
        case '.'
          name = ref(1).subs;
          val = mat2py(val);

          call = py.getattr(self.internal(), 'pyrometa_getattr');
          val = pyapply(call, {name, val}, struct());

          return
        case '{}'
          idx = ref(1).subs;
          idx = mat2py(idx);
          val = mat2py(val);

          call = py.getattr(self.internal(), 'pyrometa_getattr');
          pyapply(call, {idx, val}, struct());
          return
        otherwise
          error('only indexes as a struct/object currently');
      end
    end
  end

  methods (Access = protected)
    function object = internal(self)
      if self.async
        object = self.object.value;
        %TODO check that the return is a proxy and error if not
        self.async = false;
        self.object = object;
      else
        object = self.object;
      end
    end
  end

  methods
    function c = char(self)
      call = py.getattr(self.internal(), 'pyrometa_str');
      val = msurrogate.pyapply(call, {}, struct());
      c = char(val);
    end

    function out = dir(self)
      call = py.getattr(self.internal(), 'pyrometa_dir');
      val = msurrogate.pyapply(call, {}, struct());
      out = msurrogate.py2mat(val, self.handle);
    end

    function c = repr(self)
      call = py.getattr(self.internal(), 'pyrometa_repr');
      val = msurrogate.pyapply(call, {}, struct());
      out = msurrogate.py2mat(val, self.handle);
      c = ['<remote>', out];
    end

    function c = disp(self)
      call = py.getattr(self.internal(), 'pyrometa_repr');
      val = msurrogate.pyapply(call, {}, struct());
      out = msurrogate.py2mat(val, self.handle);
      disp(['pyrowrap[', out, ']']);
    end

    function s = struct(self)
      s = msurrogate.dict2struct(self.object);
    end

    function [varargout] = mat2py(self)
      varargout{1} = self.object;
    end

    function out = properties(self)
      out = dir(self);
    end

    function val = pyraw(self)
      val = self.object;
    end
  end
end



