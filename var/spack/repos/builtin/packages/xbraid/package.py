# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import os.path


class Xbraid(MakefilePackage):
    """XBraid: Parallel time integration with Multigrid"""

    homepage = "https://computation.llnl.gov/projects/parallel-time-integration-multigrid/software"
    url      = "https://computation.llnl.gov/projects/parallel-time-integration-multigrid/download/braid_2.2.0.tar.gz"

    version('2.2.0', '0a9c2fc3eb8f605f73cce78ab0d8a7d9')

    depends_on('mpi')

    def build(self, spec, prefix):
        make('libbraid.a')

    # XBraid doesn't have a real install target, so it has to be done
    # manually
    def install(self, spec, prefix):
        # Install headers
        mkdirp(prefix.include)
        headers = glob.glob('*.h')
        for f in headers:
            install(f, join_path(prefix.include, os.path.basename(f)))

        # Install library
        mkdirp(prefix.lib)
        library = 'libbraid.a'
        install(library, join_path(prefix.lib, library))

        # Install other material (e.g., examples, tests, docs)
        mkdirp(prefix.share)
        install('makefile.inc', prefix.share)
        install_tree('examples', prefix.share.examples)
        install_tree('drivers', prefix.share.drivers)

        # TODO: Some of the scripts in 'test' are useful, even for
        # users; some could be deleted from an installation because
        # they're not useful to users
        install_tree('test', prefix.share.test)
        install_tree('user_utils', prefix.share.user_utils)
        install_tree('docs', prefix.share.docs)

    @property
    def libs(self):
        return find_libraries('libbraid', root=self.prefix,
                              shared=False, recursive=True)
