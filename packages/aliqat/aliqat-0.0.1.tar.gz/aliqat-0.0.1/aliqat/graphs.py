#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 3/8/18
"""
.. currentmodule:: grids
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Say something descriptive about the 'grids' module.
"""

from enum import IntFlag


class CharClass(IntFlag):
    EMPTY = 1
    ALPHA = 2
    DIGIT = 4
    SPECIAL = 8
    ANY = 15

    @property
    def char(self) -> str:
        """
        Get the single-character string representation for this enumerated
        value.

        :return: the single-character string representation
        """
        try:
            return CharClass.from_int(self)
        except KeyError:
            raise RuntimeError('No character is defined.')

    @staticmethod
    def from_int(i: int):
        """
        Get the single-character string representation for an enumerated
        value.

        :param i: the integer value
        :return: the single-character string representation
        :raises KeyError: if no single-character string representation is
        defined
        """
        return {
            CharClass.EMPTY: '∅',
            CharClass.ALPHA: 'α',
            CharClass.DIGIT: 'ℝ',
            CharClass.SPECIAL: '¿',
            CharClass.ANY: 'ω',
            CharClass.ALPHA | CharClass.DIGIT: 'π',
            CharClass.ALPHA | CharClass.EMPTY: '∀',
            CharClass.ALPHA | CharClass.SPECIAL: 'غ',
            CharClass.DIGIT | CharClass.EMPTY: '𝕌',
            CharClass.DIGIT | CharClass.SPECIAL: '⊕',
            CharClass.SPECIAL | CharClass.EMPTY: '٭',
            CharClass.ANY ^ CharClass.EMPTY: '●',
            CharClass.ANY ^ CharClass.ALPHA: '◒',
            CharClass.ANY ^ CharClass.DIGIT: '◔',
            CharClass.ANY ^ CharClass.SPECIAL: '◎'
        }[i]

class Graph(object):

    def __init__(self, s: str):  # TODO: Optional parameter to set minimum size.
        self._graph = list(s) if s is not None else [' ']

    def __iter__(self):
        return iter(self._graph)

    def conflate(self, other: 'Graph'):
        i = 0
        for c in other:
            # Conflate the current value at the specified index in this graph
            # with the value from the other graph.
            try:
                self._graph[i] = self._conflate(self._graph[i], c)
            except IndexError:
                self._graph.extend(self._conflate(self._graph[i], c))
            i += 1

    @staticmethod
    def _conflate(a: str or CharClass, b: str or CharClass):
        # If the values are equal, return either one.
        if a == b:
            return a
        t = (a, b)  # Collect the values.
        # If one of them is None, return the other one.
        if None in t:
            return [c for c in t if c is not None][0]
        # Make sure we're dealing with single characters from here on in.
        if isinstance(a, str) and len(a) != 1:
            raise ValueError('a must be a single character, flag, or None.')
        if isinstance(b, str) and len(b) != 1:
            raise ValueError('b must be a single character, flag, or None.')
        # Encode each value.
        a_enc = Graph._encode(a)
        b_enc = Graph._encode(b)
        # The conflation result is a's encoding OR (binary) b's encoding.
        return a_enc | b_enc


    @staticmethod
    def _encode(c: str) -> CharClass:
        # TODO: Move special lists of characters to a more visible location!!!
        # If the argument is already character class (or just an int)...
        if isinstance(c, int):
            return c  # ...we already have our answer.
        if len(c) != 1:  # Sanity check!  # TODO: Use common logic for check.
            raise ValueError('c must be a single character or None.')
        # Classify the input.
        if c is None or c in [' ', '\r', '\n']:  # TODO: Move character lists!
            return CharClass.EMPTY
        elif c.isdigit():
            return CharClass.DIGIT
        elif c.isalpha():
            return CharClass.ALPHA
        elif c in ['+', '-', ',', ':', '*', '!', '?', '<', '>', '.']:  # TODO: Move character lists!
            return CharClass.SPECIAL
        else:
            return CharClass.ANY

    @staticmethod
    def _str(i: str or CharClass):
        try:
            return CharClass.from_int(i)
        except KeyError:
            return i

    def __str__(self):
        x = [self._str(i) for i in self._graph]
        return ''.join([self._str(i) for i in self._graph])





def graph(s: str) -> Graph:
    pass