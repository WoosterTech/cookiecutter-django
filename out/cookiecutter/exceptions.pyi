from _typeshed import Incomplete

class CookiecutterException(Exception): ...
class NonTemplatedInputDirException(CookiecutterException): ...
class UnknownTemplateDirException(CookiecutterException): ...
class MissingProjectDir(CookiecutterException): ...
class ConfigDoesNotExistException(CookiecutterException): ...
class InvalidConfiguration(CookiecutterException): ...
class UnknownRepoType(CookiecutterException): ...
class VCSNotInstalled(CookiecutterException): ...
class ContextDecodingException(CookiecutterException): ...
class OutputDirExistsException(CookiecutterException): ...
class InvalidModeException(CookiecutterException): ...
class FailedHookException(CookiecutterException): ...

class UndefinedVariableInTemplate(CookiecutterException):
    message: Incomplete
    error: Incomplete
    context: Incomplete
    def __init__(self, message, error, context) -> None: ...

class UnknownExtension(CookiecutterException): ...
class RepositoryNotFound(CookiecutterException): ...
class RepositoryCloneFailed(CookiecutterException): ...
class InvalidZipRepository(CookiecutterException): ...
