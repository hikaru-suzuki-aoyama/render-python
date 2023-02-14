
def id_read():
    f = open('LINE_id_itiran.txt', 'r')

    datalist = f.readlines()

    for i in range(len(datalist)):
        datalist[i] = datalist[i].replace('\n', '')

    LINE_id_dict = {}

    for i in range(len(datalist)):
        LINE_id_dict[datalist[i].split(":")[0]] = datalist[i].split(":")[1]

    f.close()

    return LINE_id_dict


def id_write(kidname,line_id):
    with open('LINE_id_itiran.txt', 'a') as f:
        print(kidname + ":" + line_id, file=f)