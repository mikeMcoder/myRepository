#!C:\Python22\python.exe

"""PyShellApp is a python shell application."""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
__cvsid__ = "$Id: SunShell.py,v 1.3 2008/11/13 01:48:34 rkbatra Exp $"
__version__ = "$Revision: 1.3 $"[11:-2]


from wxPython.wx import *
from wxPython.lib.PyCrust.shell import ShellMenu
from wxPython.lib.PyCrust.shell import Shell
from wxPython.lib.PyCrust.interpreter import Interpreter
from code import InteractiveInterpreter
import os
import sys
import time

python_path = os.path.abspath('..')
sys.path.append(python_path)
os.environ['path'] += ';' + python_path

VERSION = '4.0.0'
COPYRIGHT = 'Copyright © 2013, Emcore Corporation.'

import ITLA.ITLA
from ITLA.Register import Register
from ITLA.Packet import ModuleBoundPacket
from ITLA.Packet import HostBoundPacket

it = ITLA.ITLA.ITLA()

class SunInterpreter(Interpreter):
    def __init__(self, locals=None, rawin=None, \
                 stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        """Create an interactive interpreter object."""
        InteractiveInterpreter.__init__(self, locals=locals)
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        if rawin:
            import __builtin__
            __builtin__.raw_input = rawin
            del __builtin__
        self.introText = 'SunShell %s %s\n' % (VERSION, COPYRIGHT)
        self.introText += 'Use "it.connect()" to establish a connection.\n'
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = '>>> '
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = '... '
        self.more = 0
        # List of lists to support recursive push().
        self.commandBuffer = []
        self.startupScript = os.environ.get('PYTHONSTARTUP')
        
    
class SunMenu(ShellMenu):
    def createMenus(self):
        ShellMenu.createMenus(self)
        self.shell.autoCompleteIncludeMagic = 0
        self.shell.autoCompleteIncludeSingle = 0
        self.shell.autoCompleteIncludeDouble = 0
        self.shell.autoComplete = 1

    def OnAbout(self, event):
        title = 'About SunShell'
        about = '''
SunShell %s © 2013 Emcore Corporation All Rights Reserved.

Optical Products Division
8674 Thornton Avenue
Newark, CA 94560

%s

This SunShell ("Software") is furnished under license and may
only be used or copied in accordance with the terms of that license. No
license, express or implied, by estoppel or otherwise, to any intellectual
property rights is granted by this document. The Software is subject to change
without notice, and should not be construed as a commitment by Emcore
Corporation to market, license, sell or support any product or technology.
Unless otherwise provided for in the license under which this Software is
provided, the Software is provided AS IS, with no warranties of any kind,
express or implied. Except as expressly permitted by the Software license,
neither Emcore Corporation nor its suppliers assumes any responsibility or
liability for any errors or inaccuracies that may appear herein. Except as
expressly permitted by the Software license, no part of the Software may be
reproduced, stored in a retrieval system, transmitted in any form, or
distributed by any means without the express written consent of Emcore
Corporation.

        ''' % (VERSION, COPYRIGHT)
        
        dialog = wxMessageDialog(self, about, title, wxOK | wxICON_INFORMATION)
        dialog.ShowModal()
        dialog.Destroy()

    def OnAutoCompleteShow(self, event):
        pass
    
    def OnAutoCompleteIncludeMagic(self, event):
        pass

    def OnAutoCompleteIncludeSingle(self, event):
        pass
    
    def OnAutoCompleteIncludeDouble(self, event):
        pass

class SunFrame(wxFrame, SunMenu):
    def __init__(self, parent=None, id=-1, title='SunShell', \
                 pos=wxDefaultPosition, size=wxDefaultSize, \
                 style=wxDEFAULT_FRAME_STYLE, locals=None, \
                 InterpClass=None, *args, **kwds):
        """Create a SunFrame instance."""
        wxFrame.__init__(self, parent, id, title, pos, size, style)
        intro = 'Welcome SunShell'
        self.CreateStatusBar()
        #self.SetStatusText(intro.replace('\n', ', '))
        icon = wxIcon('SunShell.ico', wxBITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.shell = Shell(parent=self, id=-1, #introText=intro, \
                           locals=locals, InterpClass=InterpClass, \
                           *args, **kwds)
        # Override the shell so that status messages go to the status bar.
        self.shell.setStatusText = self.SetStatusText
        self.createMenus()
    
class App(wxApp):
    """PyShell standalone application."""

    def OnInit(self):
        locals = {'it'      : it,
                  'Register': Register,
                  'ModuleBoundPacket'  : ModuleBoundPacket,
                  'HostBoundPacket'  : HostBoundPacket,
                  '__name__': 'SunShell',
                  '__version__':VERSION,
                  '__doc__'     : 'SunShell interactive'
                  }
        self.SunFrame = SunFrame(locals=locals, InterpClass = SunInterpreter, size=(800,600))
        self.SunFrame.SetStatusText('')
        self.SunFrame.Show(true)
        self.SetTopWindow(self.SunFrame)
        # Add the application object to the sys module's namespace.
        # This allows a shell user to do:
        # >>> import sys
        # >>> sys.application.whatever
        sys.application = self
        return true


def main():
    application = App(0)
    application.MainLoop()

if __name__ == '__main__':
    main()



