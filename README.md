# coll2merge

Merge `*.coll2` files for [Decked Builder](https://deckedbuilder.com/).

Decked Builder provides an easy way to create `*.coll2` files from CSVs
[here](http://csv.deckedbuilder.com/). But you have to merge `*.coll2` files
[manually](https://deckedstudios.supportbee.io/1893-faq/3896-decked-builder/11144-q-is-there-any-way-to-merge-collections-together).
This package helps you merge `*.coll2` files automatically.

Not affiliated with Decked Builder. Back up your files before you use this.

## Installation

Clone the repo and install using `pip`:

```sh
$ git clone git@github.com:sdahdah/coll2merge.git
$ pip install ./coll2merge
```

The package places the executable `coll2merge` in your path.

## Usage

Run `coll2merge` on as many files as you need and output the result to a file:

```sh
$ coll2merge scanned_cards.coll2 precons.coll2 > full_collection.coll2
```

## Testing

Install the development dependencies:

```sh
$ pip install requirements.txt
```

Then run `pytest` in the `tests/` directory.
