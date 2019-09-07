'''
NeoPhotonics CONFIDENTIAL
Copyright 2005-2015 NeoPhotonics Corporation All Rights Reserved.

The source code contained or described herein and all documents related to
the source code ("Material") are owned by NeoPhotonics Corporation or its
suppliers or licensors. Title to the Material remains with NeoPhotonics Corporation
or its suppliers and licensors. The Material may contain trade secrets and
proprietary and confidential information of NeoPhotonics Corporation and its
suppliers and licensors, and is protected by worldwide copyright and trade
secret laws and treaty provisions. No part of the Material may be used, copied,
reproduced, modified, published, uploaded, posted, transmitted, distributed,
or disclosed in any way without NeoPhotonics's prior express written permission. 
No license under any patent, copyright, trade secret or other intellectual
property right is granted to or conferred upon you by disclosure or delivery
of the Materials, either expressly, by implication, inducement, estoppel or
otherwise. Any license under such intellectual property rights must be express
and approved by NeoPhotonics in writing.

Include any supplier copyright notices as supplier requires NeoPhotonics to use.

Include supplier trademarks or logos as supplier requires NeoPhotonics to use,
preceded by an asterisk. An asterisked footnote can be added as follows:
*Third Party trademarks are the property of their respective owners.

Unless otherwise agreed by NeoPhotonics in writing, you may not remove or alter this
notice or any other notice embedded in Materials by NeoPhotonics or NeoPhotonics's
suppliers or licensors in any way.

    $Source: /data/development/cvs/Sundial2/Python/SunShell/setup.py,v $
    $Revision: 1.2 $
    $Date: 2008/11/13 01:48:34 $
    $Name: Sundial2_02_01_04_00 $
    
'''

# Compile executable at command line: python setup.py py2exe -w
from distutils.core import setup
import distutils.dir_util as du
import sys
sys.path.append("/Python22/Lib/site-packages") 
import py2exe
name = "SunShell"
setup(name=name,
      version="4.0.0",
      description="Interactive shell to communicate with unit via RS232",
      author="NeoPhotonics",
      author_email="paul_bloch@NeoPhotonics.com",
      scripts=[name + ".py"], 
      package_dir = {'' : '..'},
      packages=['ITLA'],
      options={ 'py2exe' : {'includes' : 'dbhash'}},
      data_files=[(".",["SunShell.ico",
                        "readme.txt",
                        name + ".pdf",
                        "../msvcr70.dll",
                        "../msvcr71.dll",
                       ])]
)

target_path = r'..\..\%s' % name
du.copy_tree(r'dist\%s' % name, target_path)
