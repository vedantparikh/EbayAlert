from typing import (
    Text,
    List,
    Union,
    Dict,
)

from abc import (
    ABCMeta,
    abstractmethod,
)

from rest_framework.status import HTTP_404_NOT_FOUND


class BasicError(Exception, metaclass=ABCMeta):
    """Basic class for custom errors."""

    @property
    @abstractmethod
    def status(self) -> int:
        """HTTP status code applicable to this problem, expressed as a int value."""

        raise NotImplementedError

    @property
    @abstractmethod
    def code(self) -> Text:
        """Application-specific error code, expressed as a string value."""

        raise NotImplementedError

    @property
    @abstractmethod
    def title(self) -> Text:
        """Short, human-readable summary of the problem.

        SHOULD NOT change from occurrence to occurrence of the problem.
        """

        raise NotImplementedError

    @property
    @abstractmethod
    def details(self) -> Union[Text, Dict, List]:
        """Any additional information with explanation specific to this occurrence of the problem."""

        raise NotImplementedError


class DomainError(BasicError):
    """sSource class for any error. """

    domain = 'unknown'


class NotFoundError(DomainError):
    """ Raised when no resource with given id can be found. """

    def __init__(self, domain=None, title_overwrite=None):
        if domain:
            self.domain = domain
        title = title_overwrite if title_overwrite else f'No {self.domain} with the given ID exists.'
        super().__init__(HTTP_404_NOT_FOUND, 'not_found', title)
