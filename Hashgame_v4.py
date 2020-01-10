import pygame
import random
import os

#DIsplay Size
disp_width = 1280
disp_height = 720
#Initialize mixer for sounds
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

#Paths to images
game_dir = os.path.dirname(__file__)
img_folder = os.path.join(game_dir,'Images')
sound_folder = os.path.join(game_dir,'Sounds')
loading_folder = os.path.join(game_dir,'Loading')
Movie_folder = os.path.join(game_dir,'Movie')
#initialize sound objects

click_sound = pygame.mixer.Sound(os.path.join(sound_folder,'Click1.wav'))
pygame.mixer.music.load(os.path.join(sound_folder,'Loop1.wav'))
####################################COLORS############################################
white=(255,255,255)
offwhite=(220,220,220)
red=(255,0,0)
black=(0,0,0)
green=(0,200,0)
aquamarine=(127,255,212)
######################################################################################
gameDisplay = pygame.display.set_mode((disp_width,disp_height))
pygame.display.set_caption('Hashgame')
clock = pygame.time.Clock()
ROOTS=8
##################################fonts#################################################
font1=pygame.font.Font(None,30)
font2=pygame.font.Font('segoeuil.ttf',24)
font=pygame.font.Font('segoeuil.ttf',36)
Right_font_Large=pygame.font.Font(None,56)
Rd_text_large=pygame.font.Font(None,90)
Intro_font=pygame.font.Font(None,86)

########################################################################################
_Time_per_move=20 #In seconds
_Start_time=0
_end_time=0
_Start_time2=0
_end_time2=0
_Time_per_move2=30

Sound_flag=True #Toggle sound ON/OFF

#Draw distance of nodes from each other
Horizontal_diff = 130
HD = Horizontal_diff
Vertical_Diff = 100
list_Default=[]
g2_list=[]
list_of_8=[[],[],[],[],[],[],[],[]]
game2_list=[]
###########################################################################################################
T_list=[[30,20],[30+HD,20],[30+HD*2,20],[30+HD*3,20],[30+HD*4,20],[30+HD*5,20],[30+HD*6,20],[30+HD*7,20]]

#Open hashing
class Hash_Table:
	def __init__(self,Roots):
		self.Roots=Roots

	def Get_Val(self,R_num):
		try:
			R = int(R_num)
		except:
			R = len(R_num)
		ret = str(R % self.Roots)
		return ret

#Quadratic probing Hash function
class Q_probing:
	def __init__(self,Roots):
		self.checks=0
		self.Roots=Roots
		self.index=0
		self.pers_index=0
		self.I_lst=[]

	def Retry(self,g2_list):
		self.flag=0
		self.index = (self.pers_index + (self.checks*self.checks))%self.Roots
		print(self.index)
		if self.checks <= self.Roots:
			pass
		else:
			return 0
		if g2_list[self.index]==0:
			self.I_lst.append(self.index)
			self.flag=1
			return 0
		else:
			self.I_lst.append(self.index)
			self.checks+=1
			self.Retry(g2_list)

	def Get_Val(self,R_num,g2_list):
		self.checks=0
		self.I_lst=[]
		try:
			R = int(R_num)
		except:
			R = len(R_num)
		self.index = (R % self.Roots)
		self.pers_index=self.index
		if g2_list[self.index]==0:
			self.I_lst.append(self.index)
			return self.I_lst
		else:
			self.I_lst.append(self.index)
			self.checks+=1
			self.Retry(g2_list)
			if self.flag!=0:
				return self.I_lst
			else:
				return None


#Draw persistent nodes (Top row)
class Default_nodes:
	def __init__(self,Pos,text):
		self.font1=pygame.font.Font(None,36)
		self.pos=Pos
		self.text=text

	def Draw_rect_node(self):
		x=self.pos[0]
		y=self.pos[1]
		pygame.draw.rect(gameDisplay,white,(x,y,70,50),4)

	def Nodetext_node(self,text,tup):
		N=[tup[0],tup[1]]
		if len(text) > 2:
			N[0] -= 16
		elif len(text) == 2:
			N[0]-=13
		elif len(text) > 1:
			N[0]-=7
		if text!="None":
			text1=font.render(text,True,white)
			gameDisplay.blit(text1,N)
		else:
			text1=font2.render(text,True,white)
			gameDisplay.blit(text1,N)

	def Create(self):
		k=[self.pos[0]+24,self.pos[1]]
		self.Draw_rect_node()
		self.Nodetext_node(self.text,k)

#Draw Dynamic nodes
class Nodes(Default_nodes):
	def __init__(self,Pos,text,level):
		Default_nodes.__init__(self,Pos,text)
		self.abs_pos=[0,0]
		self.level=level

	def Draw_rect_node1(self,color):
		x=self.pos[0]
		y=self.pos[1]+(self.level*Vertical_Diff)
		self.abs_pos[0]=x
		self.abs_pos[1]=y
		pygame.draw.rect(gameDisplay,color,(x,y,70,50),4)

	def Create_new(self):
		k=(self.pos[0]+25,self.pos[1]+(self.level*Vertical_Diff))
		self.Draw_rect_node1(white)
		self.Nodetext_node(self.text,k)

	def Create_new2(self,color):
		k=(self.pos[0]+25,self.pos[1]+(self.level*Vertical_Diff))
		self.Draw_rect_node1(color)
		self.Nodetext_node(self.text,k)

####################################################################################
for x in range(8):
	M=Default_nodes(T_list[x],str(x))
	list_Default.append(M)

def Nodetext(text,centre_pos,size,color):
		f1=pygame.font.Font('segoeuil.ttf',size)
		Text = f1.render(text,True,color)
		Rect = Text.get_rect()
		Rect.center = (centre_pos)
		gameDisplay.blit(Text,Rect)
		pygame.display.update()

def Draw_rect(pos,width,height,color,th):
		x=pos[0]
		y=pos[1]
		pygame.draw.rect(gameDisplay,color,(x,y,width,height),th)
		pygame.display.update()

############################################NEW Windows####################################################################################
def Loading():
	i=1
	gameDisplay.fill(black)
	clock1=pygame.time.Clock()
	for i in range(1,90):
		gameDisplay.fill(black)
		Z = pygame.image.load(os.path.join(loading_folder,f'Pictures{i}.jpg'))
		gameDisplay.blit(Z,(disp_width/2-250,disp_height/2-140))
		pygame.display.update()

def Game_over(score):
	pygame.mixer.music.stop()
	global list_of_8
	I = pygame.image.load(os.path.join(img_folder,'gameover.png'))
	gameDisplay.blit(I,(0,0))
	Score_TT=Rd_text_large.render(str(score),True,white)
	gameDisplay.blit(Score_TT,(disp_width*0.55,disp_height*0.59+2))
	Start_pos=Start_pos=(disp_width*0.37,disp_height*0.7)
	pygame.display.update()
	GO = False
	while not GO:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				GO = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse2=pygame.mouse.get_pos()
				if(Start_pos[0]+320 > mouse2[0] > Start_pos[0]) and (Start_pos[1]+120 > mouse2[1] > Start_pos[1]):
					list_of_8=[[],[],[],[],[],[],[],[]]
					R=Random_num_gen()
					Intro()

def How_to_play():
	I = pygame.image.load(os.path.join(img_folder,'howtoplay.png'))
	gameDisplay.blit(I,(0,0))
	Start_pos=(disp_width*0.02,disp_height*0.07)
	pygame.display.update()
	GO = False
	while not GO:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				GO = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse1=pygame.mouse.get_pos()
				if (Start_pos[0]+250 > mouse1[0] > Start_pos[0]) and (Start_pos[1]+70 > mouse1[1] > Start_pos[1]):
					GO = True
					Info()

def Info():
	print("Success")
	I = pygame.image.load(os.path.join(img_folder,'intro1.png'))
	gameDisplay.blit(I,(0,0))
	Start_pos=(disp_width*0.02,disp_height*0.07-10)
	Next_pos=(disp_width*0.89,disp_height*0.83)
	pygame.display.update()
	GO = False
	while not GO:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				GO = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse1=pygame.mouse.get_pos()
				if (Start_pos[0]+250 > mouse1[0] > Start_pos[0]) and (Start_pos[1]+70 > mouse1[1] > Start_pos[1]):
					GO = True
					Intro()
				if (Next_pos[0]+68 > mouse1[0] > Next_pos[0]) and (Next_pos[1]+68 > mouse1[1] > Next_pos[1]):
					GO = True
					How_to_play()

def Intro():
	global Sound_flag
	GO=False
	gameDisplay.fill(offwhite)
	I = pygame.image.load(os.path.join(img_folder,'Start.png'))
	gameDisplay.blit(I,(0,0))
	Info_pos=(disp_width*0.42,disp_height*0.65)
	Start_pos=(disp_width*0.42,disp_height*0.52)
	Exit_pos=(disp_width*0.42,disp_height*0.78)
	Mute_pos=(disp_width*0.85,disp_height*0.78)
	unMute_pos=(disp_width*0.85,disp_height*0.65)

	pygame.display.update()
	while not GO:
		gameDisplay.blit(I,(0,0))
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				GO = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse1=pygame.mouse.get_pos()
				if (Exit_pos[0]+250 > mouse1[0] > Exit_pos[0]) and (Exit_pos[1]+70 > mouse1[1] > Exit_pos[1]):
					GO = True
					pygame.quit()
					quit()
				if (unMute_pos[0]+80 > mouse1[0] > unMute_pos[0]) and (unMute_pos[1]+80 > mouse1[1] > unMute_pos[1]):
					pygame.draw.circle(gameDisplay,aquamarine,(int(unMute_pos[0]+40),int(unMute_pos[1]+40)),40,40)
					pygame.display.update()
					Sound_flag = True
				if (Mute_pos[0]+80 > mouse1[0] > Mute_pos[0]) and (Mute_pos[1]+80 > mouse1[1] > Mute_pos[1]):
					pygame.draw.circle(gameDisplay,aquamarine,(int(Mute_pos[0]+40),int(Mute_pos[1]+40)),40,40)
					pygame.display.update()
					Sound_flag = False
				if (Info_pos[0]+250 > mouse1[0] > Info_pos[0]) and (Info_pos[1]+70 > mouse1[1] > Info_pos[1]):
					GO = True
					Info()
				if (Start_pos[0]+250 > mouse1[0] > Exit_pos[0]) and (Start_pos[1]+70 > mouse1[1] > Start_pos[1]):
					GO = True
					Level_select()

def Level_select():
	GO = False
	gameDisplay.fill(white)
	L1_pos=(disp_width/2-125,disp_height*0.35+5)
	L2_pos=(disp_width/2-125,disp_height*0.50+5)
	Draw_rect(L1_pos,250,70,black,3)
	Draw_rect(L2_pos,250,70,black,3)
	Nodetext("LEVEL SELECT",(disp_width/2,disp_height*0.1),80,black)
	Nodetext("LEVEL : 1",(disp_width/2,disp_height*0.4),56,black)
	Nodetext("LEVEL : 2",(disp_width/2+4,disp_height*0.55),56,black)

	while not GO:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				GO = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse1=pygame.mouse.get_pos()
				if (L1_pos[0]+250 > mouse1[0] > L1_pos[0]) and (L1_pos[1]+70 > mouse1[1] > L1_pos[1]):
					Loading()
					Random_num_disp(Random_num)
					Gameloop1(Random_num)
				if (L2_pos[0]+250 > mouse1[0] > L2_pos[0]) and (L2_pos[1]+70 > mouse1[1] > L2_pos[1]):
					Gameloop2()
					pygame.quit()
					quit()

###############################################################################################################################
def Display1(Score,lives,time):
	global list_of_8
	Heart = pygame.image.load(os.path.join(img_folder,'heart1.png'))

	pygame.draw.line(gameDisplay,aquamarine,(15,90),(1030,90),5)
	pygame.draw.line(gameDisplay,aquamarine,(1050,10),(1050,700),5)

	Time_text=Right_font_Large.render("Time",True,white)
	gameDisplay.blit(Time_text,(disp_width-180,disp_height-650))

	Hash1_text=font1.render("Random no%8 = Index",True,white)
	gameDisplay.blit(Hash1_text,(disp_width-225,disp_height-530))

	Score_text=Right_font_Large.render("Score",True,white)
	gameDisplay.blit(Score_text,(disp_width-180,disp_height-150))

	Lives_text=Right_font_Large.render("Lives",True,white)
	gameDisplay.blit(Lives_text,(disp_width-180,disp_height-300))

	for x in range(lives):
		gameDisplay.blit(Heart,(disp_width-230+65*x,disp_height-250))

	Score_TT = Right_font_Large.render(str(Score),True,white)
	gameDisplay.blit(Score_TT,(disp_width-160,disp_height-100))

	Time_TT = Right_font_Large.render(str(time),True,white)
	gameDisplay.blit(Time_TT,((disp_width-155,disp_height-600)))

	for z in list_Default:
		z.Create()
	for x in list_of_8:
		for y in x:
			y.Create_new()

def Display2(Score,lives,time,lst=[]):
	pygame.draw.line(gameDisplay,aquamarine,(1050,10),(1050,700),5)
	Heart = pygame.image.load(os.path.join(img_folder,'heart1.png'))

	Time_text=Right_font_Large.render("Time",True,white)
	gameDisplay.blit(Time_text,(disp_width-180,disp_height-650))

	Hash1_text=font1.render("In case of collision",True,white)
	gameDisplay.blit(Hash1_text,(disp_width-200,disp_height-530))
	Hash_text=font1.render("index=(index + i*i) i<50",True,white)
	gameDisplay.blit(Hash_text,(disp_width-225,disp_height-500))

	Score_text=Right_font_Large.render("Score",True,white)
	gameDisplay.blit(Score_text,(disp_width-180,disp_height-150))

	Lives_text=Right_font_Large.render("Lives",True,white)
	gameDisplay.blit(Lives_text,(disp_width-180,disp_height-300))

	for x in range(lives):
		gameDisplay.blit(Heart,(disp_width-230+65*x,disp_height-250))

	Score_TT = Right_font_Large.render(str(Score),True,white)
	gameDisplay.blit(Score_TT,(disp_width-160,disp_height-100))

	Time_TT = Right_font_Large.render(str(time),True,white)
	gameDisplay.blit(Time_TT,((disp_width-155,disp_height-600)))
	for x in game2_list:
		if len(lst)!=0:
			if x in lst:

				x.Create_new2(red)
			else:
				x.Create_new()
		else:
			x.Create_new()

def Create2():
	global game2_list
	g2_lst=[]
	i=0
	for x in range(7):
		for y in range(7):
			g2_lst.append(0)
			M = Nodes(T_list[x],f"{i}",y)
			game2_list.append(M)
			i+=1
	M = Nodes((930,20),"49",0)
	game2_list.append(M)
	M = Nodes((930,20),"None",1)
	game2_list.append(M)
	return g2_lst

#####################################################################################
def Random_num_gen():
	global _Start_time
	global _Start_time2
	while True:
		Random_num=random.randrange(999)
		if Random_num%50==49:
			pass
		else:
			break
	_Start_time=pygame.time.get_ticks()
	_Start_time2=pygame.time.get_ticks()
	return Random_num

def Random_num_disp(Random_num1):
	R_num = Rd_text_large.render(str(Random_num1),True,white)
	gameDisplay.blit(R_num,(disp_width-180,disp_height-450))
	pygame.display.update()

def Difficulty_inc(Score):
	global _Time_per_move
	if Score==6 or Score==15:
		_Time_per_move-=5
	if Score==25 or Score==35:
		_Time_per_move-=2
	print(_Time_per_move)

def scr_rst():
	global list_of_8
	for x in range(8):
		if len(list_of_8[x])>6:
			list_of_8[x].clear()

############################Gameloops##########################################################
def Gameloop1(Random_num):
	Random_num=Random_num_gen()
	global _Start_time
	global _end_time
	global _Time_per_move
	global list_of_8
	global Sound_flag
	_Time_per_move = 21
	if Sound_flag:
		pygame.mixer.music.play(-1)
	Difficulty = 0
	rem_time=0
	LIVES = 3
	H = Hash_Table(ROOTS)
	GameOver = False
	Score = 0
	i=1
	HN=H.Get_Val(int(Random_num))
	while LIVES > 0:
		I=pygame.image.load(os.path.join(Movie_folder,f'Pictures{i}.jpg'))
		gameDisplay.blit(I,(0,0))
		R_num = Rd_text_large.render(str(Random_num),True,white)
		gameDisplay.blit(R_num,(disp_width-180,disp_height-450))
		#TIME
		elapsed_time = pygame.time.get_ticks() - _Start_time
		rem_time = _Time_per_move - (elapsed_time/1000)
		#REFRESH DISPLAY
		scr_rst()#If index is full, reset.
		Display1(Score,LIVES,int(rem_time))
		#HASH FUNCTION

		if i<1150:
			i+=1
		else:
			i=188

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				LIVES = 0

			if event.type == pygame.MOUSEBUTTONDOWN:
				#pygame.mixer.music.pause()
				if Sound_flag:
					click_sound.play()
				mouse=pygame.mouse.get_pos()
				for x in list_Default:
					pos1=x.pos

					if ((pos1[0]+70 > mouse[0] > pos1[0]) and (pos1[1]+50 > mouse[1] > pos1[1])):
						if x.text == str(HN):
							N=Nodes(pos1,str(Random_num),len(list_of_8[list_Default.index(x)])+1)
							list_of_8[list_Default.index(x)].append(N)
							Random_num=Random_num_gen()
							Score+=1
							HN=H.Get_Val(int(Random_num))
							if Score>5:
								Difficulty_inc(Score)
							break;
						else:
							LIVES -= 1
							Random_num=Random_num_gen()
							HN=H.Get_Val(int(Random_num))
		if rem_time <= 0:
			LIVES-=1
			Random_num=Random_num_gen()
			HN=H.Get_Val(int(Random_num))
		if LIVES == 0:
			Game_over(Score)
		pygame.display.update()
		clock.tick(120)

def Gameloop2():
	Random_num=1
	global _Start_time2
	global _end_time2
	global _Time_per_move2
	global Sound_flag
	global game2_list
	BG = pygame.image.load(os.path.join(img_folder,"BG.png"))
	game2_list=[]
	pass_lst=[]
	_Time_per_move2 = 30
	H = Q_probing(50) #Creating object for quadratic probing
	Score = 0
	Lives = 3
	#gameDisplay.fill(black)
	gameDisplay.blit(BG,(0,0))
	rem_time2 = 100
	g2_list = Create2()
	Random_num=Random_num_gen()
	HN=H.Get_Val(int(Random_num),g2_list)
	print(Random_num,HN)
	if Sound_flag:
		pygame.mixer.music.play(-1)
	while Lives > 0:
		elapsed_time2 = pygame.time.get_ticks() - _Start_time2
		rem_time2 = _Time_per_move2 - (elapsed_time2/1000)
		gameDisplay.blit(BG,(0,0))
		Display2(Score,Lives,int(rem_time2),pass_lst)
		R_num = Rd_text_large.render(str(Random_num),True,white)
		gameDisplay.blit(R_num,(disp_width-180,disp_height-450))
		if HN==None:
			HN=[None]
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Lives = 0

			if event.type == pygame.MOUSEBUTTONDOWN:
				if Sound_flag:
					click_sound.play()
				mouse=pygame.mouse.get_pos()
				for x in game2_list:
					pos2=x.abs_pos

					if ((pos2[0]+70 > mouse[0] > pos2[0]) and (pos2[1]+50 > mouse[1] > pos2[1])):
						if x.text == str(HN[-1]):
							g2_list[HN[-1]] = 1
							#x.text=str(Random_num)
							Random_num = Random_num_gen() #Generate random number
							Random_num_disp(Random_num) #Display random number
							HN=H.Get_Val(int(Random_num),g2_list)
							pass_lst.append(x) #Pass the object to highlight that rect
							Score += 1
						else:
							print(HN,"Index")
							Lives -= 1
							Random_num=Random_num_gen()
							Random_num_disp(Random_num)
							HN=H.Get_Val(int(Random_num),g2_list)
		if rem_time2 <= 0:
			Lives -= 1
			Random_num=Random_num_gen()
		if Lives == 0:
			Game_over(Score)
		pygame.display.update()
		clock.tick(120)


############################################################################################################
Random_num=1
if __name__ == '__main__':
	Intro()
	pygame.quit()
	quit()
