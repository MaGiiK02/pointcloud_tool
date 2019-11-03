from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CppExtension
import glob
import builtins

builtins.__SETUP_DONE__ = True

_ext_src_root = "./vcg_tools/sampling"
_ext_sources_sampling = glob.glob("{}/*.cpp".format(_ext_src_root))

setup(
	name='_VcgTools',
	ext_modules=[
		CppExtension(
			name='_vcg_sampling',
			sources=_ext_sources_sampling,
			extra_compile_args=['-g', '-I./vcg/eigenlib', '-I./vcg/wrap', '-I./vcg'])
	],
	cmdclass={
		'build_ext': BuildExtension
	}
)
