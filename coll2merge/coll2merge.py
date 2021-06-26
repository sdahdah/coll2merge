"""Merge Decked Builder *.coll2 files.

The ``*.coll2`` file format is just a YAML file. When parsed, it has a
structure like:

    parsed_file = {
        'doc': [
            {
                'version': 1
            },
            {
                'items': [
                    [
                        {'id': card_id},
                        {'r': regular_quantity}
                    ],
                    [
                        {'id': card_id},
                        {'r': regular_quantity},
                        {'f':, foil_quantity},
                    ],
                ],
            },
        ],
    }

This script parses multiple ``*.coll2`` files into a data structure that's
easier to work with, then exports them as a single file.
"""

import argparse
import typing

import yaml


def main():
    """Merge Decked Builder *.coll2 files."""
    # Parse arguments.
    parser = argparse.ArgumentParser(
        description='Merge Decked Builder *.coll2 files.')
    parser.add_argument(
        'files',
        nargs='+',
        type=argparse.FileType('r'),
        metavar='FILES',
        help='*.coll2 files to merge',
    )
    args = parser.parse_args()
    # Add all ``*.coll2`` files to ``Collection`` object.
    collection = Collection()
    for f in args.files:
        collection.add_file(f)
    # Print new merged collection.
    print(collection.get_coll2())


class Collection:
    """Store card IDs and quantities."""

    def __init__(self) -> None:
        """Instantiate ``Collection``."""
        # Version of ``*.coll2`` file
        self._version = None
        # Internal dict-of-dicts to store IDs and quantites. Outermost key is
        # the card ID. The value is a dict whose keys are ``regular`` and
        # ``foil``. The quantities of each type of card are stored there. For
        # example:
        #
        # self._coll = {
        #     12345 : {
        #         'regular': 2,
        #         'foil': 1,
        #     },
        #     54321 : {
        #         'regular': 4,
        #         'foil': 0,
        #     },
        # }
        self._coll: dict[int, dict[str, int]] = {}

    def add_file(self, file: typing.TextIO) -> None:
        """Add a ``*.coll2`` file to the collection.

        Parameters
        ----------
        file : typing.TextIO
            ``*.coll2`` file.
        """
        # Open file
        parsed_file = yaml.safe_load(file)
        # Check version
        version = parsed_file['doc'][0]['version']
        if self._version is None:
            self._version = version
        elif self._version != version:
            raise ValueError('The versions of the chosen files do not match.')
        # Read items and add to internal dict
        items = parsed_file['doc'][1]['items']
        for i in items:
            item_id, regular, foil = self._parse_item(i)
            self._add_item(item_id, regular, foil)

    def get_coll2(self) -> str:
        """Get the ``*.coll2`` representation of the object.

        Returns
        -------
        str
            ``*.coll2`` representation of the object.
        """
        # Create empty ``*.coll2`` template
        coll2: dict[str, list[dict[str, typing.Any]]] = {
            'doc': [{
                'version': self._version
            }, {
                'items': []
            }]
        }
        # Go through the internal dict and add items to the ``*.coll2`` dict.
        for key, value in self._coll.items():
            regular = value['regular']
            foil = value['foil']
            item = self._make_item(key, regular, foil)
            coll2['doc'][1]['items'].append(item)
        # Return the ``*.coll2`` file as a string.
        return yaml.dump(coll2)

    def _add_item(self, item_id: int, regular: int, foil: int) -> None:
        """Add a card to the internal dict.

        Parameters
        ----------
        item_id : int
            Card ID.
        regular : int
            Regular (nonfoil) quantity.
        foil : int
            Foil quantity.
        """
        if item_id in self._coll.keys():
            # If it's already in the dict, sum the quantities.
            self._coll[item_id]['regular'] += regular
            self._coll[item_id]['foil'] += foil
        else:
            # If it's not in the dict, put it there.
            self._coll[item_id] = {'regular': regular, 'foil': foil}

    @staticmethod
    def _parse_item(item: list[dict[str, int]]) -> tuple[int, int, int]:
        """Parse a ``*.coll2`` item.

        Parameters
        ----------
        item : list[dict[str, int]]
            ``*.coll2`` item to parse.

        Returns
        -------
        tuple[int, int, int]
            Tuple containing ID, regular quantity, and foil quantity.
        """
        # Grab the ID right away.
        item_id = item[0]['id']
        # Assume there are 0 regular and foil card to start.
        regular = 0
        foil = 0
        for i in item[1:]:
            # Check the rest of the items for regular and foil card quantities.
            if 'r' in i.keys():
                regular = i['r']
            elif 'f' in i.keys():
                foil = i['f']
        return (item_id, regular, foil)

    @staticmethod
    def _make_item(item_id: int, regular: int,
                   foil: int) -> list[dict[str, int]]:
        """Format a ``*.coll2`` item.

        Parameters
        ----------
        item_id : int
            Card ID.
        regular : int
            Regular (nonfoil) quantity.
        foil : int
            Foil quantity.

        Returns
        -------
        list[dict[str, int]]
            ``*.coll2`` item.
        """
        # Create template for item with ID
        item = [{'id': item_id}]
        # Add regular and foil dicts if the card quantities are not zero.
        if regular != 0:
            item.append({'r': regular})
        if foil != 0:
            item.append({'f': foil})
        return item


if __name__ == '__main__':
    main()
