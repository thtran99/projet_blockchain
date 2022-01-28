#!/usr/bin/env python
# coding: utf-8
# %%
import socket, threading, sys, time
miners = {}
wallers = {}
miner_name = ""


# %%
def remove_connection(nick_name):
    if nick_name in miners.keys():
        miners[nick_name].close()
        miners.pop(nick_name)
        print("Miner", nick_name, "is removed")
        print("List:", miners.keys())
        send_list_miner()
        
    if nick_name in wallers.keys():
        wallers[nick_name].close()
        wallers.pop(nick_name)
        print("Waller", nick_name, "is removed")


# %%
def send_list_miner():
    for w in wallers.keys():
        wallers[w].send(" ".join(list(miners.keys())).encode())


# %%
def handle_waller_connection(nick_name, conn):
    while True:
        try:
            msg = conn.recv(1024)
            if msg:
                print(nick_name, ":", msg)
                for m in miners.keys():
                    miners[m].send(msg)
                    
            else:
                raise Exception("Waller " + nick_name + " is closed")
                    
        except Exception as e:
            print('Error to handle waller connection:', e)
            remove_connection(nick_name)
            break


# %%
def handle_miner_connection(nick_name, miner_nb):
    while True:
        try:
            msg = miner_nb.recv(1024).decode()
            if msg:
                print(nick_name, ":", msg)
                msg_split = msg.split("-")
                
                # It's a require to connect with new miner
                if msg_split[0] == "MINER":
                    connect_to_neighbor(msg_split[1])
            
            ## miner closed
            else:
                raise Exception("Miner " + nick_name + " is closed")
                
        except Exception as e:
            print('Error to handle miner connection:', e)
            remove_connection(nick_name)
            break


# %%
def connect_to_neighbor(m):
    global miner_name
    if m not in miners.keys():
        try:
            miner_nb = socket.socket()
            miner_nb.connect(('localhost', int(m)))
            miners[m] = miner_nb

            miner_nb.send(("MINER-" + miner_name).encode())
            print('Connected to', m)

            threading.Thread(target=handle_miner_connection, args=[m, miner_nb]).start()

        except Exception as e: 
            print('Error connecting to neighbor:', e)
            remove_connection(m)
    else:
        print(miner_name, "is already connected with", m)

    print("List:", miners.keys())


# %%
def miner():
    global miner_name
    try:
        miner_name = sys.argv[1]
        miner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        miner.bind(('localhost', int(miner_name)))
        miner.listen(100)
        
        if len(sys.argv) == 3:
            connect_to_neighbor(sys.argv[2])

        print('Miner', miner_name, 'is running!')
        
        while True:
            conn, addr = miner.accept()
            
            msg = conn.recv(1024).decode()
            msg_split = msg.split("-")
            
            ## new connect is a MINER
            if msg_split[0] == 'MINER':
                nick_name = msg_split[1]
                
                if nick_name not in miners.keys():
                    # demand new miner connect with neighbors
                    for name in miners.keys():
                        conn.send(("MINER-" + name).encode())
                        # avoid receive multi mess in same time (ex of error: MINER-8000MINER-8001)
                        time.sleep(1) 
                
                    miners[nick_name] = conn
                    threading.Thread(target=handle_miner_connection, args=[nick_name, conn]).start()
                    print("Miner", nick_name, "is connected")
                    print("List:", miners.keys())
                    
                    # send list miner to waller
                    send_list_miner()
                    
            ## new connect is WALLER
            else:
                nick_name = msg
                
                if nick_name not in wallers.keys():
                    wallers[nick_name] = conn
                    threading.Thread(target=handle_waller_connection, args=[nick_name, conn]).start()
                    print('Welcome', nick_name, 'to miner', miner_name)
                    
                    #send_list_miner()
                    conn.send(" ".join(list(miners.keys())).encode())
            
    except Exception as e:
        print('An error has occurred when instancing socket:', e)
        miner.close()
        return


# %%
miner()

