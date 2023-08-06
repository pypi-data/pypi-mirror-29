#!/usr/bin/env python3
"""
:mod:`text_stream` -- Text Data Model
=====================================

.. module text
   :platform: Unix, Windows, Mac, Linux
   :synopsis: An interface to interact with a file, a multi-line string, or standard input.
.. moduleauthor:: Qi Zhang <qz2280@columbia.edu>
"""

from abc import ABC, abstractmethod
from io import StringIO
from pathlib import PurePath, Path
from typing import Optional, Iterator, Tuple, Union

from lazy_property import LazyProperty

# ========================================= What can be exported? =========================================
__all__ = ['TextStream', 'TextFileStream', 'make_text_stream']


class TextStreamABC(ABC):
    """
    This is a general model for text streams.
    A text stream consists of one or more lines of text that can be written to a text-oriented display
    so that they can be read. When reading from a text stream, the program reads a *newline* at
    the end of each line. When writing to a text stream, the program writes a *newline* to signal the
    end of a line. [#f]_

    You can specify nothing in ``TextStream`` instance creation procedure,
    then data will be read from interactive input, you can press <Ctrl+D> to end this input.
    If you give it a string, with *newline* separator specified by ``'\\n'`` or ``'\\r\\n'``,
    then the string will be parsed by this separator.
    If you give a file path in *inp*, and if it is valid, then the file will be read.

    .. [#f] Referenced from `here <https://docs.microsoft.com/en-us/cpp/c-runtime-library/text-and-binary-streams>`_.
    """

    @property
    @abstractmethod
    def stream(self) -> StringIO:
        ...

    def generator(self) -> Iterator[str]:
        """
        Create a generate that iterates the whole content of the file or string.

        :return: An iterator.
        """
        stream = self.stream  # In case that ``self.stream`` is changed.
        stream.seek(0)
        for line in stream:
            yield line

    def generator_telling_position(self) -> Iterator[Tuple[str, int]]:
        """
        Create a generate that iterates the whole content of the file or string, and also tells which offset is now.

        :return: An iterator.
        """
        stream = self.stream  # In case that ``self.stream`` is changed.
        stream.seek(0)
        for line in stream:
            yield line, stream.tell()

    def generator_starts_from(self, offset, whence: Optional[int] = 0) -> Iterator[str]:
        """

        :param offset:
        :param whence:
        :return:
        """
        stream = self.stream  # In case that ``self.stream`` is changed.
        stream.seek(offset, whence)
        for line in stream:
            yield line

    def generator_between(self, begin: int, end: int) -> Iterator[str]:
        """

        :param begin:
        :param end:
        :return:
        """
        s: str = self.content[begin:end + 1]
        for line in s:
            yield line

    @LazyProperty
    def content(self) -> str:
        """
        Read the whole file or string, and return it.

        :return: The whole contents of the file or the string.
        """
        return self.stream.getvalue()


class TextStream(TextStreamABC):
    """
    A subclass of class ``TextStreamABC``.

    :param inp: Input, can be a string, an ``StringIO`` instance, or ``None`` (which means read from standard input).
    """

    def __init__(self, inp: Union[str, StringIO, None] = None):
        if inp is None:
            self.__stream = StringIO(_user_input())
        elif isinstance(inp, str):
            self.__stream = StringIO(inp)
        elif isinstance(inp, StringIO):
            self.__stream = inp
        else:
            raise TypeError("Unsupported type! The only recognized types are ``str`` and ``io.StringIO`` and ``None``!")

    @property
    def stream(self) -> StringIO:
        """
        Read-only property.

        :return:
        """
        return self.__stream

    @property
    def infile_path(self) -> Optional[PurePath]:
        """
        Read-only property.

        :return:
        """
        return None


class TextFileStream(TextStreamABC):
    """
    :param inp: Input, can only be a string.
        If the *inp* is a valid file existing on the system, the file the *inp* directs will be used.
    """

    def __init__(self, inp: str):
        if isinstance(inp, str):
            if Path(inp).expanduser().is_file():
                self.__infile_path = inp
                with open(inp) as f:
                    self.__stream = StringIO(f.read())
            else:
                raise FileNotFoundError("The *inp* argument '{0}' is not a valid file!".format(inp))
        else:
            raise TypeError("Unsupported type! The only recognized type is ``str``!")

    @property
    def stream(self) -> StringIO:
        """
        Read-only property.

        :return:
        """
        return self.__stream

    @property
    def infile_path(self) -> Optional[PurePath]:
        """
        Read-only property.

        :return:
        """
        return Path(self.__infile_path).expanduser()


def _user_input() -> str:
    """
    A helper function which waits for user multi-line input.

    :return:
    """
    lines = []
    try:
        while True:
            line = input()
            if line != '':
                lines.append(line)
            else:
                break
    except (EOFError, KeyboardInterrupt):
        return '\n'.join(lines)


def make_text_stream(inp: Union[str, StringIO, None] = None) -> Optional[TextStreamABC]:
    """
    A helper function that determines which class is to be used.

    :param inp:
    :return:
    """
    if isinstance(inp, str):
        if Path(inp).expanduser().is_file():
            return TextFileStream(inp)
        return TextStream(inp)
    elif isinstance(inp, StringIO):
        return TextStream(inp)
    elif inp is None:
        return TextStream(_user_input())
    else:
        raise TypeError("Unsupported type! The only recognized types are ``str`` and ``io.StringIO`` and ``None``!")
