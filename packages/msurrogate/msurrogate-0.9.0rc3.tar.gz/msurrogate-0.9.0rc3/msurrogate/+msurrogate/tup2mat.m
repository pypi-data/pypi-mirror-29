function [varargout] = tup2mat(object, handle)
  import msurrogate.*
  ocells = cell(object);
  try
    varargout{1} = cell2mat(ocells);
  catch ME
      switch ME.identifier
      case 'MATLAB:cell2mat:MixedDataTypes'
        varargout{1} = cellfun(@(obj) py2mat(obj, handle), ocells, 'UniformOutput', false);
      case 'MATLAB:cell2mat:UnsupportedCellContent'
        varargout{1} = cellfun(@(obj) py2mat(obj, handle), ocells, 'UniformOutput', false);
      otherwise
        ME.identifier
        error(ME)
      end
  end
end

