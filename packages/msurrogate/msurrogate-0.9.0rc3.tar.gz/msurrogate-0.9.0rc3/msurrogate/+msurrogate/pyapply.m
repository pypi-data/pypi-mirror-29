% A way to inject kwargs into functions from matlab: python's apply function.
% Too bad python3 kills it, so here we store it and build one using eval
% the only clearer way would be to import a stub and have a companion library for python to import from
function val = pyapply(func, args, kwargs)
  persistent pfunc

  if isempty(pfunc)
    pfunc = @py.apply;
    try
      %now test it out
      pfunc(@py.list);
    catch ME
      switch ME.identifier
      case 'MATLAB:undefinedVarOrClass'
          %OK, might be on python 3 which doesn't build this in
          %so build it using eval (GROSS)
        d = py.dict();
        pfunc = py.eval('lambda f, a, kw : f(*a, **kw)', d, d);
      otherwise
        rethrow(ME)
      end
    end
  end

  val = pfunc(func, args, kwargs);
end
