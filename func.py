import pygame
import pickle
#the range(number) you have to show,requires window size(list), how long the thing move, scale change(default=1),the basic width of the thing 
def show(table,moved,sized,wide):
    x1,y1 = moved[0]//(sized*wide),moved[1]//(sized*wide)
    x2,y2 = x1+(table[0]//(sized*wide))+1,y1+(table[1]//(sized*wide))+1
    x1,y1,x2,y2 = int(x1), int(y1),int(x2),int(y2)
    return list([x1,y1,x2-x1,y2-y1])

#to point out which object(number) you click, requires mouse's position, move, scale zoom, basic width of the thing
def click(pos,moved,sized,wide):
    no1,no2 = (pos[0] + moved[0])//(sized*wide),(pos[1] + moved[1])//(sized*wide)
    return list([int(no1),int(no2)])
#add all(if not in)
def addsurround(what,capci,to):
    addin(what,capci,to)
    addin(what,capci,to,1,0)
    addin(what,capci,to,-1,0)
    addin(what,capci,to,0,1)
    addin(what,capci,to,0,-1)
    addin(what,capci,to,1,1)
    addin(what,capci,to,1,-1)
    addin(what,capci,to,-1,1)
    addin(what,capci,to,-1,-1)
#if not in then add it
def addin(lis,cap,testwait,addy=0,addx=0):
    if cap > lis[0]+addy>-1 and cap > lis[1]+addx>-1:
        if [lis[0]+addy,lis[1]+addx] not in testwait:
            testwait.append([lis[0]+addy,lis[1]+addx])
#determive surrounding state, return T or F, require count variable
def judge(testing,fro,parameter):
    va=0
    try:
        va+=var_count(testing,fro,1,0)
        va+=var_count(testing,fro,-1,0)
        va+=var_count(testing,fro,0,1)
        va+=var_count(testing,fro,0,-1)
        va+=var_count(testing,fro,1,1)
        va+=var_count(testing,fro,1,-1)
        va+=var_count(testing,fro,-1,1)
        va+=var_count(testing,fro,-1,-1)
        if fro[testing[0]][testing[1]]:
            if va>parameter[1] or va<parameter[0]:
                return testing
        else:
            if va == parameter[2]:
                return testing
    except:
        pass
    finally:
        va=0

def var_count(tes,fr,yy=0,xx=0):
    try:
        if fr[tes[0]+yy][tes[1]+xx]:
            return  int(1)
        else:
            return int(0)
    except:
        return int(0)

#surface rect collide for arrow to move
def collid(where,recs,what,appear,kind=0):
    if kind ==0:
        #if rec
        if pygame.Rect.collidepoint(recs,what):
            where.blit(appear.image,(appear.x+appear.horcount,appear.y+appear.vercount))
    if kind == 1:
        #class
        if pygame.Rect.collidepoint(recs.rec,what):
            where.blit(appear.image,(appear.x,recs.rec.y-10+appear.vercount))
    if kind ==2:
        #move
        if pygame.Rect.collidepoint(recs,what):
            where.blit(appear.image,(appear.x+appear.horcount,appear.y+appear.vercount))
            return True
            
#regularly change a thing in a circle(animation)
def anicircle(what,start,end,seq):
    if what == end:
        what =start
    else:
        what +=seq
    return what

#require class with rec and button(click collide)
def buchange(what,wit):
    if pygame.Rect.collidepoint(what.rec,wit):
        what.button = not what.button
        return True
#judge if all of the things in the list is True or False
def lisjudge(lis,val):
    for jud in lis:
        if jud == val:
            pass
        else:
            return False
    return True
#create a font list to form a parqgraph
def paragraph(fonted,hei,title = 0,large=0):
    cache = fonted.content.split("\n")
    count = 0
    mylist = []
    for word in cache:
        if title and count ==0:
            mylist.append(Font(word,(fonted.x,fonted.y+count*hei*fonted.size+large),fonted.size+large*hei))
        else:
            mylist.append(Font(word,(fonted.x,fonted.y+count*hei*fonted.size),fonted.size))     
        count+=1
    return mylist
#font
class Font:
    def __init__(self,text,loca,size,point = None):
        self.content =text
        font = pygame.font.SysFont("OCR A Extended",size)
        self.text = font.render(text,False,(255,255,255))
        self.colorr = (255,255,255)
        self.x,self.y = loca
        self.vercount =0
        self.button = 0
        self.press = 0
        self.point = point
        self.size = size
        self.fade =1
        self.rec = self.text.get_rect(topleft = (self.x,self.y))
    def textup(self,text,size):
        font = pygame.font.SysFont("OCR A Extended",size)
        self.text = font.render(text,False,(255,255,255))
    def coloring(self,size,colorr):
        font = pygame.font.SysFont("OCR A Extended",size)
        self.text = font.render(self.content,False,colorr)
        self.colorr = colorr
    def fadeout(self,long,tick):
        try:
            self.count+=1
        except:
            self.count = 0
        if self.colorr==(0,0,0):
            self.fade = 0
        else:
            self.coloring(self.size,(self.colorr[0]-(255/(long/tick))*self.count,self.colorr[1]-(255/(long/tick))*self.count,self.colorr[2]-(255/(long/tick))*self.count))
        
def modu():
    with open("modules.txt","wb") as m:
        pickle.dump(Module("flower",[3,3],[[0,1,0],[1,0,1],[0,1,0]]),m)
        pickle.dump(Module("plane",[3,3],[[0,0,1],[1,0,1],[0,1,1]]),m)
	
#transform surface and get rect
class Picture:
    def __init__(self,image,loca,rot,size):
        self.image = pygame.transform.rotate(image,rot)
        self.image = pygame.transform.scale(self.image,size)
        self.rota =0
        self.vercount =0
        self.horcount = 0
        self.x,self.y = loca
        self.rec = self.image.get_rect(topleft = (self.x,self.y))
        self.button = 0
        self.press = 0
    def animate(self,custom):
        self.count = 1
        self.custom=custom
        self.customcount = 0
        self.custom.append(self.image)
    def animago(self,spee):
        self.count +=1
        if self.count%spee==0:
            self.image = self.custom[self.customcount%len(self.custom)]
            self.customcount+=1
            
class Module:
    def __init__(self,name,hw,life):
        self.name = name
        self.hw = hw
        self.life = life
    
        


