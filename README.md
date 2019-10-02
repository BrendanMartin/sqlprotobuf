# sqlprotobuf
A very early stage SQL to Protobuf parser written in Python. 

This does not cover many SQL/Protobuf idiosyncrasies, and is only meant to crudely turn CREATE TABLE statements into Protobuf Messages. 

To use:

1. Install requirements with
`pip install -r requirements.txt`

2. Run from a terminal:
`python sqlprotobuf --in-file=<your-schema.sql> --out-file=<your-schema.proto>`
