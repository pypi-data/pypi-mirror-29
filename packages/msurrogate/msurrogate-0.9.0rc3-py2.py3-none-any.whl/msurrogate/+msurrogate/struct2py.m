function val = struct2py(object)
  import msurrogate.*
  pydict = py.dict();
  fields = fieldnames(object);
  for i = 1:numel(fields)
    field = fields{i};
    obj = object.(field);
    obj = mat2py(obj);
    pydict.setdefault(field, obj);
  end
  val = pydict;
end

