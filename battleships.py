import tkinter as tk
import random
from tkinter import messagebox

class game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.state("zoomed")
        self.root.title("Battleships")
        self.xlim=self.root.winfo_screenwidth()
        self.ylim=self.root.winfo_screenheight()

        self.main_canvas = tk.Canvas(self.root, bg="blue")
        self.main_canvas.pack(fill="both", expand=1)
        
        #self.main_canvas.create_rectangle(int(self.xlim/3), 0, 2*self.xlim//3, self.ylim, fill="#00cccc")
        """
        self.main_canvas.create_rectangle(int(self.xlim/3), int(4*self.ylim/5), 2*self.xlim//3, self.ylim, fill="black")

        self.b_start = tk.Button(self.main_canvas, text="Start", font="Arial 20", bg="orange")
        self.b_start.place(x=(2*self.xlim//3)-50, y=(4*self.ylim//5)+40, anchor="ne")
        """

        self.yrects = 6
        self.size_rect = self.ylim//15
        self.xrects=self.xlim//(3*self.size_rect) + 1
        self.grid_up = []
        self.grid_down=[]
        prevx = self.xlim//3; prevy=0
        for i in range(self.yrects):
            self.grid_up.append([])
            for j in range(self.xrects):
                area = self.main_canvas.create_rectangle(prevx, prevy, prevx+self.size_rect, prevy+self.size_rect, fill="yellow")
                prevx+=self.size_rect
                self.grid_up[-1].append([area, 0])
            prevy += self.size_rect
            prevx = self.xlim//3

        for i in range(self.yrects):
            self.grid_down.append([])
            for j in range(self.xrects):
                area = self.main_canvas.create_rectangle(prevx, prevy, prevx+self.size_rect, prevy+self.size_rect, fill="green")
                prevx+=self.size_rect
                self.grid_down[-1].append([area, 0])
            prevy += self.size_rect
            prevx = self.xlim//3

        self.main_canvas.create_rectangle(int(self.xlim/3), 2*self.yrects*self.size_rect, self.xlim//3 + self.xrects*self.size_rect, self.ylim, fill="black")

        self.b_start = tk.Button(self.main_canvas, text="Start", font="Arial 20", bg="orange", command=self.start_game)
        self.b_start.place(x=(2*self.xlim//3)-50, y=(4*self.ylim//5)+40, anchor="ne")

        self.lab_turn = tk.Label(self.main_canvas, text="", font="Arial 20", bg="black", fg="white")
        self.lab_turn.place(x=(self.xlim//3)+50, y=(4*self.ylim//5)+40, anchor="nw")

        self.shifs=[]
        self.computer_shifs=[]
        for i in range(4):
            shif = [0, i, 5-i, 0]
            self.shifs.append(shif)
            self.construct(i)

        self.active_shif = None
        self.started_game=False
        self.game_ended=False
        self.player_turn=None
        self.main_canvas.bind("<Button-1>", self.find_shif)
        self.main_canvas.bind("<ButtonRelease-1>", lambda event: self.initialize())
        self.main_canvas.bind("<B1-Motion>", self.move_shif)
        self.main_canvas.bind("<Button-3>", self.change_dir)

        self.make_com_shifs()
        
        self.root.mainloop()
    def start_game(self):
        if self.started_game or self.game_ended:
            return
        #self.computer_shifs()
        self.lab_turn["text"] = "Your turn"
        self.player_turn=True
        self.started_game=True
        self.active_shif=None
    def make_com_shifs(self):
        for length in range(2, 6):
            d = random.randrange(0, 2)
            possible_heads = []
            for i in range(self.yrects):
                for j in range(self.xrects):
                    if self.check_limits2(i, j, length, d):
                        possible_heads.append([i, j])
            ind = random.randrange(len(possible_heads))
            self.computer_shifs.append([possible_heads[ind][0], possible_heads[ind][1], length, d])
            self.construct2(length-2)
    def construct2(self, i):
        [y, x, length, d] = self.computer_shifs[i]
        if d==0:
            for k in range(y, y+length):
                #self.main_canvas.itemconfig(self.grid_up[k][x][0], fill="red")
                self.grid_up[k][x][1] = 1
        elif d==1:
            for k in range(x, x+length):
                #self.main_canvas.itemconfig(self.grid_up[y][k][0], fill="red")
                self.grid_up[y][k][1]=1
    def check_limits2(self, hi, hj, length, d):
        if d==0:
            if hi+length > self.yrects:
                return False
            for k in range(hi, hi+length):
                if self.grid_up[k][hj][1]:
                    return False
        elif d==1:
            if hj+length > self.xrects:
                return False
            for k in range(hj, hj+length):
                if self.grid_up[hi][k][1]:
                    return False
        return True
    def opt_cel(self):
        if self.game_ended:
            return
        unmarked=[]
        mx_prob=0
        for i in range(self.yrects):
            for j in range(self.xrects):
                if self.grid_down[i][j][1]<=1:
                    prob=0
                    di=[1,-1,0,0]
                    dj=[0,0,1,-1]
                    for k in range(4):
                        ni=i+di[k]
                        nj=j+dj[k]
                        if (ni in range(self.yrects)) and (nj in range(self.xrects)):
                            if self.grid_down[ni][nj][1]==2:
                                prob+=1
                    unmarked.append([[i, j], prob])
                    mx_prob=max(mx_prob, prob)
        optimals=[]
        for cell in unmarked:
            if cell[1]==mx_prob: optimals.append(cell[0])
        return random.sample(optimals, 1)[0]
    def computer_plays(self):
        if self.game_ended:
            return
        [y, x] = self.opt_cel()
        self.throw_bomb2(x, y)
    def throw_bomb2(self, x, y):
        if self.game_ended:
            return
        bomb = self.main_canvas.create_oval(self.xlim//3+x*self.size_rect, 0, self.xlim//3+(x+1)*self.size_rect, self.size_rect, fill="#404040")
        cx = self.xlim//3+x*self.size_rect; cy = 0
        for i in range(self.yrects+y):
            self.main_canvas.move(bomb, 0, self.size_rect)
            cy += self.size_rect
            self.main_canvas.update()
            self.main_canvas.after(40)
        self.main_canvas.after(100)
        self.main_canvas.delete(bomb)
        self.main_canvas.update()
        if self.grid_down[y][x][1] == 1:
            self.main_canvas.itemconfig(self.grid_down[y][x][0], fill="orange")
            self.grid_down[y][x][1] = 2
            self.complete_destroyed(y, x)
        else:
            self.grid_down[y][x][1]=3
    def complete_destroyed(self, i, j):
        if self.game_ended:
            return
        for shif in self.shifs:
            d=shif[3]
            hi, hj = shif[0], shif[1]
            if hi!=i and hj!=j:
                continue
            length = shif[2]
            if d==0:
                hit=True
                for k in range(hi, hi+length):
                    if self.grid_down[k][hj][1]!=2:
                        hit=False
                        break
                if hit==True:
                    self.main_canvas.itemconfig(self.grid_down[hi][hj][0], fill="#6666ff")
                    self.main_canvas.itemconfig(self.grid_down[hi][hj][0], width=5)
                    self.grid_down[hi][hj][1] = 4;
                    for k in range(hi+1, hi+length):
                        self.main_canvas.itemconfig(self.grid_down[k][hj][0], fill="red")
                        self.main_canvas.itemconfig(self.grid_down[k][hj][0], width=5)
                        self.grid_down[k][hj][1] = 4
            else:
                hit=True
                for k in range(hj, hj+length):
                    if self.grid_down[hi][k][1]!=2:
                        hit=False
                        break
                if hit==True:
                    self.main_canvas.itemconfig(self.grid_down[hi][hj][0], fill="#6666ff")
                    self.main_canvas.itemconfig(self.grid_down[hi][hj][0], width=5)
                    self.grid_down[hi][hj][1]=4
                    for k in range(hj+1, hj+length):
                        self.main_canvas.itemconfig(self.grid_down[hi][k][0], fill="red")
                        self.main_canvas.itemconfig(self.grid_down[hi][k][0], width=5)
                        self.grid_down[hi][k][1] = 4
            self.check_win(0)

    def throw_bomb(self, x, y):
        if self.game_ended:
            return
        bomb = self.main_canvas.create_oval(self.xlim//3+x*self.size_rect, (2*self.yrects-1)*self.size_rect, self.xlim//3+(x+1)*self.size_rect, 2*self.yrects*self.size_rect, fill="#404040")
        cx = self.xlim//3+x*self.size_rect; cy = (2*self.yrects-1)*self.size_rect
        for i in range(2*self.yrects-y-1):
            self.main_canvas.move(bomb, 0, -self.size_rect)
            cy -= self.size_rect
            self.main_canvas.update()
            self.main_canvas.after(40)
        self.main_canvas.delete(bomb)
        self.main_canvas.update()
        if self.grid_up[y][x][1] == 1:
            self.main_canvas.itemconfig(self.grid_up[y][x][0], fill="orange")
            self.grid_up[y][x][1] = 2
            self.complete_destroyed2(y, x)
        else:
            self.grid_up[y][x][1]=3
    def complete_destroyed2(self, i, j):
        if self.game_ended:
            return
        for shif in self.computer_shifs:
            d=shif[3]
            hi, hj = shif[0], shif[1]
            if hi!=i and hj!=j:
                continue
            length = shif[2]
            if d==0:
                hit=True
                for k in range(hi, hi+length):
                    if self.grid_up[k][hj][1]!=2:
                        hit=False
                        break
                if hit==True:
                    self.main_canvas.itemconfig(self.grid_up[hi][hj][0], fill="#6666ff")
                    self.main_canvas.itemconfig(self.grid_up[hi][hj][0], width=5)
                    self.grid_up[hi][hj][1]=4
                    for k in range(hi+1, hi+length):
                        self.main_canvas.itemconfig(self.grid_up[k][hj][0], fill="red")
                        self.main_canvas.itemconfig(self.grid_up[k][hj][0], width=5)
                        self.grid_up[k][hj][1]=4
            else:
                hit=True
                for k in range(hj, hj+length):
                    if self.grid_up[hi][k][1]!=2:
                        hit=False
                        break
                if hit==True:
                    self.main_canvas.itemconfig(self.grid_up[hi][hj][0], fill="#6666ff")
                    self.main_canvas.itemconfig(self.grid_up[hi][hj][0], width=5)
                    self.grid_up[hi][hj][1]=4
                    for k in range(hj+1, hj+length):
                        self.main_canvas.itemconfig(self.grid_up[hi][k][0], fill="red")
                        self.main_canvas.itemconfig(self.grid_up[hi][k][0], width=5)
                        self.grid_up[hi][k][1]=4
            self.check_win(1)
    def check_win(self, who):
        if self.game_ended:
            return
        if who==0:
            win=True
            for i in range(self.yrects):
                for j in range(self.xrects):
                    if self.grid_down[i][j][1]==1:
                        win=False
                        break
            if win:
                messagebox.showinfo("Game end", "Computer won!", parent=self.root)
                self.game_ended=True
        else:
            win=True
            for i in range(self.yrects):
                for j in range(self.xrects):
                    if self.grid_up[i][j][1]==1:
                        win=False
                        break
            if win:
                messagebox.showinfo("Game end", "Player won!", parent=self.root)
                self.game_ended=True
    def construct(self, i):
        if not self.check_limits(i):
            return False
        [y, x] = self.shifs[i][0:2]
        length = self.shifs[i][2]
        d = self.shifs[i][3]

        if d==0:
            for k in range(y, y+length):
                color = "gray"
                if k==y:
                    color = "pink"
                self.main_canvas.itemconfig(self.grid_down[k][x][0], fill=color)
                self.main_canvas.itemconfig(self.grid_down[k][x][0], width=5)
                self.grid_down[k][x][1] = 1
        elif d==1:
            for k in range(x, x+length):
                color = "gray"
                if k==x:
                    color = "pink"
                self.main_canvas.itemconfig(self.grid_down[y][k][0], fill=color)
                self.main_canvas.itemconfig(self.grid_down[y][k][0], width=5)
                self.grid_down[y][k][1] = 1
    def destruct(self, i):
        [y, x, length, d] = self.shifs[i]
        if d==1:
            for k in range(x, x+length):
                self.main_canvas.itemconfig(self.grid_down[y][k][0], fill="green")
                self.main_canvas.itemconfig(self.grid_down[y][k][0], width=1)
                self.grid_down[y][k][1] = 0
        elif d==0:
            for k in range(y, y+length):
                self.main_canvas.itemconfig(self.grid_down[k][x][0], fill="green")
                self.main_canvas.itemconfig(self.grid_down[k][x][0], width=1)
                self.grid_down[k][x][1] = 0
    def check_limits(self, i):
        [y, x] = [self.shifs[i][0], self.shifs[i][1]]
        if x >= self.xrects or y >= self.yrects:
            return False
        length = self.shifs[i][2]
        d = self.shifs[i][3]
        if d==0:
            if y+length-1 >= self.yrects:
                return False
            for k in range(y, y+length):
                if self.grid_down[k][x][1]: return False
        if d==1:
            if x+length-1 >= self.xrects:
                return False
            for k in range(x, x+length):
                if self.grid_down[y][k][1]: return False
        return True
    def find_coordinates(self, x, y):
        if x < self.xlim//3 or x >= self.xlim//3 + self.xrects*self.size_rect:
            return (-1, -1, -1)
        if y > 2*self.yrects*self.size_rect:
            return (-1, -1, -1)

        if y > self.size_rect*self.yrects:
            gridnum=1
            y -= self.size_rect*self.yrects
        else:
            gridnum=0
        x -= self.xlim//3
        i = y//self.size_rect; j = x//self.size_rect
        return (i,j,gridnum)
    def initialize(self):
        self.active_shif = None
    def find_shif(self, event):
        (i, j, gridnum) = self.find_coordinates(event.x, event.y)
        if self.started_game:
            if gridnum != 0 or not self.player_turn or self.game_ended:
                return
            #player's turn
            self.player_turn=False
            self.throw_bomb(j, i)
            self.main_canvas.update()
            if self.game_ended:
                self.root.destroy()
                game()
                return
            #computer's turn
            self.lab_turn["text"] = "Computer's turn"
            self.main_canvas.after(300)
            self.computer_plays()
            self.main_canvas.update()
            if self.game_ended:
                self.root.destroy()
                game()
                return
            #change into player's turn
            self.lab_turn["text"] = "Your turn"
            self.player_turn=True
            return
            
        if gridnum != 1:
            return

        shif = -1
        for k in range(4):
            if self.shifs[k][0:2] == [i, j]:
                shif=k
                break
        if shif==-1:
            return
        self.active_shif = shif
    def move_shif(self, event):
        if self.active_shif==None or self.started_game:
            return
        (ni,nj,g) = self.find_coordinates(event.x, event.y)
        if g < 1:
            return
        
        self.destruct(self.active_shif)
        [memohi, memohj] = self.shifs[self.active_shif][0:2]
        
        [self.shifs[self.active_shif][0], self.shifs[self.active_shif][1]] = [ni, nj]
        if self.check_limits(self.active_shif):
            self.construct(self.active_shif)
        else:
            [self.shifs[self.active_shif][0], self.shifs[self.active_shif][1]] = [memohi, memohj]
            self.construct(self.active_shif)
    def change_dir(self, event):
        if self.started_game:
            return
        (hi, hj, g) = self.find_coordinates(event.x, event.y)
        if g < 1:
            return

        shif = -1
        for k in range(4):
            if self.shifs[k][0:2] == [hi, hj]:
                shif = k;
                break
        
        if shif==-1:
            return
        self.destruct(shif)
        self.shifs[shif][3] = not self.shifs[shif][3]
        if self.check_limits(shif):
            self.construct(shif)
        else:
            self.shifs[shif][3] = not self.shifs[shif][3]
            self.construct(shif)
game()
