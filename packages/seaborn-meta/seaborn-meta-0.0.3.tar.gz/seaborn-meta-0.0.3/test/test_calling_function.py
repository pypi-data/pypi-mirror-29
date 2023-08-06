#Ensure test_file_code
from seaborn.meta.calling_function import *
from collections import OrderedDict
import unittest

class test_calling_function(unittest.TestCase):

    def test_function_linenumber(self):
        self.assertEqual(function_linenumber(),'9    ')

    def test_function_info(self):
        actual = function_info()
        expected = {'line_number': 12,
                    'class_name':'test_calling_function',
                    'basename':'test_calling_function',
                    }
        check = actual
        check.update(expected)
        self.assertDictEqual(actual,check)

    def test_function_arguments(self):
        self.assertEqual(function_arguments(function_arguments),['func'])

    def test_function_defaults(self):
        self.assertListEqual(list(function_defaults(function_doc)),[1, None])

    def test_function_doc(self):
        """
        Tests function_doc's return
        :return:
        """
        self.assertEqual(function_doc(),"\n        Tests function_doc's return"
                                        "\n        :return:\n        ")

    def test_function_path(self):
        self.assertIn('/meta/calling_function.py',
                      function_path(function_path))

    def test_file_code(self):
        self.assertIn('#Ensure test_file_code\n'
                      'from seaborn.meta.calling_function import *\n'
                      'from collections import OrderedDict\n',file_code())

    def test_relevant_kwargs(self):
        def test(a=1,b=2,c=False,**kwargs):
            if c:
                print(a,b)
            return relevant_kwargs(simple)
        def simple(a=1,b=2,c=False,**kwargs):
            return kwargs
        self.assertDictEqual(test(),{'a':1,'b':2,'c':False})

    def test_function_args(self):
        self.assertTupleEqual(function_args(function_args),('function',))

    def test_function_kwargs(self):
        def test(a):
            return function_kwargs()
        self.assertDictEqual(test(a=1),{'a':1})

    @unittest.skip("NotImplemented")
    def test_function_code(self):
        raise NotImplemented

    def test_function_history(self):
        self.assertListEqual(['function_history', 'test_function_history',
                              'run', '__call__', 'run']
                             ,function_history()[:5])

    def test_func_frame(self):
        actual = func_frame(1,'test_func_frame')
        relevant = []
        reject = ['trace','code','globals','back','locals','builtins']
        for attr in dir(actual):
            if attr[:2] == 'f_' and not attr[2:] in reject:
                relevant += [attr]
        comp = {}
        for k in relevant:
            exec('comp.update({"'+k+'":str(actual.'+k+')})')
        expected = {'f_lasti': '124', 'f_lineno': '79'}
        self.assertSetEqual(set(expected.keys()).union(comp.keys()),
                            set(comp.keys()))

    def test_function_name(self):
        self.assertTupleEqual(function_name(),
                              ('test_calling_function','test_function_name'))

    def test_path(self):
        self.assertEqual(path(),
                         'test_calling_function__test'
                         '_calling_function__test_path')

    def test_current_folder(self):
        self.assertIn('/test',current_folder())

    def test_trace_error(self):
        err = trace_error()
        try:
            self.assertEqual(None,err[1])
        except:
            self.assertEqual('in test_trace_error\n    err = trace_error()',
                             err[1])

if __name__ == '__main__':
    unittest.main()