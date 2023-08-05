function val = cell2py(object)
  import msurrogate.*
  pylist = py.list();
  for i = 1:numel(object)
    val = object{i};
    val = mat2py(val);
    pylist.append(val);
  end
  val = pylist;
end

