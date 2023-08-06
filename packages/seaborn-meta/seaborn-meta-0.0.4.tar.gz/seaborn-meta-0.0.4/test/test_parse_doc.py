from seaborn.meta.parse_doc import *
import unittest, sys
if sys.version_info[0]==3:
    basestring = str

class test_parse_doc(unittest.TestCase):

    def test_dict(self, a='A', b=5, c=None):
        """ This will show the answer for each parse func::
            a:A
            b:B
        :param a: str for placeholder
        :param b: int for placeholder
        :param c: list of str for placeholder
        :return: None
        """
        self.assertEqual(parse_doc_dict(), {'a': 'A', 'b': 'B'},
                         'parse_doc_dict has failed with %s' % parse_doc_dict())

    def test_list(self, a='A', b=5, c=None):
        """ This will show the answer for each parse func::
            a:A
            b:B
        :param a: str for placeholder
        :param b: int for placeholder
        :param c: list of str for placeholder
        :return: None
        """
        self.assertEqual(parse_doc_list(), ['a:A', 'b:B'],
                         'parse_doc_dict has failed with %s' % parse_doc_list())

    def test_str(self, a='A', b=5, c=None):
        """ This will show the answer for each parse func::
            a:A
            b:B
        :param a: str for placeholder
        :param b: int for placeholder
        :param c: list of str for placeholder
        :return: None
        """
        self.assertEqual(parse_doc_str(), 'a:A\nb:B',
                         'parse_doc_dict has failed with %s' % parse_doc_str())

    def test_types(self, a='A', b=5, c=None):
        """ This will show the answer for each parse func::
            a:A
            b:B
        :param a: str for placeholder
        :param b: int for placeholder
        :param c: list of str for placeholder
        :return: None
        """
        result = parse_arg_types()
        expected = {'a': basestring, 'b': int,
                   'c': (list, basestring)}

        self.assertDictEqual(
            result,expected,
            'parse_arg_types has failed with %s' % result)

if __name__ == "__main__":
    unittest.main()