import methods


# Tuples with the name of the arch that will be used in VS, mapped to our internal arch names.
# For Windows platforms, Win32 is what VS wants. For other platforms, it can be different.
def get_platforms():
    return [("Win32", "x86_32"), ("x64", "x86_64")]


def get_configurations():
    return ["editor", "template_debug", "template_release"]


def get_build_prefix(env):
    # Check if env.msvc exists and is False - if not set yet or True, we assume MSVC
    if hasattr(env, "msvc") and not env.msvc:
        return []
    try:
        batch_file = methods.find_visual_c_batch_file(env)
        if not batch_file:
            return []
        return [
            "cmd /V /C",
            "set &quot;plat=$(PlatformTarget)&quot;",
            "^&amp; (if &quot;$(PlatformTarget)&quot;==&quot;x64&quot; (set &quot;plat=x86_amd64&quot;))",
            f"^&amp; call &quot;{batch_file}&quot; !plat!",
            "^&amp;",
        ]
    except Exception:
        # If we can't find the batch file (e.g., VS Insiders), return empty
        # The user is likely already in a VS Developer Command Prompt
        return []
