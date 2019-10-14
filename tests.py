import unittest
import os
import random
import decimal
import statistics
import datetime
import data_import as di


class Test_Math_Lib(unittest.TestCase):

    def test_linear_search(self):
        file = './smallData/activity_small.csv'
        instance = di.ImportData(file)
        datim = datetime.datetime(2018, 3, 12, 0, 0, 0, 0)
        output = instance.linear_search_value(datim)
        self.assertEqual(output, [0])

    def test_ImportData_class(self):
        '''
        Assert that the length of the time column matches the length of the
        value column
        '''
        file = './smallData/basal_small.csv'
        instance = di.ImportData(file)
        self.assertEqual(len(instance._time), len(instance._value))

    def test_print_array(self):
        files = os.listdir('smallData')
        data = []
        for f in files:
            data.append(di.ImportData('smallData/'+f))
        data_5 = []
        for instance in data:
            data_5.append(di.roundTimeArray(instance, 5))

        rtr = di.printArray(data_5, files, 'out_5', 'hr_small.csv')
        self.assertNotEqual(rtr, -1)
        self.assertTrue(os.path.exists('out_5.csv'))
        os.remove('out_5.csv')

    def test_replace_high_low(self):
        file = open('bolus_replace_tester.csv', 'w')
        file.write('time,value\n')
        file.write('4/20/18 4:20,low\n')
        file.write('4/21/18 4:21,high')
        file.close()
        instance = di.ImportData('bolus_replace_tester.csv')
        self.assertEqual(instance._value[0], 40)
        self.assertEqual(instance._value[1], 300)
        os.remove('bolus_replace_tester.csv')


if __name__ == '__main__':
    unittest.main()
