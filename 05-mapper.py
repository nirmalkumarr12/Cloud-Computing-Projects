 #!/usr/bin/env python
import sys

def mapper():
	p=0;
	for line in sys.stdin:
		data=line.split(',')
		
		year=data[0]
		month=data[1]
		sec_delay=data[11]
		
			



		if(sec_delay!='0'):
			print "{0},{1},1".format(year,month)
		



mapper()


