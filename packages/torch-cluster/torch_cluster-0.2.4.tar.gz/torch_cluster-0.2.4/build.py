import subprocess

import torch
from torch.utils.ffi import create_extension

headers = ['torch_cluster/src/cpu.h']
sources = ['torch_cluster/src/cpu.c']
include_dirs = ['torch_cluster/src']
define_macros = []
extra_objects = []
with_cuda = False

if torch.cuda.is_available():
    subprocess.call('./build.sh')

    headers += ['torch_cluster/src/cuda.h']
    sources += ['torch_cluster/src/cuda.c']
    include_dirs += ['torch_cluster/kernel']
    define_macros += [('WITH_CUDA', None)]
    extra_objects += ['torch_cluster/build/kernel.so']
    with_cuda = True

ffi = create_extension(
    name='torch_cluster._ext.ffi',
    package=True,
    headers=headers,
    sources=sources,
    include_dirs=include_dirs,
    define_macros=define_macros,
    extra_objects=extra_objects,
    with_cuda=with_cuda,
    relative_to=__file__)

if __name__ == '__main__':
    ffi.build()
