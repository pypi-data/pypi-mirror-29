function dict = map2dict(map)
  import msurrogate.*

  dict = py.dict();
  dict = pywrap(dict);

  for k = keys(map)
    v = map(k);
    dict{k} = v;
  end
end

