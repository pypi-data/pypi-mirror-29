function [varargout] = py2mat(object, handle)
  import msurrogate.*
  cname = class(object);
  switch cname
  case 'py.list'
    [varargout{1:nargout}] = tup2mat(object, handle);
  case 'py.tuple'
    [varargout{1:nargout}] = tup2mat(object, handle);
  case 'py.numpy.ndarray'
    if py.numpy.iscomplexobj(object)
      arr_real = py.array.array('d', object.real.flatten());
      arr_real = double(arr_real);
      arr_imag = py.array.array('d', object.imag.flatten());
      arr_imag = double(arr_imag);
      arr = arr_real + 1j * arr_imag;
    else
      arr_real = py.array.array('d', object.real.flatten());
      arr_real = double(arr_real);
      arr = arr_real;
    end
    shape = cell2mat(cell(object.shape));
    if size(shape) < 2
      shape = [1, shape];
    end
    arr = reshape(arr, shape);
    varargout{1} = arr;
  case 'py.str'
    varargout{1} = char(object);
  case 'py.unicode'
    varargout{1} = char(object);
  case 'py.NoneType'
    varargout{1} = object;
  otherwise
    if strcmp(cname(1:3), 'py.')
      if length(cname) >= 14 && strcmp(cname(1:9), 'py.Pyro4.') && strcmp(cname(end-4:end), 'Proxy')
        %it may be a superproxy! so try it out
        if py.hasattr(object, 'pyrometa_getattr')
          varargout{1} = pyrowrap(object, false, handle);
        else
          varargout{1} = pywrap(object, handle);
        end
      else
        varargout{1} = pywrap(object, handle);
      end
    else
      varargout{1} = object;
    end
  end
end

