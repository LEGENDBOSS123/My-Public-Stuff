#SERVER
import socket
import threading
import random
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#port = int(input("PORT: "))
port = 4000
serv_sock.bind(("", port))

serv_sock.listen(1)

clients_joined = []
games = []
player = 0



maps = ["W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W",
        "W","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","W",
        "W","G","G","G","G","G","B","B","G","G","5","G","B","B","G","G","G","G","G","W",
        "W","G","G","0","G","W","B","B","G","G","G","G","B","B","W","G","3","G","G","W",
        "W","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","W",
        "W","G","G","G","G","W","G","G","G","G","G","G","G","G","W","G","G","G","G","W",
        "W","G","G","G","G","G","G","G","B","B","B","B","B","G","G","G","G","G","G","W",
        "W","G","G","G","G","W","G","G","B","W","W","W","B","G","W","G","G","G","G","W",
        "W","G","G","G","G","G","G","G","B","G","G","G","B","G","G","G","G","G","G","W",
        "W","G","G","G","G","G","G","G","B","W","4","W","B","G","G","G","G","G","G","W",
        "W","G","G","G","G","G","G","G","B","G","G","G","B","G","G","G","G","G","G","W",
        "W","G","G","G","G","G","G","G","B","W","W","W","B","G","G","G","G","G","G","W",
        "W","G","G","G","G","W","G","G","B","B","B","B","B","G","W","G","G","G","G","W",
        "W","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","W",
        "W","G","G","G","G","W","G","G","G","G","G","G","G","G","W","G","G","G","G","W",
        "W","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","W",
        "W","G","G","1","G","W","B","B","G","G","G","G","B","B","W","G","2","G","G","W",
        "W","G","G","G","G","G","B","B","G","G","6","G","B","B","G","G","G","G","G","W",
        "W","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","W",
        "W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W"]


def ENCODE(lis):
    ret = ""
    for i in lis:
        ret2 = ""
        for o in i:
            ret2+=","+str(o)+","
        
        ret+=" "+ret2+" "
    return ret

def DECODE(string):
    ret = string.split()
    for i in range(len(ret)):
        ret[i] = ret[i].split(',')
        
        
        
            
                
        while '' in ret[i]:
            ret[i].remove("")

        for a in range(len(ret[i])):
            if ret[i][a][0]=="-":
                if ret[i][a][1:].isdigit():
                    ret[i][a] = int(ret[i][a])
            elif ret[i][a].isdigit():
                    ret[i][a] = int(ret[i][a])
    return ret

def on_new_client(client_sock,player):
    global clients_joined
    global games
    global maps
    connected = True
    ingame = False
    gameindex = None
    while connected:
        if gameindex!=None:
            g = games[gameindex][0]
        reply = [[1]]
        
        data = DECODE(client_sock.recv(2048).decode())
        
        
        if not data:
            connected = False
            break
        if data[0][0]==3:
            data[2]+=[player]
            
        clients_joined[player] = data

        
        if data[0][0] == 2:
            if ingame == False:
                for i in range(len(games)):
                    if games[i][0]==2 and games[i][1]==data[1][0] and len(games[i])-2<games[i][1]:
                        ingame = True
                        games[i].append(player)
                        gameindex = i
            if ingame == False:
                ingame = True
                
                games.append([2,data[1][0],player])
                gameindex = games.index([2,data[1][0],player])
        if data[0][0]==1:
            ingame = False
            if gameindex!=None:
                con = True
                if len(games[gameindex])==3:
                        games[gameindex] = [0,0]
                        gameindex = None
                        con = False
                if con == True:
                    for i in range(len(games[gameindex])):
                        
                        if i>1 and games[gameindex][i]==player:
                            games[gameindex].pop(i)
                            gameindex = None
                            break
        if gameindex!=None:
            if games[gameindex][2] == player and games[gameindex][1]==len(games[gameindex])-2:
                games[gameindex][0] = 3
                
            if games[gameindex][0]==3 and g!=3:
                reply = [[3]]
                loc = [0,0]
                for i in range(len(games[gameindex])):
                    if i>1 and games[gameindex][i]==player:
                        loc[0] = maps.index(str(i-2))%20*100+50
                        loc[1] = int(maps.index(str(i-2))/20)*100+50
                        
                reply = [[3],loc,maps]
                
            elif games[gameindex][0]==3:
                
                reply = [[3],["ID",player]]
                for i in range(len(games[gameindex])):
                    if i>1 and games[gameindex][i]!=player and len(clients_joined[games[gameindex][i]])>2:
                
                                                
                        for e in clients_joined[games[gameindex][i]][2:][:]:
                                
                            if e[0]!="HIT":
                                reply.append(e)
                            
                            elif e[0]=="HIT" and e[1]==player:
                                reply.append(e)
                                clients_joined[games[gameindex][i]].remove(e)
                            
            
                
                if len(games[gameindex]) == 3:
                    reply = [[3],["WON"]]
                                
                
            if games[gameindex][0]==2 and data[0][0]==2:
                reply = [[2],[len(games[gameindex])-2,games[gameindex][1]]]
                
            

        
        client_sock.sendall(ENCODE(reply).encode())
    client_sock.close()
    

while True:
    client_sock, client_addr = serv_sock.accept()
    clients_joined.append(None)
    ConnectionThread = threading.Thread(target = on_new_client,args = (client_sock,player))
    ConnectionThread.start()
    
    player+=1
serv_sock.close()




