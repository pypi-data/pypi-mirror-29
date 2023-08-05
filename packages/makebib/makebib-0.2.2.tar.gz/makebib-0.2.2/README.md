# Makebib

A simple script to generate a local bib file from a central
database so that only items actually cited appear.

## Installation

```bash
$ pip install makebib
```

## Usage

```bash
$ makebib cmd arg
```

where `cmd` is either `compile` or `show`.

Compile takes as an argument the basename of a TeX-file
(i.e. without the `.tex` extension) and creates a local bib file
populating it with items which are cited by the document and can
be found in the central database. Then it runs (a python version)
of BibTeX on the TeX file.

The filename of the local bib file is extracted from the TeX file
by looking for a `\bibliography` command. The program will refuse
to overrite a previously existing bib file unless given the
`--force-overwrite` option or unless it finds a file named `.generated_bib`
in the current directory. Additionally, whenever it creates
(or overwrites) a local bib file, it also creates the file named `.generated_bib`
to indicate, that the file was automatically generated.

The `show` command is used for showing various info. It has several
subcommands:
 
- `cited`    Lists all the keys which are cited in the TeX-file given by its argument.

- `missing`  Lists keys which are cited in the TeX-file given by its argument
             but not present in the central database

- `all`      Lists all the keys from the central database

- 'bibentry' Prints out the bibentry from the central database identified by
             the key given as the argument of this subcommand.

- `cfg`      Lists the values (or their defaults) of all configuration
             settings (and/or their defaults).

Additional help is available by running

```bash
$ makebib [cmd] --help
```

## Configuration

The program reads its configuration from the files `/etc/makebib`,
`~/.makebib` or `.makebib` in the current directory. If either of
the files does not exist, it is skipped. Also, options specified
in later files override options specified in the previous files
(and defaults). The files follow a simple

```
    key = val
```

format with each line specifying a single case-insensitive option.
Spaces around `=` are ignored as is everything following a `#` sign.
Currently the only available option is `db` which specifies the
location of the central BibTeX database.
