import logging
from sgcalculator.src.exceptions import InvalidInputException

logging.basicConfig(filename='calculator.log',level=logging.DEBUG)

class Calculator(object):
    """Finds the year(s) with the highest number of persons alive given a list of
        data points of the form (name, birth date, end date).
       Note: If someone dies in 1978, she/he is not counted as alive in 1978.
    
    """
    
    def _validate(self, data):
        try:
            if type(data) is not list:
                raise InvalidInputException("Input Data must be of type list.")
            for item in data:
                if type(item[0]) is not str:
                    raise InvalidInputException("First Tuple element must be a sting. Got %s."%type(item[0]))
                if type(item[1]) is not int:
                    raise InvalidInputException("Second Tuple element must be an integer. Got %s."%type(item[1]))
                if item[1] < 1900:
                    raise InvalidInputException("Second Tuple element must be at least 1900. Got %s."%item[1])
                if type(item[2]) is not int:
                    raise InvalidInputException("Third Tuple element must be an integer. Got %s."%type(item[2]))
                if item[2] > 2000:
                    raise InvalidInputException("Third Tuple element must be at most 2000. Got %s."%item[2])
                if item[2] - item[1] < 0:
                    raise InvalidInputException("End Date (%s) cannot come after Birth Date(%s)."%(item[2], item[1]))
                if len(item) !=3:
                    raise InvalidInputException("Invalid data format")
        except IndexError:
            raise InvalidInputException("Invalid data format"))
            
    def _transform(self, data):
        tdata = []
        for item in data:
            datum = list(map(lambda x: int(x >= (item[1] -1900) and  x < (item[2] -1900) ),list(range(100))))
            logging.debug('interval: %s - %s. Transform: %s.'%(item[1], item[2], datum))
            tdata.append(datum)
        return tdata
    
    def _getMax(self, data):
        sdata = [0]*100
        for item in data:
            datum = list(map(lambda (i,x): sdata[i] + x, enumerate(item)))
            sdata = datum
        maxVal = max(sdata)
        logging.info('max occurance %s'%maxVal)
        return [i+1900 for i, x in enumerate(sdata) if x == maxVal]
    
    def _cleanData(self, data):
        cdata = sorted(data)
        logging.debug('cleaned data: %s.'%cdata)
        return cdata
        
    def getMax(self, indata):
        """ Calculates the year(s) with the highest number of persons alive.
        
        Args:
        param1 (List of tuples): Example (str, int, int).
        
        Raises:
        InvalidInputException: If input has errors .
        
        """
        self._validate(indata)
        data = self._transform(indata)
        return self._cleanData(self._getMax(data))
        
