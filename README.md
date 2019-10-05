# sqlprotobuf
A very early stage SQL to Protobuf parser written in Python. Inspired by https://github.com/okdistribute/sql-protobuf.

This does not cover many SQL/Protobuf idiosyncrasies, and is only meant to crudely turn CREATE TABLE statements into Protobuf Messages. 

To use:

1. Build and install:
`python setup.py build`
`python setup.py install`

2. Run from a terminal:
`sqlprotobuf --in-file=<your-schema.sql> --out-file=<your-schema.proto>`
