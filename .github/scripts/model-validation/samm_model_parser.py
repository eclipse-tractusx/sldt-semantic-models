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
# Lightweight, dependency-free Turtle/SAMM parser.
#
# This is intentionally *not* a full RDF/Turtle parser: SAMM aspect models
# in this repository are written in a very consistent style (one top-level
# model element per unindented ``:Name a samm:Type ;`` block), which is
# reliable enough to extract the fields the MS2 criteria care about without
# pulling in an external RDF library.
#
# The ``TTLModel`` produced here is the "data package" the master script
# (``ms2_check.py``) hands to every criterion sub-routine under
# ``criteria/``.

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# A local reference such as ``:someName`` -- but not the tail end of a
# prefixed name like ``samm:someName`` (negative look-behind on the char
# before ':').
LOCAL_REF_RE = re.compile(r"(?<![\w-]):([A-Za-z_][\w]*)")

PREFIX_RE = re.compile(r"@prefix\s+([\w-]*):\s*<([^>]+)>")
OWN_NAMESPACE_RE = re.compile(r"@prefix\s+:\s*<urn:[bs]amm:([\w.]+):(\d+\.\d+\.\d+)#>")

# Top level model element, e.g. ":FooBar a samm:Aspect ;" up to the next
# such declaration (or end of file).
ELEMENT_RE = re.compile(
    r"^:(?P<name>[A-Za-z_][\w]*)\s+a\s+(?P<type>[\w:-]+)\s*;(?P<body>.*?)"
    r"(?=^:[A-Za-z_][\w]*\s+a\s+[\w:-]+\s*;|\Z)",
    re.MULTILINE | re.DOTALL,
)

# Turtle allows both a plain quoted string literal and a triple-quoted
# "long" string literal (the latter used for multi-line preferredName /
# description values); a language-tagged samm:field can be either.
LANG_STRING_RE_TMPL = (
    r'samm:{field}\s+(?:"""(?P<triple>(?:[^"]|"(?!""))*?)"""|"(?P<single>(?:[^"\\]|\\.)*)")@(?P<lang>\w+)'
)


@dataclass
class Element:
    name: str
    type: str  # e.g. "samm:Aspect", "samm-c:Enumeration", "samm-e:...
    body: str
    line_no: int
    preferred_names: list[tuple[str, str]] = field(default_factory=list)  # (lang, text)
    descriptions: list[tuple[str, str]] = field(default_factory=list)  # (lang, text)
    characteristic: str | None = None
    data_type: str | None = None
    has_example_value: bool = False
    unit: str | None = None
    see: list[str] = field(default_factory=list)
    payload_name: str | None = None
    properties: list[str] = field(default_factory=list)

    @property
    def short_type(self) -> str:
        return self.type.split(":", 1)[-1]

    def preferred_name(self, lang: str = "en") -> str | None:
        for l, text in self.preferred_names:
            if l == lang:
                return text
        return None

    def description(self, lang: str = "en") -> str | None:
        for l, text in self.descriptions:
            if l == lang:
                return text
        return None


@dataclass
class TTLModel:
    file: str
    text: str
    prefixes: dict[str, str]
    namespace: str | None
    version: str | None
    elements: dict[str, Element]

    @property
    def aspect(self) -> Element | None:
        for el in self.elements.values():
            if el.short_type == "Aspect":
                return el
        return None


def _extract_lang_strings(body: str, field_name: str) -> list[tuple[str, str]]:
    pattern = re.compile(LANG_STRING_RE_TMPL.format(field=field_name))
    result = []
    for m in pattern.finditer(body):
        text = m.group("triple") if m.group("triple") is not None else m.group("single")
        result.append((m.group("lang"), text))
    return result


def _extract_single(body: str, pattern: str) -> str | None:
    m = re.search(pattern, body)
    return m.group(1) if m else None


def parse_element(name: str, type_: str, body: str, line_no: int) -> Element:
    see_match = re.search(r"samm:see\s+([^;.]+)", body)
    see_refs = re.findall(r"<([^>]+)>", see_match.group(1)) if see_match else []

    properties: list[str] = []
    props_match = re.search(r"samm:properties\s*\(([\s\S]*?)\)\s*;", body)
    if props_match:
        properties = LOCAL_REF_RE.findall(props_match.group(1))

    return Element(
        name=name,
        type=type_,
        body=body,
        line_no=line_no,
        preferred_names=_extract_lang_strings(body, "preferredName"),
        descriptions=_extract_lang_strings(body, "description"),
        characteristic=_extract_single(body, r"samm:characteristic\s+:(\w+)"),
        data_type=_extract_single(body, r"samm:dataType\s+([\w:.\-]+)"),
        has_example_value="samm:exampleValue" in body,
        unit=_extract_single(body, r"samm:unit\s+([\w:.\-]+)"),
        see=see_refs,
        payload_name=_extract_single(body, r'samm:payloadName\s+"([^"]+)"'),
        properties=properties,
    )


def parse_model(file_path: str) -> TTLModel:
    text = Path(file_path).read_text(encoding="utf-8")

    prefixes = {p: uri for p, uri in PREFIX_RE.findall(text)}

    ns_match = OWN_NAMESPACE_RE.search(text)
    namespace, version = (ns_match.group(1), ns_match.group(2)) if ns_match else (None, None)

    elements: dict[str, Element] = {}
    for m in ELEMENT_RE.finditer(text):
        line_no = text.count("\n", 0, m.start()) + 1
        el = parse_element(m.group("name"), m.group("type"), m.group("body"), line_no)
        elements[el.name] = el

    return TTLModel(
        file=file_path,
        text=text,
        prefixes=prefixes,
        namespace=namespace,
        version=version,
        elements=elements,
    )
