# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 19:02:38 2022

@author: narut
"""

import tkinter   # 引入tkinter 模組
import re     # 引入正則表示式模組
top = tkinter.Tk()    # 創建主視窗
f1 = tkinter.Frame(top)  # 在主視窗上創建一矩形區域 frame1(for display)
f2 = tkinter.Frame(top)  # 在主視窗上創建一矩形區域 frame2(for buttons)

var = tkinter.StringVar()  # 創建一StringVar物件，用以儲存顯示的string
var.set("0") # 將var設為”0”

def compute(x1, x2, operator):  # 此函數根據input的運算子對兩input進行對應的運算
    if operator == "+":
        return x1 + x2
    elif operator == "-":
        return x1 - x2
    elif operator == "x":
        return x1 * x2
    elif operator == "/":
        if x2 == 0:    # 若除的對為0，則顯示 ma error
            var.set("ma error")
            return 0
        else:
            return x1 // x2

def SetValue(): # 在f1上建立一label，其顯示的為var中的字串
    Screen = tkinter.Label(f1, textvariable = var).grid(row = 0, column = 1)

# 其實可以加一個變數儲存目前顯示的是否為運算結果，
# 並在此CLick函數判斷此變數來決定點擊按鈕是否產生反應
# 但題目沒強制要求就沒加了 
def Click(x): 
    if var.get() == "syntax error" or var.get() == "ma error":
        pass   # 若當前顯示的為錯誤訊息，不做動作
    else:     # 否則在當前字串後方加上輸入字符
        var.set(var.get() + str(x))

def Clear():   # 將顯示的字串清為0
    var.set(0)

# 以下有兩個進行四則運算的方式
# 法一:直接利用內建eval函數，簡單快速但有點投機
def Calculate():  
    eq = var.get()  # 取得var當前存的字串
	
	# 判斷輸入字串有無語法錯誤
    if eq[0] in "+x/" or eq[-1] in "+-x/": # 頭不得為+x/(-代表負號)
        var.set("syntax error")
        return
    for i in range(len(eq) - 1):  # 判斷有無連續運算子(不含代表負號的-)
        if eq[i] in "+-x/" and eq[i + 1] in "+-x/":
            if eq[i + 1] != "-":
                var.set("syntax error")
                return

    eq = eq.replace('x', '*') # 將eq內的x替換成*，因為eval定義*為乘號
    if "/0" in eq:   # 若輸入有除以零，則顯示 ma error
        var.set("ma error")
        return
    if eq[0] == "0":  # 由於eval輸入字串的開頭不得為0，所以先去掉開頭的0
        result = int(eval(eq.split("0")[1]))
    else:
        result = eval(eq)
    var.set(result)  # 顯示運算結果

# 法二:利用迴圈一個一個處理每個運算子(此寫法不考慮輸入包含負號)
def Calculate_alt():
    eq = var.get()
	
# 判斷輸入字串有無語法錯誤
    if eq[0] in "+-x/" or eq[-1] in "+-x/":
        syn_error = True
        var.set("syntax error")
        return
    for i in range(len(eq) - 1):
        if eq[i] in "+-x/" and eq[i + 1] in "+-x/":
            var.set("syntax error")
            return
	
    # 建立儲存輸入式中所有數字的list
    operand_list = re.split("\+|-|x|/", eq) # 利用re模組的split函數
    operand_list.insert(0, "0") # 運算需求在頭尾加0
    operand_list.append("0")
    operand_list = [int(i) for i in operand_list]
	
	# 建立儲存輸入式中所有運算子的list
    operator_list = re.split("1|2|3|4|5|6|7|8|9|0", eq)
    operator_list = list(filter(lambda n: n != "", operator_list))
    operator_list.insert(0, "+")  # 濾掉list中的空白，頭尾加’+’,’=’
    operator_list.append("=")
	
	# 以下以迴圈進行計算
    i3 = 2
    num1 = operand_list[0]
    num2 = operand_list[1]
    num3 = operand_list[i3]

    j3 = 2
    op1 = operator_list[0]
    op2 = operator_list[1]
    op3 = operator_list[j3]

    while op3 != "=":
        if op2 == 'x' or op2 == '/':
            if op2 == '/' and num3 == 0:
                var.set("ma error")
                break
            else:
                num2 = compute(num2, num3, op2)
                op2 = op3

                i3 = i3 + 1
                op3 = operator_list[i3]
                j3 = j3 + 1
                num3 = operand_list[j3]
        else:
            num1 = compute(num1, num2, op1)
            op1 = op2

            num2 = num3
            op2 = op3

            i3 = i3 + 1
            op3 = operator_list[i3]
            j3 = j3 + 1
            num3 = operand_list[j3]

    if op2 == 'x' or op2 == '/':
        if op2 == '/' and num3 == 0:
            var.set("ma error")
        else:
            var.set((str)(compute(num1, compute(num2, num3, op2), op1)))
    else:
        var.set((str)(compute(compute(num1, num2, op1), num3, op2)))

# 呼叫SetValue函數
SetValue()

# 在f2建立所需按鈕，並設定其大小、位置及點擊所對應的函數
btn7 = tkinter.Button(f2,text = "7",borderwidth = 5,width = 5,height = 5, command = lambda : Click("7")).grid(row = 0,column = 0)
btn8 = tkinter.Button(f2,text = "8",borderwidth = 5,width = 5,height = 5, command = lambda : Click("8")).grid(row = 0,column= 1)
btn9 = tkinter.Button(f2,text = "9",borderwidth = 5,width = 5,height = 5, command = lambda : Click("9")).grid(row = 0,column= 2)
btnPlus = tkinter.Button(f2,text = "+",borderwidth = 5,width = 5,height = 5, command = lambda : Click("+")).grid(row = 0,column= 3)
btn4 = tkinter.Button(f2,text = "4",borderwidth = 5,width = 5,height = 5, command = lambda : Click("4")).grid(row = 1,column= 0)
btn5 = tkinter.Button(f2,text = "5",borderwidth = 5,width = 5,height = 5, command = lambda : Click("5")).grid(row = 1,column= 1)
btn6 = tkinter.Button(f2,text = "6",borderwidth = 5,width = 5,height = 5, command = lambda : Click("6")).grid(row = 1,column= 2)
btnMinus = tkinter.Button(f2,text = "-",borderwidth = 5,width = 5,height = 5, command = lambda : Click("-")).grid(row = 1,column= 3)
btn1 = tkinter.Button(f2,text = "1",borderwidth = 5,width = 5,height = 5, command = lambda : Click("1")).grid(row = 2,column= 0)
btn2 = tkinter.Button(f2,text = "2",borderwidth = 5,width = 5,height = 5, command = lambda : Click("2")).grid(row = 2,column= 1)
btn3 = tkinter.Button(f2,text = "3",borderwidth = 5,width = 5,height = 5, command = lambda : Click("3")).grid(row = 2,column= 2)
btnX = tkinter.Button(f2,text = "x",borderwidth = 5,width = 5,height = 5, command = lambda : Click("x")).grid(row = 2,column= 3)
btn0 = tkinter.Button(f2,text = "0",borderwidth = 5,width = 5,height = 5, command = lambda : Click("0")).grid(row = 3,column= 0)
btnClear = tkinter.Button(f2,text = "C",borderwidth = 5,width = 5,height = 5, command = Clear).grid(row = 3,column= 1)
btnEqual = tkinter.Button(f2,text = "=",borderwidth = 5,width = 5,height = 5, command = Calculate).grid(row = 3,column= 2)
btnDiv = tkinter.Button(f2,text = "/",borderwidth = 5,width = 5,height = 5, command = lambda : Click("/")).grid(row = 3,column= 3)
# 用pack方法進行排版(預設為由上而下)
f1.pack()
f2.pack()
top.mainloop() # 呼叫mainloop

