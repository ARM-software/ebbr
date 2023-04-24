#!/usr/bin/env python3
# Note: run sphinx with -vv when debugging.

import os
import csv
from typing import Any, Callable, TypedDict
from docutils import nodes
from sphinx.util import logging

uefi_csv = os.path.dirname(__file__) + '/uefi_index.csv'
logger = logging.getLogger(__name__)


class IndexEntry(TypedDict):
    title: str
    url: str


IndexType = dict[str, IndexEntry]

RoleType = Callable[
                [str, str, str, int, Any, dict[Any, Any], list[str]],
                tuple[list[Any], list[str]]]


def load_index(csv_filename: str) -> IndexType:
    """Load index csv.
    We expect lines in the following format:
    <chapter number>,<chapter title>,<url>
    """
    logger.debug(f"Loading {csv_filename}")
    r = {}

    try:
        with open(csv_filename, encoding='utf-8') as f:
            reader = csv.reader(f)

            for row in reader:
                r[row[0]] = IndexEntry(title=row[1], url=row[2])

    except OSError as e:
        logger.warning(f"Cannot load {csv_filename}: {e}")

    return r


def create_role(ref: str, index: IndexType) -> RoleType:
    """We wrap the role function just to pass it the index (globals do not
    work).
    ref: UEFI
    """
    def role(
            name: str, rawtext: str, text: str, lineno: int, inliner: Any,
            options: dict[Any, Any] = {}, content: list[str] = []
            ) -> tuple[list[Any], list[str]]:

        logger.debug(
            f"{ref} {name} {rawtext} {text} {lineno} {inliner} {options} "
            f"{content}")

        # Query the index.
        if text in index:
            title = index[text]['title']
            reftext = f"{ref} § {text} {title}"
            url = index[text]['url']
            logger.debug(f"{reftext} {url}")

        else:
            logger.warning(f"No index entry for {ref} section {text}")
            url = ''
            reftext = f"{ref} § {text}"

        node = nodes.reference(rawtext, reftext, refuri=url, **options)
        return [node], []

    return role


def setup(app: Any) -> None:
    """Setup our extension.
    We load the UEFI index csv and add the UEFI role.
    """
    uefi_index = load_index(uefi_csv)
    # logger.debug(uefi_index)
    app.add_role('UEFI', create_role('UEFI', uefi_index))
