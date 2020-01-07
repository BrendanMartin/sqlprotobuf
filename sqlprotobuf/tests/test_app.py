import unittest
from sqlprotobuf.app import main

class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_contraint(self):
        s = """
        -- object: public.list | type: TABLE --
        -- DROP TABLE IF EXISTS public.list CASCADE;
        CREATE TABLE public.list (
            id integer NOT NULL,
            title text NOT NULL,
            user_id integer,
            created_on integer,
            last_studied integer,
            last_updated integer,
            client_updated integer,
            deleted boolean,
            CONSTRAINT list_pk PRIMARY KEY (id),
            CONSTRAINT title_userid_constraint UNIQUE (title,user_id)
        );
        """
        main(in_string=s)

    def test_regex(self):
        s = """CREATE TABLE public.list (
                    id integer NOT NULL,
                    title char(20)
                );
                """
        main(in_string=s)

if __name__ == '__main__':
    unittest.main()
