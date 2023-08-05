function [args, kwargs] = collectargs(args_raw)
    %subtract two to also avoid the colon itself
    args = {};
    kwargs = struct();
    idx_kw = numel(args_raw) + 1;
    for i = 1:numel(args_raw)
      arg = args_raw{i};
      switch class(arg)
        case 'char'
          %start the keyword arguments
          idx_kw = i;
          break
        case 'struct'
          %add to the keyword arguments
          kwargs = mergestructs(kwargs, arg);
        case 'cell'
          %add to the arguments
          args = [args, arg];
        otherwise
          disp(arg)
          error('python calling kwargs section starts with unknown object, must be cell to add to args, struct to add to kwargs, or char to begin individual kwargs')
      end
    end

    i = idx_kw;
    try
      while i <= numel(args_raw)
        field = args_raw{i};
        val = args_raw{i + 1};
        kwargs.(field) = val;
        i = i + 2;
      end
    catch ME
      switch ME.identifier
      case 'MATLAB:badsubscript'
        error('Unbalanced keyword arguments. It is also possible that string arguments are not inside a cell array. Calling convention for python objects is ({args...}, kwstruct, "key", value, "key", value...)')
      case 'MATLAB:mustBeFieldName'
        error('Keyword argument wrong type or unbalanced keyword arguments. It is also possible that arguments are not inside a cell array. Calling convention for python objects is ({args...}, kwstruct, "key", value, "key", value...)')
      case 'MATLAB:AddField:InvalidFieldName'
        rethrow(ME)
      otherwise
        disp(ME)
        rethrow(ME)
      end
    end
end

function out = mergestructs(a, b)
                          %uses the immutability of structs to assign a into out
  out = a;
  fields = fieldnames(b);
  for i = 1:numel(fields)
    field = fields{i};
    out.(field) = b.(field);
  end
end
