import time

def main() :
    
    initTime = time.time()

    time.sleep(2)

    print (int(time.time()-initTime))

if __name__ == '__main__':
    main()