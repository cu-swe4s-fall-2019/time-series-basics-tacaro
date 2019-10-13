import unittest
import os
import random
import decimal
import statistics
import numpy as np
import data_import as di


class Test_Math_Lib(unittest.TestCase):
    def test_no_folder(self):
        with self.assertRaises(ValueError):
            di.
