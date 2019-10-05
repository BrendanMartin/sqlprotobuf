import setuptools
from pathlib import Path

setuptools.setup(
        name='sqlprotobuf',
        version='0.1',
        author="Brendan Martin",
        description="Convert SQL CREATE TABLE statements to Protobuf Messages",
        long_description=open(Path(__file__).parent/"README.md", "r").read(),
        packages=['sqlprotobuf'],
        entry_points={
            'console_scripts': [
                'sqlprotobuf=sqlprotobuf.app:cli'
            ]
        }
)
