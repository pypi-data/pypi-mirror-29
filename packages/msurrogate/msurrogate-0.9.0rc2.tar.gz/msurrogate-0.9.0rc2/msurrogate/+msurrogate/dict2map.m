function map = dict2map(object)
  import msurrogate.*

  map = containers.Map();
  kv_list = object.items();
  for kv = kv_list
    kv = kv{1};
    k = kv{1};
    v = kv{2};
    map(py2mat(k)) = py2mat(v);
  end
end

