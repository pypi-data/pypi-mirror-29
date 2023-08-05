Copyright (c) 2016 Chris Mutel and the Paul Scherrer Institut, All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Description-Content-Type: UNKNOWN
Description: Wurst
        =====
        
        |Build Status| |Coverage Status| |Docs|
        
        Show how the sausage is made!
        
        Wurst is a python package for linking and modifying industrial ecology
        models, with a focus on sparse matrices in life cycle assessment. It
        provides the following:
        
        *  Helper functions to filter activities and exchanges
        *  Helper functions to link exchanges
        *  Transformation functions to change markets, change input
           efficiencies, and change emissions
        *  Data IO with `Brightway2 <https://brightwaylca.org/>`__
        *  Logging framework and a log browser
        
        See also the separate `wurst
        examples <https://github.com/IndEcol/wurst-examples>`__ repository.
        
        Installation
        ------------
        
        Wurst can be installed in its development version using Anaconda. First,
        follow the `Brightway2 installation
        instructions <https://docs.brightwaylca.org/installation.html#quickstart>`__.
        Then, in the *same environment as Brightway*, do the following:
        
        ::
        
            conda install -c cmutel -c conda-forge -c konstantinstadler country_converter constructive_geometries
            pip install https://github.com/IndEcol/wurst/archive/master.zip
        
        License
        -------
        
        BSD 2-clause license. Contributions are welcome!
        
        Authors
        -------
        
        *  Chris Mutel
        *  Brian Cox
        
        TODO
        ----
        
        *  Review BW2 IO code to make sure all needed fields are present in
           newly-created and modified databases
        *  Parameterized exchanges (e.g. electricity sector)
        *  Check logging on all transformation functions
        *  Log browser web app
        *  Fill out geo linking tests
        
        .. |Build Status| image:: https://travis-ci.org/IndEcol/wurst.svg?branch=master
           :target: https://travis-ci.org/IndEcol/wurst
        .. |Coverage Status| image:: https://coveralls.io/repos/github/IndEcol/wurst/badge.svg?branch=master
           :target: https://coveralls.io/github/IndEcol/wurst?branch=master
        .. |Docs| image:: https://readthedocs.org/projects/wurst/badge/?version=latest
           :target: https://wurst.readthedocs.io/
        
Platform: UNKNOWN
Classifier: Development Status :: 3 - Alpha
Classifier: Intended Audience :: End Users/Desktop
Classifier: Intended Audience :: Developers
Classifier: Intended Audience :: Science/Research
Classifier: License :: OSI Approved :: BSD License
Classifier: Operating System :: MacOS :: MacOS X
Classifier: Operating System :: Microsoft :: Windows
Classifier: Operating System :: POSIX
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 3 :: Only
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
Classifier: Programming Language :: Python :: 3.6
Classifier: Topic :: Scientific/Engineering :: Information Analysis
Classifier: Topic :: Scientific/Engineering :: Mathematics
