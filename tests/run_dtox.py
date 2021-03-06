from scripttest import TestFileEnvironment as STE
import os


TESTS_WORKDIR = os.path.abspath("tests-workdir")
DOCKER_IMAGE = os.getenv("DOCKER_IMAGE", "realcundo/dtox:test")


def run(*dtox_args, **kwargs):
    """Runs docker run with optional dtox_args. Returns ProcResult.

    kwargs:
        - tox_ini=<string>: contents of the tox.ini file to be used
        - setup=<func>:     run setup(env) before actual docker run command
    """

    env = STE(TESTS_WORKDIR)

    command = ["docker", "run", "--rm", "-i"]

    # map tests work dir into /src
    command.extend(["-v", '{}:/src:ro'.format(TESTS_WORKDIR)])

    # write tox.ini if specified
    tox_ini = kwargs.pop("tox_ini", None)
    if tox_ini is not None:
        env.writefile("tox.ini", content=tox_ini)

    # run setup function if specified
    setup = kwargs.pop("setup", None)
    if setup is not None:
        setup(env)

    command.append(DOCKER_IMAGE)
    command.extend(dtox_args)

    r = env.run(*command, **kwargs)

    # make sure it isn't a docker run failure
    if "Unable to find image" in r.stderr:
        raise ValueError(r.stderr)

    return r
