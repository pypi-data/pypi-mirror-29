

class UnsignedIntegerCoder(VariableCoder):

    def encode(self, variable, name=None):
        dims, data, attrs, encoding = unpack_for_encoding(variable)

        if encoding.get('_Unsigned', False):
            pop_to(encoding, attrs, '_Unsigned')
            signed_dtype = np.dtype('i%s' % data.dtype.itemsize)
            if '_FillValue' in attrs:
                new_fill = signed_dtype.type(attrs['_FillValue'])
                attrs['_FillValue'] = new_fill
            data = duck_array_ops.around(data).astype(signed_dtype)

        return Variable(dims, data, attrs, encoding)

    def decode(self, variable, name=None):
        dims, data, attrs, encoding = unpack_for_decoding(variable)

        if '_Unsigned' in attrs:
            unsigned = pop_to(attrs, encoding, '_Unsigned')

            if data.dtype.kind == 'i':
                if unsigned:
                    unsigned_dtype = np.dtype('u%s' % data.dtype.itemsize)
                    transform = partial(np.asarray, dtype=unsigned_dtype)
                    data = lazy_elemwise_func(data, transform, unsigned_dtype)
                    if '_FillValue' in attrs:
                        new_fill = unsigned_dtype.type(attrs['_FillValue'])
                        attrs['_FillValue'] = new_fill
            else:
                warnings.warn("variable %r has _Unsigned attribute but is not "
                              "of integer type. Ignoring attribute." % name,
                              SerializationWarning, stacklevel=3)

        return Variable(dims, data, attrs, encoding)
