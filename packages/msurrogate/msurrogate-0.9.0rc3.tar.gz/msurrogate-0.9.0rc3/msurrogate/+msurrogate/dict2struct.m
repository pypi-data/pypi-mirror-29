function s = dict2struct(object)
  import msurrogate.*

  s = struct();
  kv_list = object.items();
  for kv = kv_list
    kv = kv{1};
    k = kv{1};
    v = kv{2};
    s.(k) = v
  end
end

