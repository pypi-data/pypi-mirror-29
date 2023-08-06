# encoding: utf-8


import inspect


def check_function_call_integrity(func,
                                  *args,
                                  **kwargs):

    error = False

    all_args, varargs, varkw, defaults = inspect.getargspec(func)

    arguments = []

    positional_args = [(arg, value) for arg, value in zip(all_args, args)]
    positional_arg_keys = [arg for arg, _ in positional_args]

    remaining_positional_args = args[len(positional_args):]

    number_of_optionals = len(defaults)
    mandatory_args = all_args[:-number_of_optionals]
    optional_args = all_args[-number_of_optionals:]

    for arg, value in positional_args:
        arguments.append(u'{arg}={value} (arg)'
                         .format(arg=arg,
                                 value=repr(value)))

    for arg in mandatory_args:
        try:
            if arg not in positional_arg_keys:
                arguments.append(u'{arg}={value} (kwarg)'
                                 .format(arg=arg,
                                         value=repr(kwargs[arg])))
            else:
                arguments.append(u'{arg}={value} (Err: multiple values for kwarg)'
                                 .format(arg=arg,
                                         value=repr(kwargs[arg])))
                error = True
        except KeyError:
            if arg not in positional_arg_keys:
                error = True
                arguments.append(u'{arg}=? (Err: mandatory parameter missing)'
                                 .format(arg=arg))

    for arg, default in zip(optional_args, defaults):
        try:
            if arg not in positional_arg_keys:
                arguments.append(u'{arg}={value} (kwarg)'
                                 .format(arg=arg,
                                         value=repr(kwargs[arg])))
            else:
                arguments.append(u'{arg}={value} (Err: multiple values for keyword argument)'
                                 .format(arg=arg,
                                         value=repr(kwargs[arg])))
                error = True
        except KeyError:
            if arg not in positional_arg_keys:
                arguments.append(u'{arg}={default} (default)'
                                 .format(arg=arg,
                                         default=repr(default)))

    for value in remaining_positional_args:
        arguments.append(u'{value} (from *args)'
                         .format(value=repr(value)))

    for kwarg in kwargs:
        if kwarg in mandatory_args or kwarg in optional_args:
            continue
        arguments.append(u'{arg}={value} (from **kwargs)'
                         .format(arg=kwarg,
                                 value=repr(kwargs[kwarg])))

    indent = u',\n ' + u' ' * len(func.func_name)
    signature = (u'{func_name}({arguments})'
                 .format(func_name=func.func_name,
                         arguments=indent.join(arguments)))
    if error:
        raise TypeError(u'Bad call signature:\n' + signature)

    return signature


if __name__ == u"__main__":
    def function(a,
                 b=None,
                 c=1,
                 *args,
                 **kwargs):
        pass

    print(check_function_call_integrity(function, 1, 2, 3, 4, d=1, c=3))
    pass
