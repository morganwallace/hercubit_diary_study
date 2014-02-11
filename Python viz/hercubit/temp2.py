
def get_data_from_serial():
    global ser
    serialOutput=ser.readline()
    serialTuple=serialOutput.split(",")
    if len(serialTuple)!=3:
        return None
    for i in range(len(serialTuple)):
        try:serialTuple[i]=float(serialTuple[i].strip())
        except: return None
    x, y, z = serialTuple[0],serialTuple[1],serialTuple[2]
    t=time.time()
    return t,x,y,z

def run():
    