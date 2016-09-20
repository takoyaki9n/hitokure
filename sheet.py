# coding=UTF-8

import copy

circle=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
plus=((-1,0),(0,-1),(0,1),(1,0))
times=((-1,-1),(-1,1),(1,-1),(1,1))
tfdict={True:0,False:1}

class Sheet():
    def __init__(self,matrix):
        self.set_sheet(matrix)
        
    def set_sheet(self,matrix):
        self.progress=0
        self.height=len(matrix)
        self.width=len(matrix[0])
        self.numbers=matrix
        self.flags=[[],[]]#[黒マスフラグ,白マスフラグ]
        self.answers=[]
        for i in range(self.height):
            self.numbers[i]=tuple(self.numbers[i])
            self.flags[0].append([False]*self.width)
            self.flags[1].append([False]*self.width)
        self.numbers=tuple(self.numbers)
    
    def solve(self):
        sheet=copy.deepcopy(self)
        self.search(sheet,100.0)
        if len(self.answers)!=0:
            print(str(len(self.answers))+"個の解が見つかりました。")
            for answer in self.answers:
                print(answer+"\n")
        else:
            print("解がありませんでした。")
    
    def search(self,sheet,value):
        pos=sheet.undesided_cell()
        if pos:
            oldsheet=copy.deepcopy(sheet)
            for n in range(2):
                if sheet.sieving(n,pos[0],pos[1]):
                    self.search(sheet,value/2)
                else:
                    self.progress+=value/2
                    print(self.progress)
                sheet=copy.deepcopy(oldsheet)
        else:
            self.answers.append(sheet.to_string())
            self.progress+=value
            print(self.progress)
        
    def undesided_cell(self):
        for i in range(self.height):
            for j in range(self.width):
                if not (self.flags[0][i][j] or self.flags[1][i][j]):
                    return (i,j)
        return None
                
    def sieving(self,n,x,y):
        self.flags[n][x][y]=True
        if n==0:
            return self.black_node(x, y)
        elif n==1:
            return self.white_node(x, y)
    
    def black_node(self,x,y):
        poses=[]
        for d in plus:
            i,j=(x+d[0],y+d[1])
            if self.is_valid_index(i, j):
                if self.flags[0][i][j]:#既に隣に黒マスがある
                    return False
                elif not self.flags[1][i][j]:#未確定マスである
                    poses.append((i,j))
        count=[0,0]#斜め方向の[欄外,黒マス]
        for d in times:
            i,j=(x+d[0],y+d[1])
            if not self.is_valid_index(i, j):
                count[0]+=1
            elif self.flags[0][i][j]:
                count[1]+=1
        if count[1]>0 and sum(count)>1:#分断の必要条件
            if self.is_separated(x,y):
                return False
        for pos in poses:
            self.flags[1][pos[0]][pos[1]]=True
            if not self.white_node(pos[0], pos[1]):
                return False
        return True
        
    def white_node(self,x,y):
        poses=[]
        for j in range(self.width):
            if self.numbers[x][y]==self.numbers[x][j] and y!=j:
                if self.flags[1][x][j]:#既に同じラインに同じ番号の白マスがある
                    return False
                elif not self.flags[0][x][j]:#未確定マスである
                    poses.append((x,j))
        for i in range(self.height):
            if self.numbers[x][y]==self.numbers[i][y] and x!=i:
                if self.flags[1][i][y]:
                    return False
                elif not self.flags[0][i][y]:
                    poses.append((i,y))
        for pos in poses:
            self.flags[0][pos[0]][pos[1]]=True
            if not self.black_node(pos[0], pos[1]):
                return False
        return True
    
    def is_separated(self,x,y):#分断判定
        matrix=[]
        pos=()
        for i in range(self.height):
            matrix.append([])
            for j in range(self.width):
                if self.flags[0][i][j]:#黒確定マスは-1それ以外は0ただしグループ分けの始点は1
                    matrix[i].append(-1)
                elif pos:
                    matrix[i].append(0)
                else:
                    matrix[i].append(1)
                    pos=(i,j)
        self.grouping(pos, matrix)
        for i in range(self.height):
            for j in range(self.width):
                if matrix[i][j]==0:
                    return True
        return False
                         
    def grouping(self,pos,matrix):#再帰的グループ分け
        for d in plus:
            i,j=(pos[0]+d[0],pos[1]+d[1])
            if self.is_valid_index(i,j) and matrix[i][j]==0:
                matrix[i][j]=1
                self.grouping((i,j), matrix)
    
    def to_string(self):
        string=""
        for i in range(self.height):
            for j in range(self.width):
                b,w=(self.flags[0][i][j],self.flags[1][i][j])
                if not(b or w):
                    string+="ー"
                elif b and not w:
                    string+="■"
                elif not b and w:
                    string+="×"
                else:
                    print(str(i)+"行"+str(j)+"列のフラグが両方立っています。")
                    return None
            string+="\n"
        string=string[:len(string)-1]
        return string

    def is_valid_index(self,i,j):
        return (0<=i and i<self.height) and (0<=j and j<self.width)