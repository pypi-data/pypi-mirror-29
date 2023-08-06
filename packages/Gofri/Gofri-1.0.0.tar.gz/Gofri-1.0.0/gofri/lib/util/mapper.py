def map_object(in_obj, out_obj):
    in_vars = vars(in_obj)
    out_vars = vars(out_obj)
    for var in out_vars:
        if var in in_vars.keys():
            out_vars[var] = in_vars[var]
    out_obj.__dict__ = out_vars
    return out_obj