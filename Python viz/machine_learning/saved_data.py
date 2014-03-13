import os
import pickle

def get_all():
	all_data=[]
	labels=[]
	dir_name=os.path.join('..','saved_animations_and_data')
	sample_sets=os.listdir(dir_name)
	for sample_set in sample_sets:
		if sample_set!= '.DS_Store':
			try: csv_file=os.path.join(dir_name,sample_set,os.listdir(os.path.join(dir_name,sample_set))[0])
			except:pass
			with open(csv_file) as f:
				if labels==[]:
					labels=[label.strip()  for label in f.readline().split(",")]
					print labels
				else:
					f.readline()#get rid of the header row
				for line in f:
					row=line.split(",")
					row[2]=int(row[2])
					row[3:]=[float(i) for i in row[3:]]
					all_data.append(row)
	return all_data


if __name__ == '__main__':
	get_all()