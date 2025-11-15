import threading
from Finger_counter import exec
from RotateControl import exec1



def program1():
    # 程式1的程式碼
    exec()

def program2():
    # 程式2的程式碼
    exec1()




if __name__ == '__main__':
    # 建立兩個執行緒
    t1 = threading.Thread(target=program1)
    t2 = threading.Thread(target=program2)

    # 開始執行執行緒
    t1.start()
    t2.start()


    # 等待兩個執行緒結束
    t1.join()
    t2.join()

