'''
@Auther: Charles Wang
@Date: 3/17/2014
@Note:
in the "test" folder:
bicep_1 to bicep_5: Morgan's data
bicep_6 to bicep_10: Lazar's data
same nomenclature apply to tricep and shoulder
'''
import csv, glob

test_directory = "test\\"

correct_predictions = []
wrong_predictions = []
counts_diff_from_ten = []

def predict_exercise_type(acc_x_avg, acc_y_avg, acc_z_avg):
    if acc_y_avg > acc_z_avg and acc_z_avg > acc_x_avg:
        return "bicep"
    elif acc_y_avg > acc_x_avg and acc_x_avg > acc_z_avg:
        return "tricep"
    else:
        return "shoulder"

def calculate_slope(data, interval): # inverval is used for dimensionality reduction
    shortend_data = []
    slope = []
    slope_changed = [] # 1 if slope sign changes, 0 otherwise
    for i, num in enumerate(data):
        if i % interval == 0:
            shortend_data.append(num)
    pointer = 0
    while pointer < len(shortend_data) - 1:
        slope.append(shortend_data[pointer + 1] - shortend_data[pointer])
        pointer += 1
    pointer2 = 0
    while pointer2 < len(slope) - 1:
        if slope[pointer2 + 1] * slope[pointer2] < 0:
            slope_changed.append(1)
        else:
            slope_changed.append(0)
        pointer2 += 1
    return slope_changed.count(1) / 2
    
def process_csv_files():
    for files in glob.glob(test_directory + "*.csv"):
        # initialize variables
        acc_x = []
        acc_y = []
        acc_z = []
        gyro_x = []
        gyro_y = []
        gyro_z = []
        magnet_x = []
        magnet_y = []
        magnet_z = []
        # record counts
        count = 0
        # open csv files
        cr = csv.reader(open(files,"rb"))
        file_name = files.replace("test\\","")
        exercise_type = "default"
        # write variables
        for i, row in enumerate(cr):
            if i is 1:
                exercise_type = row[1].split(" ")[0]
            if i > 0:
                acc_x.append(float(row[4]))
                acc_y.append(float(row[5]))
                acc_z.append(float(row[6]))
                gyro_x.append(float(row[7]))
                gyro_y.append(float(row[8]))
                gyro_z.append(float(row[9]))
                magnet_x.append(float(row[10]))
                magnet_y.append(float(row[11]))
                magnet_z.append(float(row[12]))
        # remove noise in data
        acc_x = acc_x[:-5]
        acc_y = acc_y[:-5]
        acc_z = acc_z[:-5]
        # some basic calculation
        print "---------------------------------------"
        print "##### processing " + file_name + " #####"        
        acc_x_avg = sum(acc_x)/len(acc_x)
        acc_y_avg = sum(acc_y)/len(acc_y)
        acc_z_avg = sum(acc_z)/len(acc_z)
        acc_x_max = max(acc_x)
        acc_y_max = max(acc_y)
        acc_z_max = max(acc_z)
        '''
        print "----- summary -----"
        print "acc_x avg: " + str(acc_x_avg)
        print "acc_y avg: " + str(acc_y_avg)
        print "acc_z avg: " + str(acc_z_avg)
        print "acc_x max: " + str(acc_x_max)
        print "acc_y max: " + str(acc_y_max)
        print "acc_z max: " + str(acc_z_max)
        '''
        prediction = predict_exercise_type(acc_x_avg, acc_y_avg, acc_z_avg)
        sample_rate = 5 
        count = min([calculate_slope(acc_x, sample_rate), calculate_slope(acc_y, sample_rate), calculate_slope(acc_z, sample_rate)])
        print "predict: " + prediction
        print "correct: " + exercise_type
        print "count: " + str(count)
        if prediction == exercise_type:
            correct_predictions.append(file_name)
        else:
            wrong_predictions.append(file_name)
        counts_diff_from_ten.append(abs(count - 10))

def prediction_accuracy():
    print "===== correct predictions ====="
    print correct_predictions
    print "===== wrong predictions ====="
    print wrong_predictions
    accuracy = float(len(correct_predictions)) / (len(correct_predictions) + len(wrong_predictions))
    print "Total prediction accuracy: " + str(accuracy * 100) + "%"
    print "Total count (correct=10) accuracy: " + str(1 - float(sum(counts_diff_from_ten)) / (len(counts_diff_from_ten) * 10)) + "%"

if __name__ == "__main__":
    process_csv_files()
    prediction_accuracy()
    
