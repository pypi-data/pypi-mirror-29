pysdl-gpu
=========

pysdl-gpu is a wrapper around the SDL_gpu library. It depends on PySDL2,
and it uses ctypes.

The SDL_gpu library, as well as its documentation, can be found here:
https://github.com/grimfang4/sdl-gpu

Feel free to report bugs or make pull requests here:
https://bitbucket.org/Jjp137/pysdl-gpu

Note that this library is intended to match the sdl_gpu.h header as closely
as possible, and thus, following PEP-8 is less of a priority.

Usage
-----

pysdl-gpu requires SDL2 and SDL_gpu to be installed on your system.
Alternatively, the environment variable ``PYSDL2_DLL_PATH`` can be used to
point pysdl-gpu to the location of the SDL2 and SDL_gpu libraries.

Once installed, simply import the library::

    import sdlgpu

Refer to SDL_gpu's documentation for a list of available functions, enums,
and structures.

Licensing
---------

pysdl-gpu is licensed under the terms of the MIT License. For more details
on the terms of this license, refer to LICENSE.txt.

