import functools
import logging
import os
import time
from typing import Any, Callable, Iterable, Optional

logger = logging.getLogger("SABER_Validation")

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass
class DatabaseError(Exception):
    """Custom exception for database errors."""
    pass
class CryptoError(Exception):
    """Custom exception for cryptographic errors."""
    pass

class FileIOError(Exception):
    """Custom exception for file input/output errors."""
    pass

class IntegrityError(Exception):
    """Custom exception for integrity check failures."""
    pass


class validationUtility_SABER:
    @staticmethod
    def condCheck(condtion: bool, msg: str = "Validation condition failed") -> None:
        """Checks a condition and raises ValidationError if false."""
        if not condtion:
            logger.debug(f"Condition check failed: {msg}")
            raise ValidationError(msg)
    @staticmethod
    def typeCheck(checkType: type, variable: Any, variableName: str = "Variable") -> Any:
        if not isinstance(variable, checkType):
            logger.debug(f"Type check failed for {variableName}: Expected {checkType.__name__}, got {type(variable)}")
            raise ValidationError(f"{variableName} must be of type {checkType.__name__}")
        return variable
    @staticmethod
    def pathExists(checkPath: str, name:str = "Path") -> None:
        if not os.path.exists(checkPath):
            logger.debug(f"{name} does not exist: {checkPath}")
            raise FileIOError(f"{name} does not exist: {checkPath}")
   
    @staticmethod
    def emptyCheck(variable: Any, name: str= "Variable") -> None:
        if variable is None:
            logger.debug(f"{name} is empty")
            raise ValidationError(f"{name} is empty")

def handleExceptions(reRaise: bool = True):
    def decorator(fn: Callable):
        @functools.wraps(fn)
        def wrapper(*args,**kwargs):
            try:
                return fn(*args, **kwargs)
            except ValidationError:
                logger.exception(f"ValidationError in {fn.__name__}")
                if reRaise:
                    raise
                return None
            except Exception as e:
                logger.exception(f"Unhandled exceptioon {e} in {fn.__name__}")
                if reRaise:
                    raise ValidationError(str(e))
                return None
            
        return wrapper
    return decorator

def retryOn(exceptionTuple: tuple = (Exception,),retries : int = 3, delay: float = 0.5):
    def decorator(fn: Callable):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            lastExec = None
            for attempt in range(1, retries+1):
                try:
                    return fn(*args, **kwargs)
                except exceptionTuple as e:
                    lastExec = e
                    logger.warning(f"Attempt {attempt}/{retries} failed for {fn.__name__} : {e}")
                if attempt < retries:
                    time.sleep(delay)
            logger.error(f"All retries failed for {fn.__name__}")
            raise lastExec
        return wrapper
    return decorator               