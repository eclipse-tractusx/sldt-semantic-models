#######################################################################
# Copyright (c) 2026 Catena-X Automotive Network e.V.
# Copyright (c) 2026 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This work is made available under the terms of the
# Creative Commons Attribution 4.0 International (CC-BY-4.0) license,
# which is available at
# https://creativecommons.org/licenses/by/4.0/legalcode.
#
# SPDX-License-Identifier: CC-BY-4.0
#######################################################################
# Dependency-free Turtle parser for SAMM aspect models.
#
# Tokenizes the file and parses it by the Turtle grammar: a subject's
# statements are separated by ';', objects of the same predicate by ',',
# and '.' ends the subject. Every subject becomes an ``Element`` - named
# ones (``:Batch a samm:Aspect ; ...``) as well as anonymous ones defined
# inline (``[ a samm-c:RegularExpressionConstraint ; ... ]``).
#
# Usage, as the criteria under ``criteria/`` see it:
#
#     for el in model.elements:               # every element, file order
#         if el.is_a("Property"):             # type, with or without prefix
#             el.get("characteristic")        # first value, or None
#             el.get_all("see")               # all values
#             el.text("preferredName")        # English literal text, or None
#
# Values returned by get()/get_all():
#
#   reference   -> str: local names without the leading ':' ("batchId"),
#                  everything else as written ("xsd:string", "<urn:...>")
#   literal     -> Literal (text, lang, datatype)
#   ( ... )     -> list of values
#   [ ... ]     -> Element (anonymous, name None)
#
# Anonymous nodes without a type (e.g. the ``[ samm:property :x ;
# samm:optional true ]`` wrappers inside samm:properties) are values only,
# not model elements, so they don't show up in ``model.elements``.

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

TOKEN_RE = re.compile(r"""
      (?P<ws>\s+)
    | (?P<comment>\#[^\n]*)
    | (?P<iri><[^>]*>)
    | (?P<string>\"\"\"(?:[^"\\]|\\.|"(?!""))*\"\"\"
                |'''(?:[^'\\]|\\.|'(?!''))*'''
                |"(?:[^"\\\n]|\\.)*"
                |'(?:[^'\\\n]|\\.)*')
    | (?P<at>@[A-Za-z][\w-]*)
    | (?P<datatype>\^\^)
    | (?P<number>[+-]?(?:\d+\.\d+|\.\d+|\d+)(?:[eE][+-]?\d+)?)
    | (?P<pname>(?:[A-Za-z][\w-]*(?:\.[\w-]+)*)?:(?:[\w-]+(?:\.[\w-]+)*)?)
    | (?P<word>[A-Za-z][\w-]*)
    | (?P<punct>[.;,\[\]()])
""", re.VERBOSE)

OWN_NAMESPACE_RE = re.compile(r"urn:[bs]amm:([\w.]+):(\d+\.\d+\.\d+)#")

ESCAPES = {"t": "\t", "n": "\n", "r": "\r", "b": "\b", "f": "\f", '"': '"', "'": "'", "\\": "\\"}


@dataclass(frozen=True)
class Literal:
    text: str
    lang: str | None = None
    datatype: str | None = None


def _matches(name: str, key: str) -> bool:
    # "samm:see" matches only itself; "see" matches any prefix's "see".
    return name == key if ":" in key else name.rsplit(":", 1)[-1] == key


@dataclass
class Element:
    name: str | None  # None for anonymous [ ... ] elements
    line_no: int
    types: list[str] = field(default_factory=list)
    statements: list[tuple[str, object]] = field(default_factory=list)  # (predicate, value), file order

    @property
    def type(self) -> str | None:
        return self.types[0] if self.types else None

    @property
    def label(self) -> str:
        # For messages: the name, or "[ a <type> ]" for an anonymous element.
        return self.name or f"[ a {self.type} ]"

    def is_a(self, type_: str) -> bool:
        return any(_matches(t, type_) for t in self.types)

    def get_all(self, predicate: str) -> list:
        return [value for pred, value in self.statements if _matches(pred, predicate)]

    def get(self, predicate: str):
        values = self.get_all(predicate)
        return values[0] if values else None

    def text(self, predicate: str, lang: str = "en") -> str | None:
        for value in self.get_all(predicate):
            if isinstance(value, Literal) and value.lang == lang:
                return value.text
        return None


@dataclass
class TTLModel:
    file: str
    text: str
    prefixes: dict[str, str]
    namespace: str | None
    version: str | None
    elements: list[Element]

    def element(self, name: str) -> Element | None:
        for el in self.elements:
            if el.name == name:
                return el
        return None

    def resolve(self, value) -> Element | None:
        # A value pointing at an element: inline [ ... ] or a local name.
        if isinstance(value, Element):
            return value
        return self.element(value) if isinstance(value, str) else None

    @property
    def aspect(self) -> Element | None:
        return next((el for el in self.elements if el.is_a("Aspect")), None)


class TurtleSyntaxError(ValueError):
    pass


@dataclass
class _Token:
    kind: str
    value: str
    line: int


def _tokenize(text: str) -> list[_Token]:
    tokens = []
    pos, line = 0, 1
    while pos < len(text):
        m = TOKEN_RE.match(text, pos)
        if not m:
            raise TurtleSyntaxError(f"line {line}: unexpected character {text[pos]!r}")
        if m.lastgroup not in ("ws", "comment"):
            tokens.append(_Token(m.lastgroup, m.group(), line))
        line += m.group().count("\n")
        pos = m.end()
    return tokens


def _unquote(raw: str) -> str:
    body = raw[3:-3] if raw[:3] in ('"""', "'''") else raw[1:-1]
    return re.sub(r"\\(u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8}|.)",
                  lambda m: chr(int(m.group(1)[1:], 16)) if m.group(1)[0] in "uU" else ESCAPES.get(m.group(1), m.group(1)),
                  body)


class _Parser:
    def __init__(self, tokens: list[_Token]):
        self.tokens = tokens
        self.pos = 0
        self.prefixes: dict[str, str] = {}
        self.elements: list[Element] = []
        self.named: dict[str, Element] = {}

    def parse(self) -> None:
        while self._peek() is not None:
            tok = self._peek()
            if tok.kind == "at" and tok.value == "@prefix":
                self._prefix(terminated=True)
            elif tok.kind == "at" and tok.value == "@base":
                self._next()
                self._expect_kind("iri")
                self._expect(".")
            elif tok.kind == "word" and tok.value.upper() == "PREFIX":
                self._prefix(terminated=False)
            elif tok.kind == "word" and tok.value.upper() == "BASE":
                self._next()
                self._expect_kind("iri")
            else:
                self._triples()
                self._expect(".")

    def _prefix(self, terminated: bool) -> None:
        self._next()
        name = self._expect_kind("pname").value
        if not name.endswith(":"):
            self._error(f"expected a prefix name ending in ':', got {name!r}")
        self.prefixes[name[:-1]] = self._expect_kind("iri").value[1:-1]
        if terminated:
            self._expect(".")

    def _triples(self) -> None:
        if self._at("["):
            subject = self._blank_node()
            if not self._at("."):
                self._predicate_object_list(subject)
            return
        tok = self._next()
        if tok.kind not in ("pname", "iri"):
            self._error(f"expected a subject, got {tok.value!r}", tok)
        name = self._ref(tok)
        subject = self.named.get(name)
        if subject is None:
            subject = Element(name, tok.line)
            self.named[name] = subject
            self.elements.append(subject)
        self._predicate_object_list(subject)

    def _predicate_object_list(self, subject: Element) -> None:
        while True:
            tok = self._next()
            if tok.kind == "word" and tok.value == "a":
                predicate = "a"
            elif tok.kind in ("pname", "iri"):
                predicate = self._ref(tok)
            else:
                self._error(f"expected a predicate, got {tok.value!r}", tok)
            while True:
                value = self._object()
                if predicate == "a":
                    subject.types.append(value)
                else:
                    subject.statements.append((predicate, value))
                if not self._at(","):
                    break
                self._next()
            if not self._at(";"):
                return
            while self._at(";"):
                self._next()
            if self._at(".") or self._at("]"):
                return

    def _object(self):
        tok = self._peek()
        if tok is None:
            self._error("unexpected end of file")
        if self._at("["):
            return self._blank_node()
        if self._at("("):
            self._next()
            items = []
            while not self._at(")"):
                items.append(self._object())
            self._next()
            return items
        tok = self._next()
        if tok.kind in ("pname", "iri"):
            return self._ref(tok)
        if tok.kind == "string":
            text = _unquote(tok.value)
            if self._peek() is not None and self._peek().kind == "at":
                return Literal(text, lang=self._next().value[1:])
            if self._peek() is not None and self._peek().kind == "datatype":
                self._next()
                return Literal(text, datatype=self._ref(self._next()))
            return Literal(text, datatype="xsd:string")
        if tok.kind == "number":
            kind = "xsd:double" if "e" in tok.value.lower() else "xsd:decimal" if "." in tok.value else "xsd:integer"
            return Literal(tok.value, datatype=kind)
        if tok.kind == "word" and tok.value in ("true", "false"):
            return Literal(tok.value, datatype="xsd:boolean")
        self._error(f"expected an object, got {tok.value!r}", tok)

    def _blank_node(self) -> Element:
        start = self._next()
        node = Element(None, start.line)
        index = len(self.elements)  # its type is only known at ']' - keep file order anyway
        if not self._at("]"):
            self._predicate_object_list(node)
        self._expect("]")
        if node.types:
            self.elements.insert(index, node)
        return node

    def _ref(self, tok: _Token) -> str:
        return tok.value[1:] if tok.kind == "pname" and tok.value.startswith(":") else tok.value

    def _peek(self) -> _Token | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _next(self) -> _Token:
        tok = self._peek()
        if tok is None:
            self._error("unexpected end of file")
        self.pos += 1
        return tok

    def _at(self, punct: str) -> bool:
        tok = self._peek()
        return tok is not None and tok.kind == "punct" and tok.value == punct

    def _expect(self, punct: str) -> None:
        tok = self._next()
        if tok.kind != "punct" or tok.value != punct:
            self._error(f"expected {punct!r}, got {tok.value!r}", tok)

    def _expect_kind(self, kind: str) -> _Token:
        tok = self._next()
        if tok.kind != kind:
            self._error(f"expected {kind}, got {tok.value!r}", tok)
        return tok

    def _error(self, message: str, tok: _Token | None = None):
        tok = tok or self._peek() or (self.tokens[-1] if self.tokens else None)
        raise TurtleSyntaxError(f"line {tok.line if tok else 1}: {message}")


def parse_model(file_path: str) -> TTLModel:
    text = Path(file_path).read_text(encoding="utf-8")
    parser = _Parser(_tokenize(text))
    parser.parse()

    own = OWN_NAMESPACE_RE.fullmatch(parser.prefixes.get("", ""))
    namespace, version = (own.group(1), own.group(2)) if own else (None, None)

    return TTLModel(
        file=file_path,
        text=text,
        prefixes=parser.prefixes,
        namespace=namespace,
        version=version,
        elements=parser.elements,
    )
