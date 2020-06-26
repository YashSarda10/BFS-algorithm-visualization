import tkinter as tk


class Application:
    def __init__(self):
        self.ROW = 10
        self.COLUMN = 10
        self.MainBoard = []
        self.window = tk.Tk()
        self.window.title("DFS")
        self.window.configure(bg="black")
        self.window.resizable(0, 0)
        self.buttons = {}
        self.frame0 = tk.Frame(self.window, pady=10, bg='black')
        self.frame0.grid(row=0, column=0, sticky=tk.N)
        self.Slider1 = tk.Scale(self.frame0, sliderlength=60, width=25, fg="white", bg="gray10", label="ROW:", length=500, from_=7, to=14, orient="horizontal",
                                command=lambda x: self.initialise(x))
        self.Slider1.grid(row=0, column=0, sticky=tk.W)
        self.Slider2 = tk.Scale(self.frame0, sliderlength=60, width=25, fg="white", bg="gray10", label="COLUMN:", length=500, from_=7, to=22, orient="horizontal",
                                command=lambda x: self.initialise(x))
        self.Slider2.grid(row=0, column=1, sticky=tk.E)
        self.frame1 = tk.Frame(self.window, relief="sunken", bd=20)
        self.frame1.grid(row=1, column=0)
        self.frame2 = tk.Frame(self.window, bd=10, pady=10, bg='black')
        self.frame2.grid(row=2, column=0, sticky=tk.S)
        self.SearchBtn = tk.Button(self.frame2, text="Search", font=('Helvetica', '12'), bg="gray75", bd=5, command=lambda: self.SearchBtnHandler())
        self.SearchBtn.grid(row=0, column=4)
        self.ResetBtn = tk.Button(self.frame2, text="RESET", font=('Helvetica', '12'), bg="gray75", bd=5, command=lambda: self.ResetBtnHandler())
        self.ResetBtn.grid(row=0, column=0)
        self.EntryBtn = tk.Button(self.frame2, text="Entry Cell", font=('Helvetica', '12'), bg="gray75", bd=5, command=lambda: self.EntryBtnHandler())
        self.EntryBtn.grid(row=0, column=1)
        self.ExitBtn = tk.Button(self.frame2, text="Exit Cell", font=('Helvetica', '12'), bg="gray75", bd=5, command=lambda: self.ExitBtnHandler())
        self.ExitBtn.grid(row=0, column=3)
        self.WallBtn = tk.Button(self.frame2, text="Wall Cell", font=('Helvetica', '12'), bg="gray75", bd=5, command=lambda: self.WallBtnHandler())
        self.WallBtn.grid(row=0, column=2)
        self.NextBtn = tk.Button(self.frame2, text="NEXT", font=('Helvetica', '12'), state="disabled", bg="gray75", bd=5, command=lambda: self.NextBtnHandler())
        self.NextBtn.grid(row=0, column=5)
        self.tracker = {}
        self.solution = []

    def NextBtnHandler(self):
        # this button displays steps of DFS and path
        if len(self.solution) != 0:
            generation = self.solution[0]
            for item in generation:
                i, j = item
                self.MainBoard[i][j] = "-"
            self.solution.pop(0)
            self.updateBoard()
        else:
            var = self.tracker[(-1, -1)]
            i, j = var
            if self.MainBoard[i][j] == "E":
                self.ResetBtn.config(state="normal")
                return
            self.MainBoard[i][j] = "r"
            self.tracker[(-1, -1)] = self.tracker[(i, j)]
            self.updateBoard()

    def SearchBtnHandler(self):
        entryVar = 0
        exitVar = 0
        # check if only one exit point and only one entry point exists
        for i in range(self.ROW):
            for j in range(self.COLUMN):
                if self.MainBoard[i][j] == "E":
                    entryVar += 1
                if self.MainBoard[i][j] == "X":
                    exitVar += 1
        if entryVar != 1 or exitVar != 1:
            return
        self.ExitBtn.config(state="disabled")
        self.EntryBtn.config(state="disabled")
        self.WallBtn.config(state="disabled")
        self.ResetBtn.config(state="disabled")
        self.SearchBtn.config(state="disabled")
        self.NextBtn.config(state="normal")
        self.updateBoard()
        self.solve()

    def markCells(self, val):
        ans = []
        i = val[0]
        j = val[1]
        if i + 1 <= self.ROW - 1:
            if self.MainBoard[i + 1][j] == "X":
                self.tracker[(-1, -1)] = val
                return []
            if self.MainBoard[i + 1][j] == " ":
                self.MainBoard[i + 1][j] = "*"
                self.tracker[(i + 1, j)] = val
                ans.append((i + 1, j))

        if i - 1 >= 0:
            if self.MainBoard[i - 1][j] == "X":
                self.tracker[(-1, -1)] = val
                return []
            if self.MainBoard[i - 1][j] == " ":
                self.MainBoard[i - 1][j] = "*"
                self.tracker[(i - 1, j)] = val
                ans.append((i - 1, j))

        if j + 1 <= self.COLUMN - 1:
            if self.MainBoard[i][j + 1] == "X":
                self.tracker[(-1, -1)] = val
                return []
            if self.MainBoard[i][j + 1] == " ":
                self.MainBoard[i][j + 1] = "*"
                self.tracker[(i, j + 1)] = val
                ans.append((i, j + 1))

        if j - 1 >= 0:
            if self.MainBoard[i][j - 1] == "X":
                self.tracker[(-1, -1)] = val
                return []
            if self.MainBoard[i][j - 1] == " ":
                self.MainBoard[i][j - 1] = "*"
                self.tracker[(i, j - 1)] = val
                ans.append((i, j - 1))
        return ans

    def solve(self):
        ans = []
        for i in range(self.ROW):
            for j in range(self.COLUMN):
                if self.MainBoard[i][j] == "E":
                    ans = [(i, j)]
                    break
        # ans contains co-ordinates of Entry Point
        # generation variable is list of all boxes checked in current step of BFS
        generation = ans
        # following while loop calculates next generations
        while len(generation) != 0:
            temp = []
            for item in generation:
                temp += self.markCells(item)
            generation = temp
            self.solution.append(generation)                # store this entire step for future
            if (-1, -1) in self.tracker:                    # (-1,-1) represents Exit point; if found, then break the loop
                break
        # if (-1,-1) = Exit point doesn't exist
        if (-1, -1) not in self.tracker:
            lbl = tk.Label(self.window, text="NO PATH FOUND", bg="black", fg="white", pady=180, font=('Helvetica', '30'))
            lbl.grid(row=1, column=0, sticky=tk.N)
            self.ResetBtn.destroy()
            self.ExitBtn.destroy()
            self.EntryBtn.destroy()
            self.WallBtn.destroy()
            self.SearchBtn.destroy()
            self.NextBtn.destroy()
            self.Slider2.destroy()
            self.Slider1.destroy()

    def EntryBtnHandler(self):
        self.ExitBtn.config(state="normal")
        self.EntryBtn.config(state="disabled")
        self.WallBtn.config(state="normal")

    def ExitBtnHandler(self):
        self.ExitBtn.config(state="disabled")
        self.EntryBtn.config(state="normal")
        self.WallBtn.config(state="normal")

    def WallBtnHandler(self):
        self.ExitBtn.config(state="normal")
        self.EntryBtn.config(state="normal")
        self.WallBtn.config(state="disabled")

    def ResetBtnHandler(self):
        self.ExitBtn.config(state="normal")
        self.EntryBtn.config(state="normal")
        self.WallBtn.config(state="normal")
        self.SearchBtn.config(state="normal")
        self.NextBtn.config(state="disabled")
        self.tracker = {}
        self.solution = []
        self.initialise(0)
        self.updateBoard()

    def initialise(self, num):
        self.buttons = {}
        self.MainBoard = []
        self.frame1.destroy()
        self.frame1 = tk.Frame(self.window, relief="sunken", bd=20)
        self.frame1.grid(row=1, column=0)
        self.ROW = self.Slider1.get()
        self.COLUMN = self.Slider2.get()
        for i in range(self.ROW):
            self.MainBoard.append([" " for i in range(self.COLUMN)])
            for j in range(self.COLUMN):
                self.buttons[str(i) + str(j)] = tk.Button(self.frame1, text=" ", bg="gray95", relief="raised", width=4, height=2, command=lambda a=i, b=j: self.createBoard(a, b))
                self.buttons[str(i) + str(j)].grid(row=i, column=j)

    def createBoard(self, i, j):                                     # creates or updates self.MainBoard
        if self.SearchBtn["state"] == "normal":
            if self.EntryBtn["state"] == "disabled":
                for x in range(self.ROW):
                    for y in range(self.COLUMN):
                        if self.MainBoard[x][y] == "E":
                            self.MainBoard[x][y] = " "
                self.MainBoard[i][j] = "E"
            if self.ExitBtn["state"] == "disabled":
                for x in range(self.ROW):
                    for y in range(self.COLUMN):
                        if self.MainBoard[x][y] == "X":
                            self.MainBoard[x][y] = " "
                self.MainBoard[i][j] = "X"
            if self.WallBtn["state"] == "disabled":
                if self.MainBoard[i][j] == "#":
                    self.MainBoard[i][j] = " "
                elif self.MainBoard[i][j] == " ":
                    self.MainBoard[i][j] = "#"
                else:
                    pass
        self.updateBoard()

    def updateBoard(self):
        for i in range(self.ROW):
            for j in range(self.COLUMN):
                if self.MainBoard[i][j] == "E":                                       # entry point
                    self.buttons[str(i) + str(j)].configure(bg="green")
                if self.MainBoard[i][j] == "X":                                       # exit point
                    self.buttons[str(i) + str(j)].configure(bg="blue")
                if self.MainBoard[i][j] == "#":                                       # wall
                    self.buttons[str(i) + str(j)].configure(bg="brown4")
                if self.MainBoard[i][j] == " " or self.MainBoard[i][j] == "*":        # void space
                    self.buttons[str(i) + str(j)].configure(bg="grey95")
                if self.MainBoard[i][j] == "-":                                       # path
                    self.buttons[str(i) + str(j)].configure(bg="grey45")
                if self.MainBoard[i][j] == "r":                                       # Checked positions
                    self.buttons[str(i) + str(j)].configure(bg="gold")

    def Mainloop(self):
        self.initialise(0)
        self.window.mainloop()


i = Application()
i.Mainloop()
