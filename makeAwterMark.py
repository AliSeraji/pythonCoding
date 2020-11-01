from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
import persian,json,sys,requests,argparse
from bidi.algorithm import get_display

DARK_THEME=1
LIGHT_THEME=2

IS_CONTINUES=1
IS_NOT_CONTINUES=0

colorRed='rgb(255,0,0)'
colorGreen='rgb(0,148,5)'
colorWhite='rgb(255,255,255)'
colorDarkGray='rgb(120,120,120)'
colorBlack='rgb(0,0,0)'
colorOrange='rgb(255,102,0)'

class Order():
    def __init__(self):
        self.price=[]
        self.volume=[]
        self.amount=[]
        self.numOfRealTrades=''
        self.numOfLegalTrades=''
        self.volumeOfRealTrades=''
        self.volumeOfLegalTrades=''
        
class TradeVariables():
    def __init__(self):
        self.symbolname=''
        self.volume=''
        self.symbolCondition=''
        self.symbolFullName=''
        self.tradeValue=''
        self.basevVolume=''
        self.realMoneyIncome=''
        self.lastPrice=''
        self.lastPricePercent=''
        self.finalPricePrercent=''
        self.finalPrice=''
        self.minValiPrice=''
        self.maxValidPrice=''
        self.yesterdayPrice=''
        self.buyOrder=Order()
        self.selOrder=Order()
        
def drawPositionedText(draw,x,text,y,fontSize,mainColor):
    color=mainColor
    for c in text:
        if c=='+':
            color=colorGreen
            break
        if c=='-':
            color=colorRed
            break
    font = ImageFont.truetype('IRANSansWeb (1).ttf', size=fontSize)
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    w,h=font.getsize(bidi_text)
    draw.text((x, y), bidi_text, fill=color, font=font)
    return x

def drawPositionedTextInLine(draw,width,text,y,fontSize,mainColor):
    color=mainColor
    for c in text:
        if c=='+':
            color=colorGreen
            break
        if c=='-' and mainColor==colorWhite:
            color=colorOrange
            break
        if c=='-' and mainColor==colorBlack:
            color=colorRed
            break
    font = ImageFont.truetype('IRANSansWeb (1).ttf', size=fontSize)
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    w,h=font.getsize(bidi_text)
    draw.text((width-w, y), bidi_text, fill=color, font=font)
    return width-w
        

def drawTextAtMiddle(imageWidth,draw,text,y,fontSize,color):
    font = ImageFont.truetype('IRANSansWeb (1).ttf', size=fontSize)
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    w,h=font.getsize(bidi_text)
    draw.text((((imageWidth-w)/2), y), bidi_text, fill=color, font=font)
        
def drawUpperSqare(draw,image,mainColor,instrument):
    w=0
    initial_text_1=" ارزش‌معاملات"
    initial_text_2=" حجم‌مبنا"
    initial_text_3=" ورود پول حقیقی"
    initial_text_4=" حجم"
    initial_text_5=" قیمت پایانی"
    initial_text_6=" آخرین قیمت"
    text=initial_text_1+persian.enToPersianNumb(" : "+instrument.tradeValue)
    drawTextAtMiddle(image.size[0],draw,text,380,35,mainColor)
    text=initial_text_2+persian.enToPersianNumb(" : "+instrument.basevVolume)
    drawTextAtMiddle(image.size[0],draw,text,455,35,mainColor)
    drawTextAtMiddle(image.size[0],draw,initial_text_3+persian.enToPersianNumb(" : "+instrument.realMoneyIncome),520,35,mainColor)
    drawTextAtMiddle(image.size[0],draw,initial_text_4+persian.enToPersianNumb(" : "+instrument.lastPrice),605,35,mainColor)
    
    w=drawPositionedText(draw,600,initial_text_5,680,35,mainColor)
    w=drawPositionedTextInLine(draw,w," : ",680,35,mainColor)
    w=drawPositionedTextInLine(draw,w,persian.enToPersianNumb(" ("+instrument.finalPricePrercent+"%) "),685,35,mainColor)
    drawPositionedTextInLine(draw,w,persian.enToPersianNumb(" "+instrument.finalPrice+" "),683,35,mainColor)

    w=drawPositionedText(draw,600,initial_text_6,745,35,mainColor)
    w=drawPositionedTextInLine(draw,w," : ",745,35,mainColor)
    w=drawPositionedTextInLine(draw,w,persian.enToPersianNumb(" ("+instrument.lastPricePercent+"%) "),750,35,mainColor)
    drawPositionedTextInLine(draw,w,persian.enToPersianNumb(" "+instrument.lastPrice+" "),748,35,mainColor)    
       
def drawMidShapeText(draw,image,mainColor,instrument):
    fontSize=35
    buyOrder=instrument.buyOrder
    selOrder=instrument.selOrder
    
    y=1000
    for i in range(len(buyOrder.amount)):
        drawPositionedText(draw,950,buyOrder.amount[i],y,fontSize,mainColor)
        drawPositionedText(draw,750,buyOrder.volume[i],y,fontSize,mainColor)
        drawPositionedText(draw,600,buyOrder.price[i],y,fontSize,mainColor)
        y+=100
    
    y=1000
    for i in range(len(selOrder.amount)):
        drawPositionedText(draw,100,selOrder.amount[i],y,fontSize,mainColor)
        drawPositionedText(draw,220,selOrder.volume[i],y,fontSize,mainColor)
        drawPositionedText(draw,380,selOrder.price[i],y,fontSize,mainColor)
        y+=100
                
def drawBottomShape(draw,image,mainColor,instrument):
    fontSize=40
    buyOrder=instrument.buyOrder
    selOrder=instrument.selOrder
    
    drawTextAtMiddle(1810,draw,buyOrder.numOfRealTrades,1530,fontSize,mainColor)
    drawPositionedText(draw,620,buyOrder.volumeOfRealTrades,1610,fontSize-5,mainColor)
    drawTextAtMiddle(1810,draw,buyOrder.numOfLegalTrades,1670,fontSize,mainColor)
    drawPositionedText(draw,620,buyOrder.volumeOfLegalTrades,1760,fontSize-5,mainColor)
    
    drawTextAtMiddle(300,draw,selOrder.numOfRealTrades,1530,fontSize,mainColor)
    drawPositionedText(draw,250,selOrder.volumeOfRealTrades,1610,fontSize-5,mainColor)
    drawTextAtMiddle(300,draw,selOrder.numOfLegalTrades,1670,fontSize,mainColor)
    drawPositionedText(draw,200,selOrder.volumeOfLegalTrades,1760,fontSize-5,mainColor)
    
    drawTextAtMiddle(1080,draw,persian.enToPersianNumb(instrument.yesterdayPrice),1350,fontSize,mainColor)
    drawTextAtMiddle(250,draw,persian.enToPersianNumb(instrument.minValiPrice),1350,fontSize,mainColor)
    drawTextAtMiddle(1900,draw,persian.enToPersianNumb(instrument.maxValidPrice),1350,fontSize,mainColor)
     
def parseInputArgs():
    instrumentID=0
    theme=''
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("name", help="Instrument name",type=str)
        parser.add_argument("theme", help="Result theme",type=int)
        args = parser.parse_args()
        instrumentName=args.name
        theme=args.theme
    except:
        e = sys.exc_info()[0]
        print(e)
    return instrumentID,theme

def percentTokenize(percent):
    num=''
    for c in percent[0:5:1]:
        num+=c
    return num
  
 
def reqPrase():
    name,theme=parseInputArgs()
    f=open('dataFile.json',"r",encoding='utf-8')
    data = json.load(f)
    instrument=TradeVariables()
    instrument.symbolname=str(data['Name'])
    instrument.symbolFullName=str(data['Title'])
    instrument.symbolCondition=" "+str(data['StatusDescription'])+" "
    instrument.minValiPrice=str(data['MinValidPrice'])
    instrument.maxValidPrice=str(data['MaxValidPrice'])
    instrument.yesterdayPrice=str(data['YesterdayPrice'])
    instrument.finalPrice=str(data['LastPrice'])
    instrument.basevVolume=str(int(data['BaseVolume'])/1000000)+"M"
    instrument.tradeValue=str(int(data['Cost']/1000000000))+"B"
    instrument.lastPrice=str(data['CurrPrice'])
    instrument.volume=str(int(data['Volume'])/1000000)+"M"
    #######################
    instrument.realMoneyIncome=persian.enToPersianNumb(str(data['InputMoney']))
    instrument.lastPricePercent=persian.enToPersianNumb(percentTokenize(str(data['DiffCurrPrice'])))
    instrument.finalPricePrercent=persian.enToPersianNumb(percentTokenize(str(data['DiffLastPrice'])))
    #######################
    for i in range(0,3):
        instrument.selOrder.amount.append(persian.enToPersianNumb(str(data['Q'][i]['CountBid'])))
        instrument.selOrder.price.append(persian.enToPersianNumb(str(data['Q'][i]['PriceBid'])))    
        instrument.selOrder.volume.append(persian.enToPersianNumb(str(data['Q'][i]['VolBid'])))
        instrument.buyOrder.amount.append(persian.enToPersianNumb(str(data['Q'][i]['CountBuy'])))
        instrument.buyOrder.volume.append(persian.enToPersianNumb(str(data['Q'][i]['VolBuy'])))
        instrument.buyOrder.price.append(persian.enToPersianNumb(str(data['Q'][i]['PriceBuy'])))
        
    instrument.buyOrder.volumeOfRealTrades=persian.enToPersianNumb(str(data['C']['VolumeAskIndv']))
    instrument.buyOrder.volumeOfLegalTrades=persian.enToPersianNumb(str(data['C']['VolumeAskNoneIndv']))
    instrument.buyOrder.numOfRealTrades=persian.enToPersianNumb(str(data['C']['CountAskIndv']))
    instrument.buyOrder.numOfLegalTrades=persian.enToPersianNumb(str(data['C']['CountAskNoneIndv']))
    
    instrument.selOrder.volumeOfRealTrades=persian.enToPersianNumb(str(data['C']['VolumeBidIndv']))
    instrument.selOrder.volumeOfLegalTrades=persian.enToPersianNumb(str(data['C']['VolumeBidNoneIndv']))
    instrument.selOrder.numOfRealTrades=persian.enToPersianNumb(str(data['C']['CountBidIndv']))
    instrument.selOrder.numOfLegalTrades=persian.enToPersianNumb(str(data['C']['CountBidNoneIndv']))
    
    return instrument,theme,name
     
 
def runProgram():
    instrument,theme,name=reqPrase()
    if theme==LIGHT_THEME:
        main(colorBlack,'Artboard – 26.jpg',str(name)+"-"+str(DARK_THEME),instrument)
    if theme==DARK_THEME:
        main(colorWhite,'Artboard – 25.jpg',str(name)+"-"+str(LIGHT_THEME),instrument)
    else:
        main(colorBlack,'Artboard – 26.jpg',str(name)+"-"+str(DARK_THEME),instrument)
    

def main(mainColor,path,name,instrument):
    image=Image.open(path)
    draw = ImageDraw.Draw(image)
    
    (x, y) = (470, 60)
    drawTextAtMiddle(image.size[0],draw,instrument.symbolname,y,70,mainColor)
    
    (x, y) = (390, 170)
    drawTextAtMiddle(image.size[0],draw,"("+instrument.symbolCondition+")",y,50,colorDarkGray)
     
    (x, y) = (340, 250)
    drawTextAtMiddle(image.size[0],draw,instrument.symbolFullName,y,50,colorDarkGray)
    
    drawUpperSqare(draw,image,mainColor,instrument)
    drawMidShapeText(draw,image,mainColor,instrument)
    drawBottomShape(draw,image,mainColor,instrument)
    
    image.save(name+'.jpg')
    print(name+'.jpg',end='@')
    return 0
    

runProgram()
    