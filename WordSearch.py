from termcolor import colored

dimensions = list(map(int,input("DIMENSIONS: ").split("x")))

grid = [list(input("ROW: ")) for i in range(dimensions[0])]




def print_grid(g,colored_spots = [],color = "red"):
    new_grid = []
    for y in range(len(g)):
        new_grid.append([])
        for x in range(len(g[y])):
            if [y,x] in colored_spots:
                new_grid[y].append([g[y][x],color])
            else:
                new_grid[y].append([g[y][x],0])
    for y in range(len(new_grid)):
        print_string = ""
        for x in range(len(new_grid[y])):
            if new_grid[y][x][1]==0:
                print_string+=new_grid[y][x][0]
            else:
                print_string+=colored(new_grid[y][x][0],color,attrs=["reverse"])
        print(print_string)
    return 1

def valid(g,x,y):
    if y>=0 and x>=0 and y<g[0] and x<g[1]:
        return True
    return False

def loop(g,x,y,word,d=-1):
    dim = [len(g),len(g[0])]
    x1 = x
    y1 = y
    if d==-1:
        answers = []
        x2 = x1-1
        y2 = y1-1
        for i in range(3):
            if valid(dim,x2,y2):
                if g[y2][x2]==word[0]:
                    answer = [y2,x2]+loop(g,x2,y2,word[1:],[x2-x1,y2-y1])
                    if -1 not in answer:
                        answers.append([y1,x1]+answer)
            x2+=1
        x2 = x1-1
        y2 = y1+1
        for i in range(3):
            if valid(dim,x2,y2):
                if g[y2][x2]==word[0]:
                    answer = [y2,x2]+loop(g,x2,y2,word[1:],[x2-x1,y2-y1])
                    if -1 not in answer:
                        answers.append([y1,x1]+answer)
            x2+=1
        x2 = x1-1
        y2 = y1
        for i in range(2):
            if valid(dim,x2,y2):
                if g[y2][x2]==word[0]:
                    answer = [y2,x2]+loop(g,x2,y2,word[1:],[x2-x1,y2-y1])
                    if -1 not in answer:
                        answers.append([y1,x1]+answer)
            x2+=2
        if answers == []:
            return -1
        else:
            answer2=[]
            for i in range(0,len(answers[0]),2):
                answer2.append([answers[0][i],answers[0][i+1]])
            return answer2

    else:
        if valid(dim,x1+d[0],y1+d[1]):
            if g[y1+d[1]][x1+d[0]]==word[0]:
                if len(word)!=1:
                    return [y1+d[1],x1+d[0]]+loop(g,x1+d[0],y1+d[1],word[1:],d)
                else:
                    return [y1+d[1],x1+d[0]]
            else:
                return [-1]
        else:
            return [-1]

def search(g,word):
    for y in range(len(g)):
        for x in range(len(g[y])):
            if g[y][x] == word[0]:
                answer = loop(g,x,y,word[1:])
                if answer!=-1:
                    return answer
    return -1

while True:
    query = input("WORD: ")
    answer = search(grid,query)
    if answer == -1:
        print(query + " not found. Please try another word")
    else:
        print_grid(grid,answer)

