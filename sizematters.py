import sys
import math

#1 file containing file path to picard tools insert size
#2 file containing file path to fluffy output csv

input_files=[]
for line in open(sys.argv[1]):
	input_files.append(line.strip())

ffy={}
first=True
for file in open(sys.argv[2]):
	for line in open(file.strip()):
		content=line.strip().split("\",\"")
		if content[-8] == "FFY":
			continue

		if content[8] != "":
			continue
	
		ff=float(content[-8])
		if ff < 0.5:
			continue
		ffy[ content[0].strip("\"")  ]=str(ff)

bin_size=2
min_pos=60
max_pos=450

total_counts={}
all_data={}
for file in input_files:
	data_found=False
	total_counts[file]=0
	all_data[file]={}

	for line in open(file):

		if not data_found:
			if line.startswith("insert_size"):
				data_found=True
			continue
		if line.strip() =="":
			continue
		size=int(line.strip().split()[0])

		if size < min_pos:
			continue
		if size > max_pos:
			continue

		fragments=int(line.strip().split()[1])

		total_counts[file]+=int(line.strip().split()[-1])

		p=int(math.floor( (size-1)/bin_size ))*bin_size

		all_data[file][p]=fragments

		

		
#print(total_counts)
#print(all_data)
#quit()

positions=set([])
for sample in all_data:
	for p in all_data[sample]:
		positions.add(p)

positions=sorted(list(positions))
print( "Sample,"+",".join(map(str,positions))+",FFY" )

for sample in all_data:
	id=sample.split("/")[-1].split(".")[0]
	out=[id]
	if not id in ffy:
		continue

	for position in positions:

		if position in all_data[sample]:
			all_data[sample][position]=all_data[sample][position]/float(total_counts[sample])
		else:
			#print("hej")
			all_data[sample][position]=0

		out.append(str(all_data[sample][position]))
	out.append(ffy[id])
	print( ",".join(out) )
