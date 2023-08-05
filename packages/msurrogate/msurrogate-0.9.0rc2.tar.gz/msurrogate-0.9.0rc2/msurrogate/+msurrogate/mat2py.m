function [varargout] = mat2py(object)
  import msurrogate.*
  if isnumeric(object)
    %all numeric types (including complex) convert correctly to the python type
    %for indexes and such, be careful to convert to int first 
    if isscalar(object) == 1
      if int32(object) == object
        varargout{1} = int32(object);
      else
        varargout{1} = object;
      end
      return
    end

    %the conversion through python.array works well into numpy for integer types as well
    %only complex types need conversion
    if isreal(object)
      varargout{1} = mat2np(object);
    else
      %surprisingly, this works
      varargout{1} = mat2np(real(object)) + 1j * mat2np(imag(object));
    end
  else
    switch class(object)
    case 'msurrogate.pywrap'
      varargout{1} = pyraw(object);
    case 'msurrogate.pyrowrap'
      varargout{1} = pyraw(object);
    case 'struct'
      varargout{1} = struct2py(object);
    case 'cell'
      varargout{1} = cell2py(object);
    case 'char'
      varargout{1} = object;
    case 'containers.Map';
      varargout{1} = map2dict(object);
    otherwise
      varargout{1} = object;
    end
  end
end
