
# -*- coding:utf-8 -*-

import pygame
import func
import pickle

pygame.init()

window = [800,600]
screen = pygame.display.set_mode(window)
pygame.display.set_caption("python life game")
clock = pygame.time.Clock()

green = pygame.color.Color("#99dd6f")
black = pygame.color.Color("#000000")
reccolor = pygame.color.Color("#ff2222")
background = pygame.Surface(screen.get_size()).convert()
background.fill((0,0,0))


arrow = pygame.image.load("pic\\arrow.png").convert_alpha()
up= func.Picture(arrow,(365,20),0,(50,50))
down = func.Picture(arrow,(365,515),180,(50,50))
left = func.Picture(arrow,(35,260),90,(50,50))
right = func.Picture(arrow,(715,260),270,(50,50))
toolbu = func.Picture(pygame.image.load("pic\\toolbu.png").convert_alpha(),(30,30),0,(60,60))
toollabel = func.Picture(pygame.image.load("pic\\toollabel5.png").convert_alpha(),(30,30),0,(500,600))
toolcap = func.Picture(pygame.image.load("pic\\toolcap1.png").convert_alpha(),(0,0),0,(800,600))
smallcap = func.Picture(pygame.image.load("pic\\toollasmallcap.png").convert_alpha(),(30,30),0,(60,60))
textcap = func.Picture(pygame.image.load("pic\\butextcap3.png").convert_alpha(),(60,100),0,(225,60))
textcapsmall = func.Picture(pygame.image.load("pic\\butextcap3.png").convert_alpha(),(0,0),0,(125,30))
label = func.Picture(pygame.image.load("pic\\label2.png").convert_alpha(),(330,130),0,(400,300))
label.animate([pygame.image.load("pic\\label3.png").convert_alpha()])
addlabel = func.Picture(pygame.image.load("pic\\addlabel1.png").convert_alpha(),(200,140),0,(400,150))
selectlabel = func.Picture(pygame.image.load("pic\\addlabel1.png").convert_alpha(),(340,10),0,(400,400))

toollabel.horcount = -500
piclist = [up,down,left,right]

speed_text = func.Font("3/s",(45,window[1]-75),30)
state = func.Font(" ",(window[0]-185,window[1]-75),30)
welcome = func.Font("Click to place life",(180,240),40)
introduction = func.Font("introduction",(95,110),28,textcap)
helptext = func.Font("how to play",(95,170),28,textcap)
module = func.Font("modules",(95,230),28,textcap)
clearup = func.Font("clear",(95,470),28,textcap)
clearup.coloring(28,(160,230,220))
introtext = func.Font("LIFE GAME\n \n2 or 3 -> survive\n3 -> born\nothers -> die",(370,160),22)
introlist = func.paragraph(introtext,2,1,5)
hetext = func.Font("\nclick -> place life\nscroll -> size\nspace -> run\nw/s -> higher/lower \n             the speed",(370,140),22)
helist = func.paragraph(hetext,2)
addnew = func.Font(">  +   ",(100,430),22,textcapsmall)
paint = func.Font("draw",(365,220),22,textcapsmall)
select = func.Font("select",(355,170),22,textcapsmall)
selecttext = func.Font("- select an area to make module -",(150,250),22)

toollist =[introduction,helptext,module,clearup]
fontlist = [speed_text,state,welcome]
mod =None
moduleseq =[]
modulefont ={}
moduledic ={}
modulepic = {">  plane":pygame.image.load("pic\\plane.PNG").convert(),">  flower":pygame.image.load("pic\\flower.PNG")}


button = [introduction,helptext,module,clearup,addnew,paint,select]

ucheck=pygame.Rect(0,0,800,100)
dcheck=pygame.Rect(0,500,800,100)
rcheck=pygame.Rect(700,0,100,600)
lcheck = pygame.Rect(0,0,100,600)

size=1
move=[0,0]
mouse_press = False
moving = False
mouse=[400,300]
selemouse = []
wid = 10
capacity = 500

test_wait=[]
change_wait = []
neighbor=[2,3,3]
count = 0
alcount = 0
speed=4.0

data =[]

#k = designated nuber's life state
k=0
tx,ty=0,0
sx,sy =0,0
move_delx,move_dely = 0,0
modulerec = 0
pressbu = 0
# stop = life working; done = all
rot = 0
stop = True
done = False
#圖往左，上移move+
item=[[0 for i in range(capacity)] for j in range(capacity)]

with open("modules.txt","rb") as m:
    while 1:
        try:
            data = pickle.load(m)
            k=func.Font(">  "+data.name,(0,0),22,textcapsmall)
            if k.content not in moduleseq:
                moduleseq.append(k.content)
                modulefont[k.content] = k
                moduledic[k.content] = data
        except:
            break


while not done:
    alcount+=1

    screen.blit(background,(0,0))

    #show
    tx,ty = func.show(window,move,size,wid)[2],func.show(window,move,size,wid)[3]
    sx,sy = func.show(window,move,size,wid)[0],func.show(window,move,size,wid)[1]
    move_delx,move_dely = move[0]%(wid*size), move[1]%(wid*size)
    for v in range(ty):
        for h in range(tx):
            if item[sy+v][sx+h]:
                func.addsurround([sy+v,sx+h],capacity,test_wait)
                pygame.draw.rect(screen,green,pygame.Rect(h*wid*size-move_delx,v*wid*size-move_dely,wid*size,wid*size))

    #state text
    if stop:
        k="pause"
    else:
        k = "living..."
    state.textup(k,30)
    #speed text
    k=str(speed)
    speed_text.textup(k+"/s",30)
    for texts in fontlist:
        screen.blit(texts.text,(texts.x,texts.y))
        
    #speed control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        if speed >0.5 and alcount%2==0:
            speed -=0.5
    if keys[pygame.K_w]:
        if speed <15 and alcount%2==0:
            speed +=0.5

    #arrows if touch show
    if not toolbu.button:
        mouse=pygame.mouse.get_pos()
        func.collid(screen,ucheck,mouse,up)
        func.collid(screen,dcheck,mouse,down)
        func.collid(screen,rcheck,mouse,right)
        func.collid(screen,lcheck,mouse,left)
    
    #move
    if mouse_press:
        if toollabel.button == 0 and toolbu.button == 0:
            mouse=list(pygame.mouse.get_pos())
            if mouse[0]>700 or mouse[0] <100 or mouse[1] >500 or mouse[1] <100:
                if mouse[0]>700 and move[0]+ (int(mouse[0]-700))*4/10< (capacity*wid*size-window[0]):
                    right.horcount = func.anicircle(right.horcount,0,10,1)
                    move[0]+=(int(mouse[0]-700))*4/10
                else:
                    right.horcount=0
                if mouse[0] <100 and move[0] -(int(100-mouse[0]))*4/10>0:
                    left.horcount = func.anicircle(left.horcount,0,-10,-1)
                    move[0]-=(int(100-mouse[0]))*4/10
                else:
                    left.horcount=0
                if mouse[1] >500 and move[1]+ (int(mouse[1]-500))*4/10< (capacity*wid*size-window[1]):
                    down.vercount = func.anicircle(down.vercount,0,10,1)
                    move[1]+=(int(mouse[1]-500))*4/10
                else:
                    down.vercount=0
                if mouse[1] <100 and move[1]-(int(100-mouse[1]))*4/10>0:
                    up.vercount = func.anicircle(up.vercount,0,-10,-1)
                    move[1]-=(int(100-mouse[1]))*4/10
                else:
                    up.vercount=0 

    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = not done

        if event.type == pygame.KEYDOWN:
            if func.lisjudge([modulefont[i].button for i in moduleseq],0) or toolbu.button ==0:
                if event.key == pygame.K_SPACE:
                    stop = not stop

        if event.type == pygame.MOUSEBUTTONDOWN:
            try:
                fontlist.remove(welcome)
            except:
                pass
            mouse=list(pygame.mouse.get_pos())
            if event.button ==1:
                mouse_press = 1
            
            if func.lisjudge([modulefont[i].button for i in moduleseq],0) and not addnew.button:
                #toolbutton
                if pygame.Rect.collidepoint(toolbu.rec,mouse):
                    if toolbu.button ==0:
                        toolbu.button = 1
                        rot = 1
                    else:
                        toolbu.button = 0
                #scroll size
                if toolbu.button ==0:
                    if event.button ==4:
                        if size<4 and move[0]+ (move[0]+mouse[0])*((size+0.4)/size-1)< (capacity*wid*size -window[0])and move[1]+(move[1]+mouse[1])*((size+0.4)/size-1) < (capacity*wid*size-window[1]):
                            move[0]+=(move[0]+mouse[0])*((size+0.4)/size-1)
                            move[1]+=(move[1]+mouse[1])*((size+0.4)/size-1)
                            size+=0.4
                    elif event.button ==5:
                        if size >1 and move[0]-(move[0]+mouse[0])*(1-(size-0.4)/size)>0 and move[1]-(move[1]+mouse[1])*(1-(size-0.4)/size)>0:
                            move[0]-=(move[0]+mouse[0])*(1-(size-0.4)/size)
                            move[1]-=(move[1]+mouse[1])*(1-(size-0.4)/size)
                            size-=0.4
                    else:
                        #place life
                        if stop and not (mouse[0]>700 or mouse[0] <100 or mouse[1] >500 or mouse[1] <100):
                            k = item[func.click(mouse,move,size,wid)[1]][func.click(mouse,move,size,wid)[0]]
                            item[func.click(mouse,move,size,wid)[1]][func.click(mouse,move,size,wid)[0]] = not k
                            func.addsurround(func.click(mouse,move,size,wid),capacity,test_wait)
                else:
                    #button (1)
                    if pygame.Rect.collidepoint(clearup.rec,mouse):
                        clearup.press = 1
                        item = [[0 for i in range(capacity)]for j in range(capacity)]
                        test_wait.clear()
                        change_wait.clear()
                    for tools in toollist:
                        if func.buchange(tools,mouse):
                            k = tools
                            tools.press = 1
                            for tool in toollist:
                                if tool!=k:
                                    tool.button = 0
                            break
                    if pygame.Rect.collidepoint(addnew.rec,mouse):
                        addnew.button = not addnew.button
                    for thing in moduleseq:
                        if pygame.Rect.collidepoint(modulefont[thing].rec,mouse):
                            modulefont[thing].button = not modulefont[thing].button
                            mod = thing
            else:
                #module place
                if not func.lisjudge([modulefont[i].button for i in moduleseq],0):
                    if event.button ==1 or event.button==3:
                        if event.button==3:
                            for thing in moduleseq:
                                modulefont[thing].button =0
                        else:
                            if event.button ==1:
                                mouse_press = True
                                if not (mouse[0]>700 or mouse[0] <100 or mouse[1] >500 or mouse[1] <100):
                                    if  modulerec:
                                        k=func.click(mouse,move,size,wid)
                                        for i in range(moduledic[mod].hw[1]):
                                            for j in range(moduledic[mod].hw[0]):
                                                item[k[1]+i][k[0]+j] = moduledic[mod].life[i][j]
                                for thing in moduleseq:
                                    modulefont[thing].button =0
                                moduleseq.clear()
                #add
                elif addnew.button:
                    if event.button ==3:
                        addnew.button = 0
                        paint.button = 0
                        select.button = 0
                    if not (paint.button or select.button):
                        if event.button  ==1:
                            if func.buchange(select,mouse):
                                select.press = 1
                                selecttext.fade = 1
                            elif func.buchange(paint,mouse):
                                paint.press = 1
                    
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_press = False
            for bu in button:
                bu.press = 0
            #arrow move
            for pic in piclist:
                pic.vercount = 0
                pic.horcount = 0
    #button cap
    for bu in button:
        if bu.press:
            bu.vercount = 5
            bu.point.vercount =5
        else:
            bu.vercount = 0
            bu.point.vercount = 0

    #tool control
    if toolbu.button !=0:
        mouse=pygame.mouse.get_pos()
        if func.lisjudge([modulefont[i].button for i in moduleseq],0) and not addnew.button:
            stop = True
            #animation unfold
            if rot == 1:
                if toolbu.rota <350:
                    toolbu.rota+=15
                else:
                    toolbu.rota =0
                    rot = 0
            if toollabel.horcount<-30:
                toollabel.horcount+=20
            else:
                toollabel.button = 1
            screen.blit(toolcap.image,(toolcap.x,toolcap.y))
            screen.blit(toollabel.image,(toollabel.x+toollabel.horcount,0))
            screen.blit(smallcap.image,(smallcap.x,smallcap.y))
            #click button
            for tools in toollist:
                if pygame.Rect.collidepoint(tools.rec,mouse) and toollabel.button ==1:
                    screen.blit(tools.point.image,(tools.point.x,tools.y-10+tools.point.vercount))
                screen.blit(tools.text,(tools.x+toollabel.horcount,tools.y+tools.vercount))
            #textbutton
            if introduction.button ==1:
                label.animago(15)
                screen.blit(label.image,(label.x,label.y))
                for fonts in introlist:
                    screen.blit(fonts.text,(fonts.x,fonts.y))
            elif helptext.button ==1:
                label.animago(15)
                screen.blit(label.image,(label.x,label.y))
                for fonts in helist:
                    screen.blit(fonts.text,(fonts.x,fonts.y))
            else:
                label.count=1
                label.customcount = 0
            #module    
            if module.button ==1:
                with open("modules.txt","rb") as m:
                    while 1:
                        try:
                            data = pickle.load(m)
                            k=func.Font(">  "+data.name,(0,0),22,textcapsmall)
                            if k.content not in moduleseq:
                                moduleseq.append(k.content)
                                modulefont[k.content] = k
                                moduledic[k.content] = data
                        except:
                            break
                for thing in moduleseq:
                    if pygame.Rect.collidepoint(modulefont[thing].rec,mouse):
                        try:
                            screen.blit(modulepic[thing],(250,280+moduleseq.index(thing)*45))
                            screen.blit(modulefont[thing].point.image,(95,290+moduleseq.index(thing)*45))
                        except:
                            pass
                    modulefont[thing].rec.x,modulefont[thing].rec.y = 100,290+moduleseq.index(thing)*45
                    screen.blit(modulefont[thing].text,(100,290+moduleseq.index(thing)*45+modulefont[thing].vercount))
                if pygame.Rect.collidepoint(addnew.rec,mouse):
                    screen.blit(addnew.point.image,(95,addnew.y))
                screen.blit(addnew.text,(addnew.x,addnew.y))
        else:
            
            if func.lisjudge([modulefont[i].button for i in moduleseq],0) or addnew.button:
                screen.blit(toolcap.image,(toolcap.x,toolcap.y))
                
            if addnew.button and not(paint.button or select.button):
                screen.blit(addlabel.image,(addlabel.x,addlabel.y))
                if pygame.Rect.collidepoint(paint.rec,mouse):
                    screen.blit(paint.point.image,(select.x-23,paint.y))
                if pygame.Rect.collidepoint(select.rec,mouse):
                    screen.blit(select.point.image,(select.x-23,select.y))
                screen.blit(paint.text,(paint.x,paint.y))
                screen.blit(select.text,(select.x,select.y))
            elif select.button:
                if selecttext.fade == 1:
                    selecttext.fadeout(2,30)
                    screen.blit(selecttext.text,(selecttext.x,selecttext.y))
    else:
        for tools in toollist:
            tools.button =0
        if toollabel.horcount>-490:
            toollabel.horcount-=20 
            screen.blit(toollabel.image,(toollabel.x+toollabel.horcount,0))
            screen.blit(smallcap.image,(smallcap.x,smallcap.y))
            for tools in toollist:
                screen.blit(tools.text,(tools.x+toollabel.horcount,tools.y+tools.vercount))
        else:
            toollabel.button = 0

    screen.blit(pygame.transform.rotate(toolbu.image,toolbu.rota),(toolbu.x,toolbu.y))

    #using module module.button 
    if func.lisjudge([modulefont[i].button for i in moduleseq],0)==0 or select.button:
        mouse = pygame.mouse.get_pos()
        if func.collid(screen,ucheck,mouse,up,2) or func.collid(screen,dcheck,mouse,down,2) or func.collid(screen,rcheck,mouse,right,2) or func.collid(screen,lcheck,mouse,left,2):
            modulerec = 0
            #move
            if func.collid(screen,ucheck,mouse,up,2):
                if move[1]-(int(100-mouse[1]))*4/10>0:
                    up.vercount = func.anicircle(up.vercount,0,-10,-1)
                    move[1]-=(int(100-mouse[1]))*4/10
            else:
                up.vercount=0 
            if func.collid(screen,dcheck,mouse,down,2):
                if move[1]+ (int(mouse[1]-500))*4/10< (capacity*wid*size-window[1]):
                    down.vercount = func.anicircle(down.vercount,0,10,1)
                    move[1]+=(int(mouse[1]-500))*4/10
            else:
                down.vercount=0
            if func.collid(screen,rcheck,mouse,right,2):
                if move[0]+ (int(mouse[0]-700))*4/10< (capacity*wid*size-window[0]):
                    right.horcount = func.anicircle(right.horcount,0,10,1)
                    move[0]+=(int(mouse[0]-700))*4/10
            else:
                right.horcount=0
            if func.collid(screen,lcheck,mouse,left,2):
                if move[0] -(int(100-mouse[0]))*4/10>0:
                    left.horcount = func.anicircle(left.horcount,0,-10,-1)
                    move[0]-=(int(100-mouse[0]))*4/10
            else:
                left.horcount=0
        else:
            if func.lisjudge([modulefont[i].button for i in moduleseq],0)==0:
                modulerec = 1
                k=func.click(mouse,move,size,wid)
                for i in range(moduledic[mod].hw[1]):
                    for j in range(moduledic[mod].hw[0]):
                        if item[k[1]+i][k[0]+j]:
                            modulerec = 0
                            break
                    if  modulerec == 0:
                        break
                if modulerec ==1:
                    reccolor = green
                else:
                    reccolor  =pygame.color.Color("#ff2222")
                k= [k[0]-sx,k[1]-sy]
                try:
                    pygame.draw.rect(screen,reccolor,pygame.Rect(k[0]*wid*size-move_delx,k[1]*wid*size-move_dely,moduledic[mod].hw[0]*wid*size,moduledic[mod].hw[1]*wid*size))
                except:
                    modulerec = 0
            else:
                if mouse_press:
                    selemouse = pygame.mouse.get_pos()

    #determine lives's state
    if not stop and toollabel.button ==0:
        count +=1
        if count%(30/speed)<1:
            for tests in test_wait:
                if func.judge(tests, item, neighbor) is not None:
                    change_wait.append(func.judge(tests,item,neighbor))
                    func.addsurround(tests,capacity,test_wait)
            for change in change_wait:
                try:
                    item[change[0]][change[1]]=not item[change[0]][change[1]]
                except Exception == IndexError:
                    pass
            change_wait=[]
    
    pygame.display.update()
                             
    clock.tick(30)
pygame.quit()
