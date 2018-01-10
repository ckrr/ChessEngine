import tkinter as tk
import math, sys, copy, time, linecache

RD=((1,0),(-1,0),(0,1),(0,-1))
BY=(-1,1)
BX=(-1,1)
ND=((2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1))
KD=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
PieceVal=(10,30,30,50,90,1000)
NotationChar=('','B','N','R','Q','K')
NotationCol=('a','b','c','d','e','f','g','h')
ReverseChar={'B':1,'N':2,'R':3,'Q':4,'K':5}
ReverseCol={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
TypeIndex=[0,0,0,0,0,0,0,0,3,2,1,4,5,1,2,3]
StateConst=10000000
Rfilename="Openings.txt"
Side=60

DarkSquare='#4C3200'
LightSquare='#B27600'
DarkGreen='#269800'
LightGreen='#59BA00'
DarkPink='#A5197F'
LightPink='#D83B7F'

LayerMax=8

IsBlackAI=1
IsWhiteAI=0
#Handicap=[[2,3,4,5,6,7,8,9,10,11,13,14,15],[0,1,2,3,4,5,6,7,8,9,10,11,13,14,15]]
Handicap=[[],[]]

BlackTimeLeft=120
WhiteTimeLeft=120
BlackTimeRound=BlackTimeLeft
WhiteTimeRound=WhiteTimeLeft

MoveBuffer=10
MoveFactor=40

IsGameStart=0
ToBeUpdated=0
NewTimer=1

IsWhiteTurn=1
OpeningLine=0
GameState=0

TurnsSinceBlackCastleKing=0
TurnsSinceBlackCastleQueen=0
TurnsSinceWhiteCastleKing=0
TurnsSinceWhiteCastleQueen=0

EPCol=-2
IsPromotion=0
FiftyMoves=0

CC0=-1
CR0=-1
CR1=-1
CC1=-1
NewClick=1

root = tk.Tk()
RootStr=str(13*Side)+"x"+str(10*Side)+"+0+0"
root.geometry(RootStr)

TextBlackName=tk.Label(root,text="Black")
TextBlackName.place(x=10*Side,y=Side,height=Side,width=2*Side)
TextBlackName.config(font=("Calibri", int(Side/2)))

TextWhiteName=tk.Label(root,text="White")
TextWhiteName.place(x=10*Side,y=7*Side,height=Side,width=2*Side)
TextWhiteName.config(font=("Calibri", int(Side/2)))

TextBlackClockString=tk.StringVar()
TextBlackClock=tk.Label(root,textvariable=TextBlackClockString)
TextBlackClock.place(x=10*Side,y=2*Side,height=40,width=2*Side)
TextBlackClock.config(font=("Calibri", int(Side/2)))
TextBlackClockString.set(str(math.floor(BlackTimeRound/60))+":"+str(BlackTimeRound%60))
if (BlackTimeRound%60==0):
	TextBlackClockString.set(TextBlackClockString.get()+"0")

TextWhiteClockString=tk.StringVar()
TextWhiteClock=tk.Label(root,textvariable=TextWhiteClockString)
TextWhiteClock.place(x=10*Side,y=8*Side,height=40,width=2*Side)
TextWhiteClock.config(font=("Calibri", int(Side/2)))
TextWhiteClockString.set(str(math.floor(WhiteTimeRound/60))+":"+str(WhiteTimeRound%60))
if (WhiteTimeRound%60==0):
	TextWhiteClockString.set(TextWhiteClockString.get()+"0")

ImgBoard=tk.PhotoImage(file="Board.png")
ImgPromotion=tk.PhotoImage(file="Promotion.png")
ImgBP=tk.PhotoImage(file="BP.png")
ImgWP=tk.PhotoImage(file="WP.png")
ImgBR=tk.PhotoImage(file="BR.png")
ImgWR=tk.PhotoImage(file="WR.png")
ImgBN=tk.PhotoImage(file="BN.png")
ImgWN=tk.PhotoImage(file="WN.png")
ImgBB=tk.PhotoImage(file="BB.png")
ImgWB=tk.PhotoImage(file="WB.png")
ImgBQ=tk.PhotoImage(file="BQ.png")
ImgWQ=tk.PhotoImage(file="WQ.png")
ImgBK=tk.PhotoImage(file="BK.png")
ImgWK=tk.PhotoImage(file="WK.png")
ImgStart=tk.PhotoImage(file="StartButton.png")
ImgTrans=tk.PhotoImage(file="Transparent.png")

BoardImage=tk.Label(root,image=ImgBoard,bd=0)
BoardImage.place(x=Side,y=Side)

StartPinkSquare=tk.Label(root,image=ImgTrans,bd=0)
StartPinkSquare.place(x=-2*Side,y=-2*Side)

StartImage=tk.Label(root,image=ImgStart,bd=0)
StartImage.place(x=10*Side,y=4*Side)

class Piece:
	def __init__(self,index,row,col,type):
		self.index=index
		self.row=row
		self.col=col
		self.type=type
	
class Move:
	#sp=-1 for normal, -2 for starting pawn 2 forward, -3 for en passant, 0 for castling
	#sp=1 through 4 for promotions to knight, bishop, rook, queen
	def __init__(self,p1,p2,sr,sc,er,ec,sp,val):
		self.p1=p1
		self.p2=p2
		self.sr=sr
		self.sc=sc
		self.er=er
		self.ec=ec
		self.sp=sp
		self.val=val
	def __eq__(self, other):
		return (self.p1==other.p1 and self.er==other.er and self.ec==other.ec)

B=[]
for i in range(8):
	br=[0,0,0,0,0,0,0,0]
	B.append(br)
for i in range(2):
	for j in range(8):
		B[6+i][j]=-(j+1+(8*i))
for i in range(2):
	for j in range(8):
		B[1-i][j]=(j+1+(8*i))

BlackPieces=[]
for row in [6,7]:
	for col in range(8):
		BlackTemp=Piece(B[row][col],row,col,0)
		BlackPieces.append(BlackTemp)
WhitePieces=[]
for row in [1,0]:
	for col in range(8):
		WhiteTemp=Piece(B[row][col],row,col,0)
		WhitePieces.append(WhiteTemp)
ColorPieces=[BlackPieces,WhitePieces]
for row in range(2):
	for col in range(16):
		ColorPieces[row][col].type=TypeIndex[col]

ColorAlive=[]
BlackAlive=list(range(16))
WhiteAlive=list(range(16))
ColorAlive=[BlackAlive,WhiteAlive]

NullMove=Move(0,0,-1,-1,-1,-1,-1,0)
BestMove=NullMove

BlackImages=[]
WhiteImages=[]
for j in range(8):
	BlackImages.append(tk.Label(root,image=ImgBP,bd=0))
BlackImages.append(tk.Label(root,image=ImgBR,bd=0))
BlackImages.append(tk.Label(root,image=ImgBN,bd=0))
BlackImages.append(tk.Label(root,image=ImgBB,bd=0))
BlackImages.append(tk.Label(root,image=ImgBQ,bd=0))
BlackImages.append(tk.Label(root,image=ImgBK,bd=0))
BlackImages.append(tk.Label(root,image=ImgBB,bd=0))
BlackImages.append(tk.Label(root,image=ImgBN,bd=0))
BlackImages.append(tk.Label(root,image=ImgBR,bd=0))
for j in range(16):
	if ((j<8 and j%2==0) or (j>=8 and j%2==1)):
		BlackImages[j].config(bg=DarkSquare)
	else:
		BlackImages[j].config(bg=LightSquare)
	if (j<8):
		BlackImages[j].place(x=Side*(j+1),y=2*Side)
	else:
		BlackImages[j].place(x=Side*((j-8)+1),y=Side)

for j in range(8):
	WhiteImages.append(tk.Label(root,image=ImgWP,bd=0))
WhiteImages.append(tk.Label(root,image=ImgWR,bd=0))
WhiteImages.append(tk.Label(root,image=ImgWN,bd=0))
WhiteImages.append(tk.Label(root,image=ImgWB,bd=0))
WhiteImages.append(tk.Label(root,image=ImgWQ,bd=0))
WhiteImages.append(tk.Label(root,image=ImgWK,bd=0))
WhiteImages.append(tk.Label(root,image=ImgWB,bd=0))
WhiteImages.append(tk.Label(root,image=ImgWN,bd=0))
WhiteImages.append(tk.Label(root,image=ImgWR,bd=0))
for j in range(16):
	if ((j<8 and j%2==0) or (j>=8 and j%2==1)):
		WhiteImages[j].config(bg=LightSquare)
	else:
		WhiteImages[j].config(bg=DarkSquare)
	if (j<8):
		WhiteImages[j].place(x=Side*(j+1),y=7*Side)
	else:
		WhiteImages[j].place(x=Side*((j-8)+1),y=8*Side)

ColorImages=[BlackImages,WhiteImages]
PromotionImage=tk.Label(root,image=ImgPromotion,bd=0)

BoardMap={}
EndOfGame=0
IsImmediate=0
ResetCi1=0
ResetCi2=0
ResetBg=DarkSquare

def FindMovesPawn(P):
	global RD, BY, BX, ND, KD, PieceVal, NullMove
	global IsWhiteTurn, TurnsSinceBlackCastleKing, TurnsSinceBlackCastleQueen, TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen, IsPromotion
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	FoundMoves=[]
	index=P.index
	row=P.row
	col=P.col
	
	if (index<0):
		dir=-1
		last=0
		start=6
		epstart=3
		if (col==0 or B[row+dir][col-1]<=0):
			PieceValLeft=0
		else:
			PieceValLeft=PieceVal[ColorPieces[0][B[row+dir][col-1]-1].type]
		if (col==7 or B[row+dir][col+1]<=0):
			PieceValRight=0
		else:
			PieceValRight=PieceVal[ColorPieces[0][B[row+dir][col+1]-1].type]
	else:
		dir=1
		last=7
		start=1
		epstart=4
		if (col==0 or B[row+dir][col-1]>=0):
			PieceValLeft=0
		else:
			PieceValLeft=PieceVal[ColorPieces[0][-B[row+dir][col-1]-1].type]
		if (col==7 or B[row+dir][col+1]>=0):
			PieceValRight=0
		else:
			PieceValRight=PieceVal[ColorPieces[0][-B[row+dir][col+1]-1].type]
	
	if (col>0 and B[row+dir][col-1]*index<0):
		NextMove=Move(index,B[row+dir][col-1],row,col,row+dir,col-1,-1,PieceValLeft)
		FoundMoves.append(NextMove)
	if (col<7 and (B[row+dir][col+1])*index<0):
		NextMove=Move(index,B[row+dir][col+1],row,col,row+dir,col+1,-1,PieceValRight)
		FoundMoves.append(NextMove)
	
	if (B[row+dir][col]==0):
		NextMove=Move(index,0,row,col,row+dir,col,-1,0)
		FoundMoves.append(NextMove)
		if (row==start and B[row+(2*dir)][col]==0):
			NextMove=Move(index,0,row,col,row+(2*dir),col,-2,0)
			FoundMoves.append(NextMove)
	
	if (row==epstart):
		if ((col+1)==EPCol):
			NextMove=Move(index,B[row][col+1],row,col,row+dir,col+1,-3,PieceVal[0])
			FoundMoves.append(NextMove)
		elif ((col-1)==EPCol):
			NextMove=Move(index,B[row][col-1],row,col,row+dir,col-1,-3,PieceVal[0])
			FoundMoves.append(NextMove)
	
	if (row+dir==last):
		SpecialMoves=[]
		for TempMove in FoundMoves:
			for i in range(1,5):
				TempSpecial=copy.deepcopy(TempMove)
				TempSpecial.sp=i
				TempSpecial.val=TempMove.val+PieceVal[i]-PieceVal[0]
				SpecialMoves.append(TempSpecial)
		return SpecialMoves
	
	return FoundMoves

def FindMovesRook(P):
	global RD, BY, BX, ND, KD, PieceVal, NullMove
	global IsWhiteTurn, TurnsSinceBlackCastleKing, TurnsSinceBlackCastleQueen, TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen, IsPromotion
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	FoundMoves=[]
	index=P.index
	
	for d in RD:
		y=d[0]
		x=d[1]
		r=P.row+y
		c=P.col+x
		while (r>=0 and r<=7 and c>=0 and c<=7):
			if (B[r][c]==0):
				NextMove=Move(index,0,P.row,P.col,r,c,-1,0)
				FoundMoves.append(NextMove)
			else:
				if (B[r][c]*index<0):
					if (B[r][c]>0):
						EnemyType=ColorPieces[1][B[r][c]-1].type
					else:
						EnemyType=ColorPieces[0][-B[r][c]-1].type
					NextMove=Move(index,B[r][c],P.row,P.col,r,c,-1,PieceVal[EnemyType])
					FoundMoves.append(NextMove)
				break
					
			r+=y
			c+=x
	
	return FoundMoves

def FindMovesBishop(P):
	global RD, BY, BX, ND, KD, PieceVal, NullMove
	global IsWhiteTurn, TurnsSinceBlackCastleKing, TurnsSinceBlackCastleQueen, TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen, IsPromotion
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	FoundMoves=[]
	index=P.index
	
	for y in BY:
		for x in BX:
			r=P.row+y
			c=P.col+x
			while (r>=0 and r<=7 and c>=0 and c<=7):
				if (B[r][c]==0):
					NextMove=Move(index,0,P.row,P.col,r,c,-1,0)
					FoundMoves.append(NextMove)
				else:
					if (B[r][c]*index<0):
						if (B[r][c]>0):
							EnemyType=ColorPieces[1][B[r][c]-1].type
						else:
							EnemyType=ColorPieces[0][-B[r][c]-1].type
						NextMove=Move(index,B[r][c],P.row,P.col,r,c,-1,PieceVal[EnemyType])
						FoundMoves.append(NextMove)
					break
						
				r+=y
				c+=x
	
	return FoundMoves

def FindMovesKnight(P):
	global RD, BY, BX, ND, KD, PieceVal, NullMove
	global IsWhiteTurn, TurnsSinceBlackCastleKing, TurnsSinceBlackCastleQueen, TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen, IsPromotion
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	
	FoundMoves=[]
	index=P.index
	
	for d in ND:
		y=d[0]
		x=d[1]
		r=P.row+y
		c=P.col+x
		if (r>=0 and r<=7 and c>=0 and c<=7):
			if (B[r][c]==0):
				NextMove=Move(index,0,P.row,P.col,r,c,-1,0)
				FoundMoves.append(NextMove)
			elif (B[r][c]*index<0):
				if (B[r][c]>0):
					EnemyType=ColorPieces[1][B[r][c]-1].type
				else:
					EnemyType=ColorPieces[0][-B[r][c]-1].type
				NextMove=Move(index,B[r][c],P.row,P.col,r,c,-1,PieceVal[EnemyType])
				FoundMoves.append(NextMove)
		
	return FoundMoves

def FindMovesKing(P):
	global RD, BY, BX, ND, KD, PieceVal, NullMove
	global IsWhiteTurn, TurnsSinceBlackCastleKing, TurnsSinceBlackCastleQueen, TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen, IsPromotion
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	global IsImmediate
	
	FoundMoves=[]
	index=P.index
	
	for d in KD:
		y=d[0]
		x=d[1]
		r=P.row+y
		c=P.col+x
		if (r>=0 and r<=7 and c>=0 and c<=7):
			if (B[r][c]==0):
				NextMove=Move(index,0,P.row,P.col,r,c,-1,0)
				FoundMoves.append(NextMove)
			elif (B[r][c]*index<0):
				if (B[r][c]>0):
					EnemyType=ColorPieces[1][B[r][c]-1].type
				else:
					EnemyType=ColorPieces[0][-B[r][c]-1].type
				NextMove=Move(index,B[r][c],P.row,P.col,r,c,-1,PieceVal[EnemyType])
				FoundMoves.append(NextMove)
	
	if ((IsWhiteTurn and (TurnsSinceWhiteCastleKing==0)) or ((not IsWhiteTurn) and (TurnsSinceBlackCastleKing==0))):
		if (B[P.row][5]==0 and B[P.row][6]==0 and (IsImmediate or (not InCheck()))):
			NextMove=Move(index,B[P.row][7],P.row,P.col,P.row,6,0,0)
			FoundMoves.append(NextMove)
	
	if ((IsWhiteTurn and (TurnsSinceWhiteCastleQueen==0)) or ((not IsWhiteTurn) and (TurnsSinceBlackCastleQueen==0))):
		if (B[P.row][1]==0 and B[P.row][2]==0 and B[P.row][3]==0 and (IsImmediate or (not InCheck()))):
			NextMove=Move(index,B[P.row][0],P.row,P.col,P.row,2,0,0)
			FoundMoves.append(NextMove)
	
	return FoundMoves

def FindMovesQueen(P):
	return (FindMovesRook(P)+FindMovesBishop(P))

def FindMovesAll():
	global RD, BY, BX, ND, KD, PieceVal, NullMove
	global IsWhiteTurn, TurnsSinceBlackCastleKing, TurnsSinceBlackCastleQueen, TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen, IsPromotion
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	global IsImmediate
	
	AllMoves=[]
	ca1=1
	if (not IsWhiteTurn):
		ca1=0
	for index in ColorAlive[ca1]:
		if (ColorPieces[ca1][index].index != 0):
			type=ColorPieces[ca1][index].type
			if (type==0):
				AllMoves=AllMoves+FindMovesPawn(ColorPieces[ca1][index])
			elif (type==1):
				AllMoves=AllMoves+FindMovesBishop(ColorPieces[ca1][index])
			elif (type==2):
				AllMoves=AllMoves+FindMovesKnight(ColorPieces[ca1][index])
			elif (type==3):
				AllMoves=AllMoves+FindMovesRook(ColorPieces[ca1][index])
			elif (type==4):
				AllMoves=AllMoves+FindMovesQueen(ColorPieces[ca1][index])
			else:
				AllMoves=AllMoves+FindMovesKing(ColorPieces[ca1][index])
	return AllMoves

def FindMovesLegal():
	global RD, BY, BX, ND, KD, PieceVal, NullMove
	global IsWhiteTurn, TurnsSinceBlackCastleKing, TurnsSinceBlackCastleQueen, TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen, IsPromotion
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	AllMoves=FindMovesAll()
	LegalMoves=[]
	for m in AllMoves:
		
		cp1=1
		cp2=m.p1-1
		if (m.p1<0):
			cp1=0
			cp2=-m.p1-1
		
		cp1e=1
		cp2e=m.p2-1
		if (m.p2<0):
			cp1e=0
			cp2e=-m.p2-1
		
		ModifyForward(m,cp1,cp2,cp1e,cp2e)
		
		OpponentMoves=FindMovesAll()
		
		IsLegal=1
		for om in OpponentMoves:
			if (om.val>=1000):
				IsLegal=0
				break
		
		ModifyBackward(m,cp1,cp2,cp1e,cp2e)
		
		if (IsLegal):
			LegalMoves.append(m)
	
	return LegalMoves
	
def ModifyForward(m,cp1,cp2,cp1e,cp2e):
	global RD, BY, BX, ND, KD, PieceVal, NullMove
	global IsWhiteTurn, TurnsSinceBlackCastleKing, TurnsSinceBlackCastleQueen, TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen, IsPromotion
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	
	B[m.sr][m.sc]=0
	B[m.er][m.ec]=m.p1
	
	ColorPieces[cp1][cp2].row=m.er
	ColorPieces[cp1][cp2].col=m.ec
	
	if (m.p2!=0 and m.sp!=0):
		ColorPieces[cp1e][cp2e].index=0
	
	EPCol=-2
	if (m.sp != -1):
		if (m.sp>0):
			ColorPieces[cp1][cp2].type=m.sp
		else:
			if (m.sp==-2):
				EPCol=m.sc
			elif (m.sp==-3):
				B[m.sr][m.ec]=0
			else:
				if (m.ec==6):
					B[m.sr][7]=0
					B[m.sr][5]=m.p2
					ColorPieces[cp1e][cp2e].col=5
				else:
					B[m.sr][0]=0
					B[m.sr][3]=m.p2
					ColorPieces[cp1e][cp2e].col=3
					
	
	if (IsWhiteTurn):
		if (TurnsSinceWhiteCastleKing==0):
			if (ColorPieces[cp1][cp2].type==5):
				TurnsSinceWhiteCastleKing=1
			elif (ColorPieces[cp1][cp2].type==3 and m.sc==7):
				TurnsSinceWhiteCastleKing=1
		else:
			TurnsSinceWhiteCastleKing+=1
		if (TurnsSinceWhiteCastleQueen==0):
			if (ColorPieces[cp1][cp2].type==5):
				TurnsSinceWhiteCastleQueen=1
			elif (ColorPieces[cp1][cp2].type==3 and m.sc==0):
				TurnsSinceWhiteCastleQueen=1
		else:
			TurnsSinceWhiteCastleQueen+=1
	else:
		if (TurnsSinceBlackCastleKing==0):
			if (ColorPieces[cp1][cp2].type==5):
				TurnsSinceBlackCastleKing=1
			elif (ColorPieces[cp1][cp2].type==3 and m.sc==7):
				TurnsSinceBlackCastleKing=1
		else:
			TurnsSinceBlackCastleKing+=1
		if (TurnsSinceBlackCastleQueen==0):
			if (ColorPieces[cp1][cp2].type==5):
				TurnsSinceBlackCastleQueen=1
			elif (ColorPieces[cp1][cp2].type==3 and m.sc==0):
				TurnsSinceBlackCastleQueen=1
		else:
			TurnsSinceBlackCastleQueen+=1
	
	IsWhiteTurn=not IsWhiteTurn

def ModifyBackward(m,cp1,cp2,cp1e,cp2e):
	global RD, BY, BX, ND, KD, PieceVal, NullMove
	global IsWhiteTurn, TurnsSinceBlackCastleKing, TurnsSinceBlackCastleQueen, TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen, IsPromotion
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	
	IsWhiteTurn=not IsWhiteTurn
	
	EPCol=-2
	if (m.sp != -1):
		if (m.sp>0):
			ColorPieces[cp1][cp2].type=0
		else:
			if (m.sp==-2):
				EPCol=m.sc
			elif (m.sp==-3):
				B[m.sr][m.ec]=0
			else:
				if (m.ec==6):
					B[m.sr][5]=0
					B[m.sr][7]=m.p2
					ColorPieces[cp1e][cp2e].col=7
				else:
					B[m.sr][3]=0
					B[m.sr][0]=m.p2
					ColorPieces[cp1e][cp2e].col=0
	
	if (m.p2!=0):
		ColorPieces[cp1e][cp2e].index=m.p2
	
	ColorPieces[cp1][cp2].row=m.sr
	ColorPieces[cp1][cp2].col=m.sc
	
	B[m.sr][m.sc]=m.p1
	if (m.sp==-3 or m.sp==0):
		B[m.er][m.ec]=0
	else:
		B[m.er][m.ec]=m.p2
	
	if (IsWhiteTurn):
		if (TurnsSinceWhiteCastleKing>0):
			TurnsSinceWhiteCastleKing-=1
		if (TurnsSinceWhiteCastleQueen>0):
			TurnsSinceWhiteCastleQueen-=1
	else:
		if (TurnsSinceBlackCastleKing>0):
			TurnsSinceBlackCastleKing-=1
		if (TurnsSinceBlackCastleQueen>0):
			TurnsSinceBlackCastleQueen-=1

def MiddleBonus(r,c):
	return(0.001*(12.25-(abs(3.5-r)+abs(3.5-c))))

def BurdenBonus(sr,sc,type):
	if ((type==1 or type==2) and (sr==0 or sr==7) and (sc==5 or sc==6)):
		return 0.2
	if (type==0):
		if ((sr==1 or sr==6) and (sc==4)):
			return 0.3
		if ((sc==5 or sc==6 or sc==7)):
			return -0.1
	return 0

def Coverage():
	global IsWhiteTurn, ColorPieces
	
	cval=0
	C=[]
	for i in range(8):
		cr=[0,0,0,0,0,0,0,0]
		C.append(cr)
	IsWhiteTurn=(not IsWhiteTurn)
	AllMoves=FindMovesAll()
	IsWhiteTurn=(not IsWhiteTurn)
	for m in AllMoves:
		C[m.er][m.ec]+=1
	for p in ColorPieces[1-IsWhiteTurn]:
		if (p.index!=0 and C[p.row][p.col]==0):
			cval-=10
	for row in range(8):
		for col in range(8):
			proximity=8-abs(3.5-row)-abs(3.5-col)
			cval+=proximity*C[row][col]
	
	return cval

def PawnCoverage():
	global IsWhiteTurn, ColorPieces
	if (IsWhiteTurn):
		backrow=7
	else:
		backrow=0
	
	cval=0
	C=[]
	for i in range(8):
		cr=[0,0,0,0,0,0,0,0]
		C.append(cr)
	IsWhiteTurn=(not IsWhiteTurn)
	AllMoves=FindMovesAll()
	IsWhiteTurn=(not IsWhiteTurn)
	for m in AllMoves:
		C[m.er][m.ec]+=1
	for p in ColorPieces[1-IsWhiteTurn]:
		if (p.index!=0 and C[p.row][p.col]==0):
			cval-=10
	for row in range(8):
		for col in range(8):
			proximity=8-abs(3.5-row)-abs(3.5-col)
			cval+=proximity*C[row][col]
	
	cval*=0.01
	
	pval=0
	dir=1
	if (IsWhiteTurn):
		dir=-1
	for p in ColorPieces[1-IsWhiteTurn]:
		if (p.index!=0 and p.type==0):
			if (C[p.row+dir][p.col]>1):
				pval+=(abs(p.row-backrow))
			for pr in ColorPieces[1-IsWhiteTurn]:
				if (pr.index!=0 and (pr.type==3 or pr.type==4)):
					if (p.col==pr.col):
						pval+=2*(abs(p.row-backrow))
		
		
	return (cval+pval)

def SoftVal():
	global IsWhiteTurn, ColorPieces, GameState
	
	val=0
	if (IsWhiteTurn):
		backrow=7
		pawnrow=6
	else:
		backrow=0
		pawnrow=1
		
	if (GameState==0):
		#Opening
		if (abs(B[backrow][6])==13 or abs(B[backrow][2])==13):
			val+=0.3 #castled
		val-=0.1*abs(ColorPieces[1-IsWhiteTurn][12].row-backrow) #king away from back row
		if (abs(B[backrow][5])==14):
			val-=0.2
		if (abs(B[backrow][6])==15):
			val-=0.2
		if (abs(B[pawnrow][4])==5):
			val-=0.2
		if (abs(B[backrow][1])==10):
			val-=0.1
		if (abs(B[backrow][2])==11):
			val-=0.1
		if (abs(B[pawnrow][3])==4):
			val-=0.1
		val+=Coverage()*0.001
	elif (GameState==1):
		addval=0
		for bp in ColorPieces[0]:
			if (bp.index!=0 and bp.type==0):
				addval-=0.1/(bp.row)
		for wp in ColorPieces[1]:
			if (wp.index!=0 and wp.type==0):
				addval+=0.1/(7-wp.row)
		if (IsWhiteTurn):
			addval*=-1
		val+=addval
		val+=Coverage()*0.001
	elif (GameState==2):
		val=PawnCoverage()*0.001
	else:
		ekrow=ColorPieces[IsWhiteTurn][12].row
		ekcol=ColorPieces[IsWhiteTurn][12].col
		krow=ColorPieces[1-IsWhiteTurn][12].row
		kcol=ColorPieces[1-IsWhiteTurn][12].col
		rowdiff=0
		rcol=-1
		coldiff=0
		rrow=-1
		rowopp=0
		colopp=0
		if (ekcol==kcol and abs(ekrow-krow)==2):
			rowopp=1
		if (ekrow==krow and abs(ekcol-kcol)==2):
			colopp=1
		
		for p in ColorPieces[1-IsWhiteTurn]:
			if (p.index!=0 and (p.type==3 or p.type==4)):
				if (abs(ekrow-p.row)==1 and p.row!=krow):
					val+=(0.1+abs(ekcol-p.col)*0.0001)
					rowdiff=(ekrow-p.row)
					rcol=p.col
				elif (abs(ekcol-p.col)==1 and p.col!=kcol):
					val+=(0.1+abs(p.row-ekrow)*0.0001)
					coldiff=(ekcol-p.col)
					rrow=p.row
				elif (rowopp and (p.row==ekrow)):
					val+=0.5
				elif (colopp and (p.col==ekcol)):
					val+=0.5
			elif (p.index!=0 and (p.type==1 or p.type==2)):
				val-=0.00001*(abs(backrow-p.row)+abs(backrow-p.col))
		if (rowdiff!=0):
			if (ekrow-krow==(2*rowdiff)):
				val+=0.1
				if (abs(ekcol-kcol)==1):
					val+=0.1
			for p in ColorPieces[1-IsWhiteTurn]:
				if (p.index!=0 and (p.type==3 or p.type==4)):
					if (p.row==ekrow):
						val+=0.5
			if (kcol==rcol):
				val-=0.2
			if (rowdiff*(ekrow-krow)>0):
				val+=0.2
		if (coldiff!=0):
			if (ekcol-kcol==(2*rowdiff)):
				val+=0.1
				if (abs(ekrow-krow)==1):
					val+=0.1
			for p in ColorPieces[1-IsWhiteTurn]:
				if (p.index!=0 and (p.type==3 or p.type==4)):
					if (p.col==ekcol):
						val+=0.5
			if (krow==rrow):
				val-=0.2
			if (coldiff*(ekcol-kcol)>0):
				val+=0.2
		val-=0.001*(abs(ekrow-krow)+abs(ekcol-kcol))
		
	return val

def PriorityCalc(m):
	global ColorPieces
	cp1=1
	cp2=m.p1-1
	if (m.p1<0):
		cp1=0
		cp2=-m.p1-1
	if (ColorPieces[cp1][cp2].type==0):
		return (m.val+1)
	return (m.val+3)
	
def CalcVal(secondlayer,states,extramove,sparelayers):
	global RD, BY, BX, ND, KD, PieceVal, NullMove
	global IsWhiteTurn, TurnsSinceBlackCastleKing, TurnsSinceBlackCastleQueen, TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen, IsPromotion
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	global root, t0, BlackTimeLeft, WhiteTimeLeft, BlackTimeRound, WhiteTimeRound, TextBlackClockString, TextWhiteClockString, IsWhiteTurnTrue
	global GameState
	
	if (GameState==0 and (not InCheck())):
		AllMoves=FindMovesAll()
	else:
		AllMoves=FindMovesLegal()
	
	bestval=-4000
	if (len(AllMoves)==0):
		if (InCheck()):
			bestval=-3000
		else:
			bestval=3000
	
	TotalCaptures=0
	for m in AllMoves:
		if (m.p2!=0):
			TotalCaptures+=1
	
	TotalPriority=0
	for m in AllMoves:
		TotalPriority+=PriorityCalc(m)
	
	for m in AllMoves:
		cp1=1
		cp2=m.p1-1
		if (m.p1<0):
			cp1=0
			cp2=-m.p1-1
		
		cp1e=1
		cp2e=m.p2-1
		if (m.p2<0):
			cp1e=0
			cp2e=-m.p2-1
		
		ModifyForward(m,cp1,cp2,cp1e,cp2e)
		
		if (m.val==1000):
			tempval=1000
		else:
			tempval=m.val
			nextstates=(states*PriorityCalc(m)/TotalPriority)-1
			if (nextstates>0 or sparelayers>0):
				tempval=m.val-0.99*CalcVal(0,nextstates,1-extramove,sparelayers-1)
			elif (extramove):
				tempval=0

		if (secondlayer):
			IsWhiteTurn=(not IsWhiteTurn)
			S=HashBoard()
			IsWhiteTurn=(not IsWhiteTurn)
			if (RepeatedPosition(S)>1):
				tempval=3000
			UnrepeatPosition(S)
		
		if (tempval>bestval):
			bestval=tempval
		
		ModifyBackward(m,cp1,cp2,cp1e,cp2e)
	
	t1=time.clock()
	
	if (IsWhiteTurnTrue):
		TempWhiteTimeLeft=WhiteTimeLeft-(t1-t0)
		if (round(TempWhiteTimeLeft) != WhiteTimeRound):
			WhiteTimeRound=round(TempWhiteTimeLeft)
			TextWhiteClockString.set("{:0>1}:{:0>2}".format(int(WhiteTimeRound/60),WhiteTimeRound%60))
			root.update()
	else:
		TempBlackTimeLeft=BlackTimeLeft-(t1-t0)
		if (round(TempBlackTimeLeft) != BlackTimeRound):
			BlackTimeRound=round(TempBlackTimeLeft)
			TextBlackClockString.set("{:0>1}:{:0>2}".format(int(BlackTimeRound/60),BlackTimeRound%60))
			root.update()
	
	return bestval

def ConvertToNotation(m):
	global ColorPieces, BestMove
	global NotationCol, NotationChar
	
	if (m.sp==0):
		if (m.ec==6):
			return ("O-O")
		else:
			return ("O-O-O")
	
	cp1=1
	cp2=m.p1-1
	if (m.p1<0):
		cp1=0
		cp2=-m.p1-1
	type=ColorPieces[cp1][cp2].type
	
	s=""
	if (type==0 and m.p2!=0):
		s+=NotationCol[m.sc]
	else:
		s+=NotationChar[type]
	if (m.p2!=0):
		s+='x'
	s+=NotationCol[m.ec]
	s+=str(m.er+1)
	
	return s
	
def ReverseNotation(s):
	global IsWhiteTurn, ColorPieces, BestMove
	global ReverseCol, ReverseChar
	
	if (s=="O-O"):
		type=5
		er=7
		if (IsWhiteTurn):
			er=0
		ec=6
		
	elif (s=="O-O-O"):
		type=5
		er=7
		if (IsWhiteTurn):
			er=0
		ec=2
		
	else:
		if (s[0] in ReverseChar):
			type=ReverseChar[s[0]]
		else:
			type=0
		if (s[1]=='x'):
			ec=ReverseCol[s[2]]
			er=ord(s[3])-ord('0')-1
		elif (type==0):
			ec=ReverseCol[s[0]]
			er=ord(s[1])-ord('0')-1
		else:
			ec=ReverseCol[s[1]]
			er=ord(s[2])-ord('0')-1
	
	p1vals=[]
	cp1=0
	mult=-1
	if (IsWhiteTurn):
		cp1=1
		mult=1
	for i in range(16):
		if (ColorPieces[cp1][i].type==type):
			p1vals.append((i+1)*mult)
	
	AllMoves=FindMovesLegal()
	
	BestMove=AllMoves[0]
	for m in AllMoves:
		for p1 in p1vals:
			checkmove=Move(p1,0,-1,-1,er,ec,-1,0)
			if (m==checkmove):
				BestMove=m
	
def IsOpening():
	global OpeningLine, IsWhiteAI, IsBlackAI
	
	if (OpeningLine==-1):
		return 0
	
	found=1
	if (not (IsWhiteTurn and OpeningLine==0)):
		prevmove=ConvertToNotation(BestMove)
		list=(linecache.getline(Rfilename,OpeningLine+1)).split()
		found=0
		for i in range(1,len(list),2):
			if (list[i]==prevmove):
				OpeningLine=int(list[i+1])
				found=1
				break
	
	if (not found):
		OpeningLine=-1
		return 0
	
	list=(linecache.getline(Rfilename,OpeningLine+1)).split()
	if (len(list)==1):
		OpeningLine=-1
		return 0
	
	bestfreq=-1
	bestnote=""
	for i in range(2,len(list),2):
		checklist=(linecache.getline(Rfilename,int(list[i])+1)).split()
		freq=int(checklist[0])
		if (freq>bestfreq):
			bestfreq=freq
			bestnote=list[i-1]
			if ((not IsWhiteAI) or (not IsBlackAI)):
				OpeningLine=int(list[i])
	ReverseNotation(bestnote)
	
	return 1

def CalcMove():
	global RD, BY, BX, ND, KD, PieceVal, NullMove
	global IsWhiteTurn, TurnsSinceBlackCastleKing, TurnsSinceBlackCastleQueen, TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen, IsPromotion
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	global WhiteTimeLeft, BlackTimeLeft
	global GameState
	global MoveBuffer, MoveFactor
		
	if (IsOpening()):
		return
	
	if (ColorPieces[0][11].index!=0 and ColorPieces[1][11].index!=0):
		GameState=0
	else:
		bpieces=0
		bpawns=0
		wpieces=0
		wpawns=0
		for i in range(16):
			if (ColorPieces[0][i].index!=0):
				if (ColorPieces[0][i].type==0):
					bpawns=1
				elif (ColorPieces[0][i].type!=5):
					bpieces=1
			if (ColorPieces[1][i].index!=0):
				if (ColorPieces[1][i].type==0):
					wpawns=1
				elif (ColorPieces[1][i].type!=5):
					wpieces=1
		if (bpieces and wpieces):
			GameState=1
		elif (bpawns or wpawns):
			GameState=2
		else:
			GameState=3
	
	LegalMoves=FindMovesLegal()
	bestval=-5000
	BestMove=NullMove
	
	NumPlayerMoves=len(FindMovesAll())
	IsWhiteTurn=(not IsWhiteTurn)
	NumEnemyMoves=len(FindMovesAll())
	IsWhiteTurn=(not IsWhiteTurn)
	
	if (IsWhiteTurn):
		states=(StateConst*WhiteTimeLeft-MoveBuffer)/(MoveFactor*NumPlayerMoves*NumEnemyMoves)
	else:
		states=(StateConst*BlackTimeLeft-MoveBuffer)/(MoveFactor*NumPlayerMoves*NumEnemyMoves)
			
	TotalPriority=0
	for m in LegalMoves:
		TotalPriority+=PriorityCalc(m)
		
	sparelayers=0
	
	if (not SufficientMaterial(1-IsWhiteTurn)):
		sparelayers=2
		
	for m in LegalMoves:
		cp1=1
		cp2=m.p1-1
		if (m.p1<0):
			cp1=0
			cp2=-m.p1-1
		
		cp1e=1
		cp2e=m.p2-1
		if (m.p2<0):
			cp1e=0
			cp2e=-m.p2-1
		ModifyForward(m,cp1,cp2,cp1e,cp2e)
		nextstates=(states*PriorityCalc(m)/TotalPriority)-1
		tempval=m.val
		S=HashBoard()
		RepVal=RepeatedPosition(S)
		if (nextstates>0 or sparelayers>0):
			tempval-=0.99*CalcVal(1,nextstates,0,sparelayers-1)
		UnrepeatPosition(S)
		tempval+=SoftVal()
		#print(m.sr,m.sc,m.er,m.ec,tempval,nextstates)
		if (RepVal>1):
			tempval=-3000
		#print(m.sr,m.sc,m.er,m.ec,tempval)
		if (tempval>bestval):
			bestval=tempval
			BestMove=m
		ModifyBackward(m,cp1,cp2,cp1e,cp2e)

def IsValid():
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	LegalMoves=FindMovesLegal()
	#print()
	#print(BestMove.p1, BestMove.p2)
	for m in LegalMoves:
		#print(m.sr,m.sc,m.er,m.ec)
		if (m==BestMove):
			BestMove=m
			return 1
	return 0

def InCheck():
	global RD, BY, BX, ND, KD, PieceVal, NullMove
	global IsWhiteTurn, TurnsSinceBlackCastleKing, TurnsSinceBlackCastleQueen, TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen, IsPromotion
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	global IsImmediate
	
	IsWhiteTurn=(not IsWhiteTurn)
	IsImmediate=1
	OpponentMoves=FindMovesAll()
	IsImmediate=0
	for om in OpponentMoves:
		if (om.val==1000):
			IsWhiteTurn=(not IsWhiteTurn)
			return 1
	IsWhiteTurn=(not IsWhiteTurn)
	return 0
	
def Update():
	global IsWhiteTurn, TurnsSinceBlackCastleKing, TurnsSinceBlackCastleQueen, TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen, IsPromotion
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	global ToBeUpdated, CC0, CR0, CR1, CC1, NewClick, root, ColorImages, PromotionImage
	global IsBlackAI, IsWhiteAI, LayerMax
	global ResetCi1, ResetCi2, ResetBg
	global FiftyMoves
	
	m=BestMove
		
	cp1=1
	cp2=m.p1-1
	if (m.p1<0):
		cp1=0
		cp2=-m.p1-1
	
	if (ColorPieces[cp1][cp2].type!=0 and m.p2==0):
		FiftyMoves+=1
	else:
		FiftyMoves=0
	
	if ((not IsPromotion) and ColorPieces[cp1][cp2].type==0 and (m.er==7 or m.er==0)):
		IsPromotion=1
		if ((IsWhiteTurn and (not IsWhiteAI)) or ((not IsWhiteTurn) and (not IsBlackAI))):
			PromotionImage.place(x=Side,y=Side-24)
	else:
	
		PromotionImage.place(x=-2*Side,y=-2*Side)
		
		cp1e=1
		cp2e=m.p2-1
		if (m.p2<0):
			cp1e=0
			cp2e=-m.p2-1
		
		ModifyForward(m,cp1,cp2,cp1e,cp2e)
		
		for i in range(2):
			for j in ColorAlive[i]:
				if (ColorPieces[i][j].index==0):
					ColorAlive[i].remove(j)
		
		#GUI
		
		ci1=1
		ci2=m.p1-1
		if (m.p1<0):
			ci1=0
			ci2=-m.p1-1
		
		ColorImages[ResetCi1][ResetCi2].config(bg=ResetBg)
		
		if ((m.ec+m.er)%2==0):
			ColorImages[ci1][ci2].config(bg=DarkPink)
		else:
			ColorImages[ci1][ci2].config(bg=LightPink)
			
		if ((m.sc+m.sr)%2==0):
			StartPinkSquare.config(bg=DarkPink)
		else:
			StartPinkSquare.config(bg=LightPink)
			
		ColorImages[ci1][ci2].place(x=Side*(m.ec+1),y=Side*(8-m.er))
		StartPinkSquare.place(x=Side*(m.sc+1),y=Side*(8-m.sr))
		
		ResetCi1=ci1
		ResetCi2=ci2
		if ((m.ec+m.er)%2==0):
			ResetBg=DarkSquare
		else:
			ResetBg=LightSquare
		
		if (m.p2!=0):
			ci1e=1
			ci2e=m.p2-1
			if (m.p2<0):
				ci1e=0
				ci2e=-m.p2-1
			if (m.sp==0):
				if (m.ec==6):
					ColorImages[ci1e][ci2e].place(x=6*Side,y=Side*(8-m.er))
				else:
					ColorImages[ci1e][ci2e].place(x=4*Side,y=Side*(8-m.er))
				if ((m.ec+m.er)%2==1):
					ColorImages[ci1e][ci2e].config(bg=DarkSquare)
				else:
					ColorImages[ci1e][ci2e].config(bg=LightSquare)
					
			else:
				ColorImages[ci1e][ci2e].place(x=-2*Side,y=-2*Side)
		
		if (m.sp>0):
			if (m.p1>0):
				if (m.sp==1):
					ColorImages[ci1][ci2].config(image=ImgWB)
				elif (m.sp==2):
					ColorImages[ci1][ci2].config(image=ImgWN)
				elif (m.sp==3):
					ColorImages[ci1][ci2].config(image=ImgWR)
				else:
					ColorImages[ci1][ci2].config(image=ImgWQ)
			else:
				if (m.sp==1):
					ColorImages[ci1][ci2].config(image=ImgBB)
				elif (m.sp==2):
					ColorImages[ci1][ci2].config(image=ImgBN)
				elif (m.sp==3):
					ColorImages[ci1][ci2].config(image=ImgBR)
				else:
					ColorImages[ci1][ci2].config(image=ImgBQ)
					ColorImages[ci1][ci2].config(image=ImgBQ)
			IsPromotion=0	

def DebugBoard():
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	print()
	for i in range(7,-1,-1):
		for j in range(8):
			sys.stdout.write(str(B[i][j]))
			sys.stdout.write(" ")
			if (B[i][j]>=0):
				sys.stdout.write(" ")
			if (abs(B[i][j])<=9):
				sys.stdout.write(" ")
		print()

def DebugColorPieces():
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	print()
	for i in ColorPieces:
		for p in i:
			print(p.index,p.row,p.col,p.type)

def DebugFindMovesAll():
	AllMoves=FindMovesAll()
	for m in AllMoves:
		print(m.p1,m.p2,m.sr,m.sc,m.er,m.ec,m.sp)
			
def ClickPosition(event):
	global IsGameStart
	MY = root.winfo_pointery() - root.winfo_rooty()
	MX = root.winfo_pointerx() - root.winfo_rootx()
	if (IsGameStart):
		ClickBoard(MY,MX)
	elif (MX>=Side and MX <12*Side and MY>=4*Side and MY<6*Side):
		IsGameStart=1
	
def ClickBoard(i,j):
	global IsWhiteTurn, TurnsSinceBlackCastleKing, TurnsSinceBlackCastleQueen, TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen, IsPromotion
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	global ToBeUpdated, CC0, CR0, CR1, CC1, NewClick, root, ColorImages, PromotionImage
	global IsWhiteTurnTrue
	
	if (IsPromotion and i>=Side-24 and i<Side and j>=Side and j<(Side+480)):
		BestMove.sp=(4-math.floor((j-60)/120))
		ToBeUpdated=1
	elif ((not IsPromotion) and i>=Side and i<9*Side and j>=Side and j<9*Side):
		if ((IsWhiteTurnTrue and (not IsWhiteAI)) or (not IsWhiteTurnTrue and (not IsBlackAI))):
			r=int(8-math.floor(i/60))
			c=int(math.floor(j/60)-1)
			if (NewClick):
				if ((B[r][c]>0 and IsWhiteTurnTrue) or (B[r][c]<0 and (not IsWhiteTurnTrue))):
					NewClick=0
					CR0=r
					CC0=c
					ci1=1
					ci2=B[CR0][CC0]-1
					if (B[CR0][CC0]<0):
						ci1=0
						ci2=-B[CR0][CC0]-1
						ci2=-B[CR0][CC0]-1
					if ((CR0+CC0)%2==0):
						ColorImages[ci1][ci2].config(bg=DarkGreen)
					else:
						ColorImages[ci1][ci2].config(bg=LightGreen)
			else:
				if (B[r][c]*B[CR0][CC0]>0):
					
					ci1=1
					ci2=B[CR0][CC0]-1
					if (B[CR0][CC0]<0):
						ci1=0
						ci2=-B[CR0][CC0]-1
					if ((CR0+CC0)%2==0):
						ColorImages[ci1][ci2].config(bg=DarkSquare)
					else:
						ColorImages[ci1][ci2].config(bg=LightSquare)
					
					if (CR0 != r or CC0 != c):
						CR0=r
						CC0=c
						ci1=1
						ci2=B[CR0][CC0]-1
						if (B[CR0][CC0]<0):
							ci1=0
							ci2=-B[CR0][CC0]-1
						if ((CR0+CC0)%2==0):
							ColorImages[ci1][ci2].config(bg=DarkGreen)
						else:
							ColorImages[ci1][ci2].config(bg=LightGreen)
					else:
						CR0=-1
						CC0=-1
						NewClick=1
				else:
					NewClick=1
					CR1=r
					CC1=c
					m=Move(B[CR0][CC0],B[CR1][CC1],CR0,CC0,CR1,CC1,-1,0)
					BestMove=m
					if (IsValid()):
						ToBeUpdated=1
					else:
						ci1=1
						ci2=B[CR0][CC0]-1
						if (B[CR0][CC0]<0):
							ci1=0
							ci2=-B[CR0][CC0]-1
						if ((CR0+CC0)%2==0):
							ColorImages[ci1][ci2].config(bg=DarkSquare)
						else:
							ColorImages[ci1][ci2].config(bg=LightSquare)

def HashBoard():
	global IsWhiteTurn, TurnsSinceBlackCastleKing, TurnsSinceBlackCastleQueen, TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen, IsPromotion
	global B, ColorPieces, ColorAlive, BestMove, EPCol
	global BoardMap
	
	S=str(IsWhiteTurn)
	for row in B:
		for col in row:
			S+=str(col)
	return S

def RepeatedPosition(S):
	global BoardMap, IsWhiteTurn
	
	#S=HashBoard()
	if (S in BoardMap):
		BoardMap[S]+=1
	else:
		BoardMap.update({S:1})
	return BoardMap[S]

def UnrepeatPosition(S):
	global BoardMap
	BoardMap[S]-=1

def SufficientMaterial(cp1):
	global ColorPieces
	bishops=0
	for p in ColorPieces[cp1]:
		if (p.index != 0):
			if (p.type==0 or p.type==3 or p.type==4):
				return 1
			if (p.type==1):
				if (bishops==1):
					return 1
				bishops=1
			else:
				if (bishops==1):
					return 1
	return 0

def ImplementHandicap():
	for cp1 in range(2):
		for cp2 in Handicap[cp1]:
			B[ColorPieces[cp1][cp2].row][ColorPieces[cp1][cp2].col]=0
			ColorPieces[cp1][cp2].index=0
			ColorImages[cp1][cp2].place(x=-2*Side,y=-2*Side)
			ColorAlive[cp1].remove(cp2)
					
ImplementHandicap()

root.bind("<Button 1>",ClickPosition)
root.title("Internal Combustion Chess Engine")

while (not IsGameStart):
	root.update_idletasks()
	root.update()
	
while (1):
	t0=time.clock()
	IsWhiteTurnTrue=copy.deepcopy(IsWhiteTurn)
	root.update_idletasks()
	root.update()
	
	if ((IsWhiteTurn and (IsWhiteAI)) or ((not IsWhiteTurn) and (IsBlackAI))):
		CalcMove()
		if (not (BestMove==NullMove)):
			ToBeUpdated=1
	
	t1=time.clock()
	
	if (IsWhiteTurn):
		WhiteTimeLeft-=(t1-t0)
		if (round(WhiteTimeLeft) != WhiteTimeRound):
			WhiteTimeRound=round(WhiteTimeLeft)
			TextWhiteClockString.set("{:0>1}:{:0>2}".format(int(WhiteTimeRound/60),WhiteTimeRound%60))
			
	else:
		BlackTimeLeft-=(t1-t0)
		if (round(BlackTimeLeft) != BlackTimeRound):
			BlackTimeRound=round(BlackTimeLeft)
			TextBlackClockString.set("{:0>1}:{:0>2}".format(int(BlackTimeRound/60),BlackTimeRound%60))
	
	if (WhiteTimeLeft<0):
		if (SufficientMaterial(0)):
			print("Black wins")
			ImgEndBlack=tk.PhotoImage(file="EndBlack.png")
			EndBlackImage=tk.Label(root,image=ImgEndBlack,bd=0)
			EndBlackImage.place(x=10*Side,y=4*Side)
			EndOfGame=1
		else:
			print("Insufficient Material")
			ImgEndDraw=tk.PhotoImage(file="EndDraw.png")
			EndDrawImage=tk.Label(root,image=ImgEndDraw,bd=0)
			EndDrawImage.place(x=10*Side,y=4*Side)
			EndOfGame=1
	elif (BlackTimeLeft<0):
		if (SufficientMaterial(1)):
			print("White wins")
			ImgEndWhite=tk.PhotoImage(file="EndWhite.png")
			EndWhiteImage=tk.Label(root,image=ImgEndWhite,bd=0)
			EndWhiteImage.place(x=10*Side,y=4*Side)
			EndOfGame=1
		else:
			print("Insufficient Material")
			ImgEndDraw=tk.PhotoImage(file="EndDraw.png")
			EndDrawImage=tk.Label(root,image=ImgEndDraw,bd=0)
			EndDrawImage.place(x=10*Side,y=4*Side)
			EndOfGame=1
	
	if (ToBeUpdated):
		#print(BestMove.p1,BestMove.p2,BestMove.sr,BestMove.sc,BestMove.er,BestMove.ec,BestMove.sp)
		Update()
		#DebugBoard()
		#DebugColorPieces()
		#DebugFindMovesAll()
		#print(TurnsSinceWhiteCastleKing, TurnsSinceWhiteCastleQueen)
		ToBeUpdated=0
		LegalMoves=FindMovesLegal()
		if (len(LegalMoves)==0):
			if (InCheck()):
				if (IsWhiteTurn):
					print("Black wins")
					ImgEndBlack=tk.PhotoImage(file="EndBlack.png")
					EndBlackImage=tk.Label(root,image=ImgEndBlack,bd=0)
					EndBlackImage.place(x=10*Side,y=4*Side)
					EndOfGame=1
				else:
					print("White wins")
					ImgEndWhite=tk.PhotoImage(file="EndWhite.png")
					EndWhiteImage=tk.Label(root,image=ImgEndWhite,bd=0)
					EndWhiteImage.place(x=10*Side,y=4*Side)
					EndOfGame=1
			else:
				print("Stalemate")
				ImgEndDraw=tk.PhotoImage(file="EndDraw.png")
				EndDrawImage=tk.Label(root,image=ImgEndDraw,bd=0)
				EndDrawImage.place(x=10*Side,y=4*Side)
				EndOfGame=1
		elif (RepeatedPosition(HashBoard())==3):
			print("Repeated Position")
			ImgEndDraw=tk.PhotoImage(file="EndDraw.png")
			EndDrawImage=tk.Label(root,image=ImgEndDraw,bd=0)
			EndDrawImage.place(x=10*Side,y=4*Side)
			EndOfGame=1
		elif (FiftyMoves==100):
			print("Fifty Moves Rule")
			ImgEndDraw=tk.PhotoImage(file="EndDraw.png")
			EndDrawImage=tk.Label(root,image=ImgEndDraw,bd=0)
			EndDrawImage.place(x=10*Side,y=4*Side)
			EndOfGame=1
	
	if (EndOfGame):
		break
		
	
	









