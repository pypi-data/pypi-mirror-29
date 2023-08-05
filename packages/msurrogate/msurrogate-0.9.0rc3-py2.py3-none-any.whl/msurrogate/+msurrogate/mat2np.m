function val = mat2np(object)
  s = size(object);
  if (length(s) <= 2) && (s(1) == 1)
                                %conversion may be direct
    val = py.numpy.array(object);
  else
                                %reshape first
    arr_np = py.numpy.array(reshape(object, 1, prod(size(object))));
    val = arr_np.reshape(uint32(s));
  end
end
