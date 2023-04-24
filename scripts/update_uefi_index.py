#!/usr/bin/env python3

from html.parser import HTMLParser
import re
import os
import csv
from typing import Optional, TypedDict
import enum
import logging
import requests

UEFI_INDEX_URL = 'https://uefi.org/specs/UEFI/2.10/index.html'
uefi_csv = os.path.dirname(__file__) + '/../source/extensions/uefi_index.csv'
logger = logging.getLogger(__name__)

AttrsType = list[tuple[str, Optional[str]]]


class ParsedEntry(TypedDict, total=False):
    num: str
    title: str
    href: Optional[str]


# State machine:
#
#         AWAIT_DIV
#             v
#         AWAIT_LI <----+
#             v         |
#          AWAIT_A -----+
#             v         |
# +-- AWAIT_FIRST_DATA -+
# |           v         |
# |   AWAIT_MORE_DATA --+
# |           v
# +-------> DONE
class State(enum.Enum):
    AWAIT_DIV = enum.auto()
    AWAIT_LI = enum.auto()
    AWAIT_A = enum.auto()
    AWAIT_FIRST_DATA = enum.auto()
    AWAIT_MORE_DATA = enum.auto()
    DONE = enum.auto()


class IndexHtmlParser(HTMLParser):
    """A class to parse an HTML index and extract what we need from there.
    """
    def reset(self) -> None:
        self.index: list[ParsedEntry] = []  # The index we have captured.
        self.state = State.AWAIT_DIV        # Our state-machine current state.
        self.current: ParsedEntry = {}      # The current data.
        self.nums: set[str] = set()         # To detect duplicates.
        HTMLParser.reset(self)

    def set_state(self, s: State) -> None:
        if self.state != s:
            logger.debug(f"-> {s}")
            self.state = s

    def has_class(self, pat: str, attrs: AttrsType) -> bool:
        for a in attrs:
            if a[0] == 'class' and a[1] is not None and pat in a[1]:
                return True

        return False

    def handle_starttag(self, tag: str, attrs: AttrsType) -> None:
        logger.debug(f"Encountered a start tag: {tag}, {attrs}")

        if self.state == State.AWAIT_DIV and tag == 'div':
            # We look for a div with toctree* class.
            if self.has_class('toctree', attrs):
                self.set_state(State.AWAIT_LI)
                return

        elif self.state == State.AWAIT_LI and tag == 'li':
            # We look for an li with toctree* class.
            if self.has_class('toctree', attrs):
                self.set_state(State.AWAIT_A)
                return

        elif self.state == State.AWAIT_A:
            # We expect an a with a reference internal class and a href.
            if tag == 'a' and self.has_class('reference internal', attrs):
                for a in attrs:
                    if a[0] == 'href':
                        self.current['href'] = a[1]
                        self.set_state(State.AWAIT_FIRST_DATA)
                        return

            self.set_state(State.AWAIT_LI)

        elif self.state == State.AWAIT_FIRST_DATA:
            self.set_state(State.AWAIT_LI)

        elif self.state == State.AWAIT_MORE_DATA:
            # Ignore most of the tags when inside the data.
            if tag != 'a':
                return

            self.set_state(State.AWAIT_LI)

    def handle_endtag(self, tag: str) -> None:
        logger.debug(f"Encountered an end tag : {tag}")

        if self.state in (State.AWAIT_A, State.AWAIT_FIRST_DATA):
            self.set_state(State.AWAIT_LI)

        elif self.state == State.AWAIT_MORE_DATA:
            if tag != 'a':
                # Ignore most of the tags when inside the data.
                return

            # else: tag == 'a'
            # When we have all the data, store the index entry.

            # We need to filter the section titles a bit because they sometimes
            # contain a few remaining unicode characters.
            self.current['title'] = re.sub(
                r'[\x80-\xff]+', '-', self.current['title'])

            logger.debug(f"Index entry: {self.current}")
            self.index.append(self.current)
            self.current = {}
            self.set_state(State.AWAIT_LI)

    def handle_data(self, data: str) -> None:
        logger.debug(f"Encountered some data  : {data}")

        if self.state == State.AWAIT_A:
            self.set_state(State.AWAIT_LI)

        elif self.state == State.AWAIT_FIRST_DATA:
            # Inside the li, and the a, we look for a first data in the right
            # format.
            m = re.match(r'([A-Z0-9\.]*[0-9])\. (.*)', data)
            if m:
                num = m[1]

                # Bail out at first duplicate.
                if num in self.nums:
                    self.set_state(State.DONE)
                    return

                self.nums.add(num)
                self.current['num'] = num
                self.current['title'] = m[2]
                self.set_state(State.AWAIT_MORE_DATA)
                return

        elif self.state == State.AWAIT_MORE_DATA:
            # We might have more data.
            self.current['title'] += data
            return


def update_index(index_url: str, csv_filename: str) -> None:
    """Update index database.
    We download the index and create a csv containing lines in the following
    format:
    <chapter number>,<chapter title>,<url>
    """
    # Download index
    logger.info(f"Downloading {index_url}")
    req = requests.get(index_url, allow_redirects=True, timeout=60.0)
    # logger.debug(req)

    # Parse HTML
    logger.debug('Parsing')
    parser = IndexHtmlParser()
    parser.feed(req.text)
    # logger.debug(parser.index)

    # Save csv
    logger.info(f"Saving {csv_filename}")
    url_prefix = os.path.dirname(index_url)

    with open(csv_filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')

        for e in parser.index:
            writer.writerow(
                [e['num'], e['title'], f"{url_prefix}/{e['href']}"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    update_index(UEFI_INDEX_URL, uefi_csv)
