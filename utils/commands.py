def format_signature(command):
    signature = command.signature
    args = []
    i = 0
    while i < len(signature):
        if signature[i] == "<":
            end_idx = signature.find(">", i)
            arg = signature[i + 1 : end_idx]
            args.append(f"<\u001b[34m{arg}\u001b[0m>")
            i = end_idx + 1
        elif signature[i] == "[":
            end_idx = signature.find("]", i)
            arg = signature[i + 1 : end_idx]
            args.append(f"[\u001b[36m{arg}\u001b[0m]")
            i = end_idx + 1
        else:
            i += 1
    return " ".join(args)


def format_command(command):
    q = "`"
    signature = format_signature(command)
    prefix_name = f"s!\u001b[1m{command.qualified_name}\u001b[0m"
    return f"{q*3}ansi\n{prefix_name} {signature}\n{q*3}"


def get_arguments(command):
    params = command.app_command._params
    arguments = {}

    for param in params:
        param = params.get(param)
        arguments[param.name] = param.description.message

    return arguments
