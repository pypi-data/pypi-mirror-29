import unittest
from sgcalculator.src.exceptions import InvalidInputException
from sgcalculator.src.calculator import Calculator

class TestExceptionMethods(unittest.TestCase):
    
    indata = [('sara', 1921, 1953),('Jane', 1943, 1987),('Jose', 1903, 1954),('Josh', 1981, 2000),
              ('Oni', 1960, 1993),('Li', 1923, 1994),('Derick', 1910, 1977),('Joe', 1936, 1990),
              ('Jeseph', 1943, 1987),('Jay', 1912, 1966),('Xu', 1941, 1991),('Lin', 1901, 1921),
              ('Danny', 1900, 1977),('Sai', 1930, 1985),('Uri', 1913, 1967),('Eric', 1963, 1979),
              ('Tom', 1919, 1961),]
        
    indata1 = [('sara', 1921, 1953),('Jane', 1943, 1987),('Jose', 1903, 1954),('Josh', 1981, 2000),
             ('Oni', 1960, 1993),('Li', 1923, 1994),('Derick', 1910, 1977),('Joe', 1936, 1990),
             ('Jeseph', 1943, 1987),('Jay', 1912, 1966),('Xu', 1941, 1991),('Lin', 1901, 1921),
             ('Danny', 1900, 1977),('Sai', 1930, 1985),('Uri', 1913, 1967),('Eric', 1963, 1979),
             ('Tom', 1919, 1961),('Jake', 1908, 1992),('Rod', 1944, 1994),('ciara', 1973, 1996),
             ('Zen', 1937, 1974),('Zoe', 1908, 1909),('Emily', 1953, 1984),('Sage', 1950, 1983),
             ('Kay', 1993, 1999),('Lane', 1900, 2000),('Cary', 1920, 1980),('Chris', 1930, 1970),
             ('Landon', 1940, 1947),('Murr', 1925, 1955),]
    
    def test_NotNull(self):
        self.assertIsNotNone(Calculator())
        
    def test_InvalidInputType(self):
        input0 = {'jess': (1990, 1967), 'tim': (1933,1999) }
        cal = Calculator()
        self.assertRaises(InvalidInputException, cal.getMax, input0 )
        
    def test_InvalidInputData0(self):
        input0 = [('jess', 1991, 1998), ('tim', 1899, 1992)]
        cal = Calculator()
        self.assertRaises(InvalidInputException, cal.getMax, input0 )
        
    def test_InvalidInputData1(self):
        input0 = [('jess', 1991, 1998), ('tim', 1993, 2023)]
        cal = Calculator()
        self.assertRaises(InvalidInputException, cal.getMax, input0 )

    def test_InvalidInputData2(self):
        input0 = [('jess', 1991, 1938), ('tim', 1933, 1978)]
        cal = Calculator()
        self.assertRaises(InvalidInputException, cal.getMax, input0 )
            
    def test_sample1(self):
        input0 = [('jess', 1991, 1998), ('tim', 1991, 1992)]
        expected = [1991,]
        result = Calculator().getMax(input0)
        self.assertEqual(set(expected), set(result))
        
    def test_sample2(self):
        input0 = [('jess', 1900, 1998), ('tim', 1991, 1992), ('steph', 1939, 1941) ]
        expected = [1991,1939, 1940]
        result = Calculator().getMax(input0)
        self.assertEqual(set(expected), set(result))
        
    def test_sample3(self):
        input0 = [('jess', 1920, 1920), ('tim', 1991, 1992), ('steph', 1939, 1941) ]
        expected = [1991, 1939, 1940]
        result = Calculator().getMax(input0)
        self.assertEqual(set(expected), set(result))

    def test_sample4(self):
        input0 = self.indata
        expected = range(1943,1953)
        result = Calculator().getMax(input0)
        self.assertEqual(set(expected), set(result))
    
    def manualTest(self):
        input0 = self.indata1
        expected = []
        result = Calculator().getMax(input0)
        self.assertEqual(set(expected), set(result))
        
    
if __name__ == '__main__':
    unittest.main()
