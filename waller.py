#!/usr/bin/env python
# coding: utf-8
# %%
import socket, threading, sys
miners = []
nick_name = ""


# %%
def handle_messages(miner_name, miner):
    global miners
    while True:
        try:
            msg = miner.recv(1024)
            if msg:
                miners = msg.decode().split()
                print("List of miners:", miners)
                
            else:
                print("Miner", miner_name, "closed")
                miner.close()

                if len(miners) > 0:
                    print("Connecting to new miner...")
                    connect_miner(int(miners.pop(0)))
                else:
                    print("No available miner found")
                    
        except Exception as e:
            print('Error handling message from miner:', e)
            miner.close()
            break


# %%
def connect_miner(miner_name):
    global nick_name
    
    try:
        miner = socket.socket()
        miner.connect(('localhost', miner_name))

        miner.send(nick_name.encode())
        print('Connected to miner', miner_name)

        threading.Thread(target=handle_messages, args=[miner_name, miner]).start()

        while True:
            msg = input()
            miner.send(msg.encode())
            
    except Exception as e:
        print('Error connecting to miner socket:', e)
        return


# %%
def waller():
    global nick_name
    nick_name = sys.argv[1]
    miner_name = int(sys.argv[2])
    connect_miner(miner_name)


# %%
waller()

