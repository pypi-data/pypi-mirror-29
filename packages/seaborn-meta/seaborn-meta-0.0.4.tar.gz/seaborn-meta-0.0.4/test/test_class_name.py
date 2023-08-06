from seaborn.meta.class_name import *
import unittest
import os

class test_class_name(unittest.TestCase):
    def test_class_name_to_instant_name(self):
        self.assertEqual("parent_name.child_name",class_name_to_instant_name("ParentName_ChildName"))

    def test_instant_name_to_class_name(self):
        self.assertEqual("ParentName_ChildName",instant_name_to_class_name("parent_name.child_name"))

    def test_create_init_files(self):
        success=True
        create_init_files(os.getcwd())
        try:
            os.remove(os.getcwd()+'/__init__.py')
        except BaseException as e:
            print(e)
            success=False
        self.assertTrue(success,"__init__.py not found")

if __name__ == '__main__':
    unittest.main()
