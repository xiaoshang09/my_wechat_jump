import os
import time

num_list=['540 1480','260 740','540 740','825 740','260 980'
    ,'540 980','825 980','260 1230','540 1230','825 1230']

def input_code(code):
    code=str(code)
    for each in code:
        each=int(each)
        num_p=num_list[each]
        print('%d >>> %s'%(each,num_p))
        os.system('adb shell input swipe {} {} 50'.format(num_p,num_p))

os.system('adb shell input keyevent 26')
os.system('adb shell input swipe 800 800 800 400 200')
#os.system('adb shell input swipe 400 800 800 1200 6000')
input_code(314667)
