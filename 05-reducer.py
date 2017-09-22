 #!/usr/bin/env python
import sys


def reducer():
	oldyear=None
	oldmonth=None
	count=0
	print "year,month,count"
	for line in sys.stdin:
		data=line.strip().split(',')
		year,month,cnt=data
		tip=year+'-'+month
		if oldyear and oldyear!=tip:
			print "{0},{1}".format(tip,count)
			count=0
		oldyear=tip
		
		count+=1
	if oldyear and oldmonth:
		print "{0},{1}".format(oldyear,count)


reducer()



