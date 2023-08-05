to WMO WOUDC data services
Home-page: https://github.com/woudc/pywoudc
Author: Meteorological Service of Canada
Author-email: tom.kralidis@canada.ca
License: MIT
Description-Content-Type: UNKNOWN
Description: |Build Status| |Build status| |Downloads this month on PyPI| |Latest
        release| |License|
        
        pywoudc
        =======
        
        High level package providing Pythonic access to
        `WOUDC <http://geo.woudc.org>`__ data services.
        
        Overview
        --------
        
        The World Ozone and Ultraviolet Radiation Data Centre (WOUDC) is one of
        six World Data Centres which are part of the `Global Atmosphere
        Watch <http://www.wmo.int/gaw>`__ programme of the World Meteorological
        Organization.
        
        The WOUDC archive is made available via `OGC Web
        Services <http://geo.woudc.org>`__. These web services are publically
        available and can be used within a GIS environment and / or software
        supporting the OGC standards. pywoudc provides a high level library
        using Python idioms (API, data structures) which provides Python
        implementations a simple, straightforward bridge without requiring
        intimate knowledge of the OGC standards.
        
        Installation
        ------------
        
        Requirements
        ~~~~~~~~~~~~
        
        pywoudc requires Python 2.7 or greater. pywoudc works with Python 3.
        
        Dependencies
        ------------
        
        pywoudc requires the `OWSLib <https://geopython.github.io/OWSLib>`__
        library. Installing via ``pip`` or ``easy_install`` will ensure that
        OWSlib is installed as part of pywoudc.
        
        Installing the Package
        ~~~~~~~~~~~~~~~~~~~~~~
        
        .. code:: bash
        
            # via pip
            pip install pywoudc
            # via easy_install
            easy_install pywoudc
        
        Using the API
        -------------
        
        .. code:: python
        
            from pywoudc import WoudcClient
            client = WoudcClient()
        
        Development
        -----------
        
        .. code:: bash
        
            virtualenv pywoudc
            cd pywoudc
            source bin/activate
            git clone https://github.com/woudc/pywoudc.git
            cd pywoudc
            pip install -r requirements.txt
            pip install -r requirements-dev.txt
        
        Running tests
        ~~~~~~~~~~~~~
        
        .. code:: bash
        
            # via distutils
            python setup.py test
            # manually
            python tests/run_tests.py
        
        Code Conventions
        ~~~~~~~~~~~~~~~~
        
        pywoudc code conventions are as per
        `PEP8 <https://www.python.org/dev/peps/pep-0008>`__
        
        Issues
        ------
        
        Issues are managed at https://github.com/woudc/pywoudc/issues
        
        .. |Build Status| image:: https://travis-ci.org/woudc/pywoudc.png?branch=master
           :target: https://travis-ci.org/woudc/pywoudc
        .. |Build status| image:: https://ci.appveyor.com/api/projects/status/02koln2pe4ap5kvd/branch/master?svg=true
           :target: https://ci.appveyor.com/project/tomkralidis/pywoudc
        .. |Downloads this month on PyPI| image:: https://img.shields.io/pypi/dm/pywoudc.svg
           :target: http://pypi.python.org/pypi/pywoudc
        .. |Latest release| image:: https://img.shields.io/pypi/v/pywoudc.svg
           :target: http://pypi.python.org/pypi/pywoudc
        .. |License| image:: https://img.shields.io/github/license/woudc/pywoudc.svg
           :target: https://github.com/woudc/pywoudc
        
Keywords: woudc ozone uv ultra-violet WMO
Platform: all
Classifier: Development Status :: 4 - Beta
Classifier: Environment :: Console
Classifier: Intended Audience :: Developers
Classifier: Intended Audience :: Science/Research
Classifier: License :: OSI Approved :: MIT License
Classifier: Operating System :: OS Independent
Classifier: Programming Language :: Python
Classifier: Topic :: Scientific/Engineering :: Atmospheric Science
Classifier: Topic :: Scientific/Engineering :: GIS
