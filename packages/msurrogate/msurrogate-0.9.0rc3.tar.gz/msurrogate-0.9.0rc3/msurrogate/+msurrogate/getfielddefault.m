function val = getfielddefault(s, field, default)
  if isfield(s, field)
    val = s.(field);
  else
    val = default;
  end
end

