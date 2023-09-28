import numpy as np
import matplotlib.pyplot as plt

def line():
    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")

def line1():
    print("..............................................................")
    print("")

def compare(x): #コンパレータ
    if 0 < x:
        return VinMax, 1 #　DAC出力　Vout出力　の順で表記
    else:
        return VinMin, 0

def integrator(new,old):
    ans = old+new #積分器　1っこ前の値と新しい入力を足して　積分動作
    return ans

def adder(dVin,dDAC):  #加算器　dVin→入力　ｄDAC→DAC
    ans = dVin-dDAC
    return ans

line()
print("このプログラムはインバータ積分器の必要性能を割り出す計算プログラムです。")

line()
print("想定される最大入力電圧を入力してください。 単位は[V]です。")
VinMax = float(input())
VinMin = -VinMax                            #入力電圧範囲の最大最少の絶対値が同じ値を想定　　±○○　を想定
line1()
print("入力電圧範囲を", VinMin, "～", VinMax, "[V]に設定しました。")

line()
print("サンプリング周波数を入力してください。　単位は[kHz]です。")
samplingF = float(input())
line1()
print("サンプリング周波数を", samplingF, "[kHz]に設定しました。")
samplingF = samplingF*1000          #　単位が　kHzだから　×　千
samplingT = 1/samplingF             #　周波数＝1/周期　だから　周期を求めてる。

line()
Vinput = 4          #エラー処理用に　いい加減な値を代入
print("入力波形を選んでください")
print("0:直流　1:正弦波　2:方形波　3:三角波")
Vinput = int(input())
while True:
    if Vinput == 0 or Vinput == 1 or Vinput == 2 or Vinput == 3:
        break
    print("入力波形を以下の中から選んでください。")
    print("0:直流　1:正弦波　2:方形波　3:三角波")
    Vinput = int(input())

line1()
if Vinput == 0:
    print("入力波形を　直流　に設定しました。")
elif Vinput == 1:
    print("入力波形を　正弦波　に設定しました。")
elif Vinput == 2:
    print("入力波形を　方形波　に設定しました。")
else:
    print("入力波形を　三角波　に設定しました。")

line()
print("入力電圧を入力してください。　単位は[V]です。")
VinA = float(input())

while VinMax < VinA and VinMin > VinA:
    line()
    print("入力電圧", VinA, "[V]が入力電圧範囲", VinMin, "～", VinMax, "[V]を超えています")
    print("入力電圧範囲内で入力電圧を入力してください。")
    VinA = float(input())

line1()
print("入力電圧を", VinA, "[V]に設定しました。")

if Vinput != 0:
    line()
    print("入力信号の周波数を入力してください。　単位は[kHz]です。")
    VinF = float(input())
    line1()
    print("入力信号の周波数を", VinF, "[kHz]に設定しました。")
    VinF = VinF * 1000
    VinT = 1 / VinF

renzokuP = 0
renzokuM = 0
cnt = 0
Vintold = 0
DAC = VinMin
VaddMax = 0
VaddMin = 0
VintMax = 0
VintMin = 0
Voutold = 0
VoutP = 0
VoutM = 0
MaxVoutP = 0
MaxVoutM = 0
out = []    #出力波形を入れておく配列

Voutold1 = 0
Voutold2 = 0
Voutold3 = 0
Voutold4 = 0
Voutold5 = 0
Voutold6 = 0
Voutold7 = 0
Voutold8 = 0
Voutold9 = 0
Voutold10 = 0

outout = [] #DA変換されたあとの波形を入れておく配列

Vinhakei = []   #入力波形を入れておく配列

line()
print("演算回数を入れてください。　単位は[千回]です。")
cntt = int(input())
line1()
print(cntt,"回演算します。")
cntt = cntt*1000


while cnt < cntt: #ここの数字を変えると　計算回数を変えられる

    # line()
    # print(cnt+1,"回目の計算です。")

    if Vinput == 0:     #　入力波形を生成するプログラム
        Vin = VinA
    elif Vinput == 1:
        T = samplingT*cnt
        Vin = VinA*np.sin(2*np.pi*VinF*T)
    elif Vinput == 2:
        T = samplingT*cnt
        t = T%VinT
        if t < VinT/2:
            Vin = VinA
        else:
            Vin = -VinA
    else:
        T = samplingT * cnt
        t = T % VinT
        if t < VinT / 2:
            Vin = -VinA+2*VinA*(t/(VinT/2))
        else:
            Vin = VinA-2*VinA*((t-VinT/2)/(VinT/2))

    Vinhakei.append(Vin)
    Vadd = adder(Vin,DAC)

    if VaddMin > Vadd: #加算器出力の　最大最小値を更新していく　ブロック
        VaddMin = Vadd
    if VaddMax < Vadd:
        VaddMax = Vadd

    Vint = integrator(Vadd,Vintold)
    Vintold = Vint #　古い値をここで更新

    if VintMin > Vint: #積分器出力の　最大最小値を更新していく　ブロック
        VintMin = Vint
    if VintMax < Vint:
        VintMax = Vint

    DAC, Vout = compare(Vint)

    if Vout == Voutold:
        if Vout == 0:
            VoutM = VoutM+1
        else:
            VoutP = VoutP+1
    else:
        if Voutold == 0:
            VoutM = 0
        else:
            VoutP = 0

    if MaxVoutM < VoutM:  #コンパレータ出力の　最大カウント回数を更新していく　ブロック
        MaxVoutM = VoutM
    if MaxVoutP < VoutP:
        MaxVoutP = VoutP

    out.append(Vout)    # コンパレータ出力をためる配列
    Voutold = Vout   #　連続して　０　１　　が出力されているかどうかを判定するための比較用

    Voutold10 = Voutold9
    Voutold9 = Voutold8
    Voutold8 = Voutold7
    Voutold7 = Voutold6
    Voutold6 = Voutold5
    Voutold5 = Voutold4
    Voutold4 = Voutold3
    Voutold3 = Voutold2
    Voutold2 = Voutold1
    Voutold1 = DAC
    Voutout = (Voutold10 + Voutold9 + Voutold8 + Voutold7 + Voutold6 + Voutold5 + Voutold4 + Voutold3 + Voutold2 + Voutold1) / 10
    outout.append(Voutout)      #　ad変換された値を配列に代入


    # print("Vout=",Vout,"Vadd=",Vadd,"Vint=",Vint,"DAC=",DAC)
    cnt = cnt+1

line()
line1()
line()
print("加算器の出力の最小電圧は",VaddMin,"[V]で最大電圧は",VaddMax,"[V]でした。")
print("積分器出力の最小電圧は",VintMin,"[V]で最大電圧は",VintMax,"[V]でした。")
print("出力の「 0 」が連続する回数は",MaxVoutM,"回で、「 1 」が連続する回数は",MaxVoutP,"回でした。")


# plt.plot(out, color="red")　　　　　　　　＃こっからマトラボの関数を使ってるよ
plt.plot(outout, color="blue")
plt.plot(Vinhakei, color="magenta")

plt.show()



