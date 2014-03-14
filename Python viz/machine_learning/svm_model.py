# import saved_data
import sklearn
import pickle 

dataset=pickle.load(open('all_samples.p','rb'))
print dataset[0]
##### INCOMPLETE