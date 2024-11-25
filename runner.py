from apphandler import AppHandler

if __name__ == "__main__":
    # AppHandler().start()
    filename = "file21.txt"
    f = open(filename, "w")
    buf =["ueueueu\n", "032032jjr\n"]
    for i in range(len(buf)):
        f.write(buf[i])
