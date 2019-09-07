class TExException(Exception):
    def __init__(self,Msg,Category=None):
        self.Msg = Msg
        Exception.__init__(self,Msg)

    def __str__(self):
        retstr = "Exception %s : "%self.__class__.__name__ + Exception.__str__(self)
        return retstr
    __repr__ = __str__

class TExWarning(Warning):
    def __init__(self,Msg,Category=None):
        self.Msg = Msg
        Warning.__init__(self,Msg)

    def __str__(self):
        retstr = "Warning %s : "%self.__class__.__name__ + Warning.__str__(self)
        return retstr
    __repr__ = __str__

class CommunicationError(TExException):pass
class WindowsError(TExException):pass
class TimeOutError(TExException):pass


class FrameworkError(TExException):pass
class FrameworkWarning(TExWarning):pass

class Deprecated(FrameworkWarning):pass
class NotSupported(Deprecated):pass
class NotImplemented(FrameworkError):pass
class ProgrammerError(FrameworkError):pass

class InstrumentException(CommunicationError):pass
class GPIBException(InstrumentException):pass

class GPIBTimeout(TimeOutError,GPIBException):pass #used by instrument drivers for GPIB comm
class TCP_IPTimeout(TimeOutError):pass  #used by instrument drivers for TCPIP comm
class SerialTimeout(TimeOutError):pass  #used by instrument drivers for serial comm

class ApplicationException(TExException):pass
class ApplicationDriverTimeout(TimeOutError,ApplicationException):pass    # Used by applications when polling some condition and loop condition is true > timeout secs.

class FirmwareException(ApplicationException):pass



warn = 1

def _warn(msg):
    import warnings
    if warn:
        warnings.warn(msg + " This will raise Exception in TEx 5.2 or >.",TExWarning,3)
        print msg
    else:
        raise ProgrammerError(msg)
