# igrik_pvp.py
# Igrik's World PvP — 2D shooter with jumping, endless respawns
#
# Run on two computers in the same LAN with Python 3.8+

import tkinter as tk
from tkinter import simpledialog, messagebox
import threading, socket, json, time

# === CONFIG ===
WIDTH, HEIGHT = 900, 600
FPS = 60
PLAYER_W, PLAYER_H = 60, 60
GROUND_Y = HEIGHT - 80

GRAVITY = 1600.0
JUMP_SPEED = 700.0
MOVE_SPEED = 250.0

FIREBALL_R = 8
FIREBALL_SPEED = 420
FIRE_COOLDOWN = 1.5

SERVER_PORT = 50007

# === CLIENT STATE ===
client_state_lock = threading.Lock()
client_state = {"players": {}, "fireballs": [], "you_id": None}

# === SERVER IMPLEMENTATION ===
class PvPServer(threading.Thread):
    def __init__(self, host_ip='', port=SERVER_PORT):
        super().__init__(daemon=True)
        self.host_ip = host_ip; self.port = port
        self.sock = None; self.clients = {}
        self.lock = threading.Lock(); self.running = False
        self.players = {}; self.fireballs = []
        self.next_player_id = 1; self.next_fire_id = 1

    def run(self):
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host_ip, self.port))
        self.sock.listen(4); self.sock.settimeout(0.5)
        threading.Thread(target=self.accept_loop, daemon=True).start()
        last = time.time()
        while self.running:
            now = time.time(); dt = now - last; last = now
            if dt > 0.1: dt = 0.1
            with self.lock:
                self.update_players(dt)
                self.update_fireballs(dt)
                self.broadcast_state()
            time.sleep(0.016)

    def accept_loop(self):
        while self.running:
            try:
                conn, addr = self.sock.accept()
                pid = str(self.next_player_id); self.next_player_id += 1
                self.clients[conn] = pid
                threading.Thread(target=self.client_handler, args=(conn, pid), daemon=True).start()
            except socket.timeout: continue

    def client_handler(self, conn, pid):
        f = conn.makefile(mode='r')
        try:
            join_msg = json.loads(f.readline().strip())
            name = join_msg.get("name", f"Player{pid}")
            color = join_msg.get("color", "green")
            spawn_x = 120 if pid=="1" else WIDTH-120
            self.players[pid] = {
                "id": pid, "x": spawn_x, "y": GROUND_Y-PLAYER_H/2,
                "vx":0,"vy":0,"name": name, "color": color,
                "lives": 3, "last_shot": 0, "on_ground": True,
                "input": {"left":False,"right":False,"jump":False,"shoot":None}
            }
            conn.sendall((json.dumps({"type":"assign","id":pid})+"\n").encode())
            while self.running:
                line = f.readline()
                if not line: break
                msg = json.loads(line.strip())
                if msg.get("type")=="input":
                    with self.lock:
                        if pid in self.players:
                            self.players[pid]["input"] = msg
        finally:
            if pid in self.players: del self.players[pid]
            if conn in self.clients: del self.clients[conn]
            conn.close()

    def update_players(self,dt):
        for p in self.players.values():
            inp=p["input"]
            # horizontal
            if inp["left"]: p["vx"]=-MOVE_SPEED
            elif inp["right"]: p["vx"]=MOVE_SPEED
            else: p["vx"]=0
            p["x"]+=p["vx"]*dt
            # gravity
            p["vy"]+=GRAVITY*dt
            p["y"]+=p["vy"]*dt
            # ground
            if p["y"]+PLAYER_H/2>=GROUND_Y:
                p["y"]=GROUND_Y-PLAYER_H/2
                p["vy"]=0; p["on_ground"]=True
            else: p["on_ground"]=False
            # jump
            if inp["jump"] and p["on_ground"]:
                p["vy"]=-JUMP_SPEED; p["on_ground"]=False
            # shoot
            if inp["shoot"] in ("left","right"):
                nowt=time.time()
                if nowt-p["last_shot"]>=FIRE_COOLDOWN:
                    p["last_shot"]=nowt
                    dirv=-1 if inp["shoot"]=="left" else 1
                    fb={"id":str(self.next_fire_id),"owner":p["id"],
                        "x":p["x"]+dirv*(PLAYER_W/2+10),"y":p["y"],
                        "vx":dirv*FIREBALL_SPEED}
                    self.next_fire_id+=1
                    self.fireballs.append(fb)

    def update_fireballs(self,dt):
        for fb in list(self.fireballs):
            fb["x"]+=fb["vx"]*dt
            for pid,p in self.players.items():
                if pid==fb["owner"]: continue
                if abs(fb["x"]-p["x"])<PLAYER_W/2+FIREBALL_R and abs(fb["y"]-p["y"])<PLAYER_H/2+FIREBALL_R:
                    p["lives"]-=1
                    # respawn
                    p["x"]=120 if pid=="1" else WIDTH-120
                    p["y"]=GROUND_Y-PLAYER_H/2
                    p["vx"]=p["vy"]=0
                    self.fireballs.remove(fb); break
            else:
                if fb["x"]<-50 or fb["x"]>WIDTH+50:
                    self.fireballs.remove(fb)

    def broadcast_state(self):
        state={"type":"state","players":list(self.players.values()),"fireballs":self.fireballs}
        s=json.dumps(state)+"\n"
        for c in list(self.clients):
            try:c.sendall(s.encode())
            except: pass

    def stop(self):
        self.running=False
        try:self.sock.close()
        except:pass

# === CLIENT ===
class PvPClient:
    def __init__(self, host,name,color,port=SERVER_PORT):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((host,port)); self.running=True
        self.sock.sendall((json.dumps({"name":name,"color":color})+"\n").encode())
        threading.Thread(target=self.recv_loop,daemon=True).start()

    def recv_loop(self):
        f=self.sock.makefile('r')
        while self.running:
            line=f.readline()
            if not line: break
            msg=json.loads(line.strip())
            if msg.get("type")=="assign":
                with client_state_lock: client_state["you_id"]=msg["id"]
            elif msg.get("type")=="state":
                with client_state_lock:
                    client_state["players"]={p["id"]:p for p in msg["players"]}
                    client_state["fireballs"]=msg.get("fireballs",[])

    def send_input(self,left,right,jump,shoot):
        if not self.running:return
        msg={"type":"input","left":left,"right":right,"jump":jump,"shoot":shoot}
        try:self.sock.sendall((json.dumps(msg)+"\n").encode())
        except:self.running=False

    def close(self):
        self.running=False
        try:self.sock.close()
        except:pass

# === DRAW IGRIK ===
def draw_igrik(canvas,x,y,w,h,color,name,lives):
    canvas.create_oval(x-w/2,y-h/2,x+w/2,y+h/2,fill=color,tags="actors")
    canvas.create_oval(x-w*0.2-6,y-h*0.2-6,x-w*0.2+6,y-h*0.2+6,fill="white",tags="actors")
    canvas.create_oval(x+w*0.2-6,y-h*0.2-6,x+w*0.2+6,y-h*0.2+6,fill="white",tags="actors")
    canvas.create_oval(x-w*0.2-2,y-h*0.2-2,x-w*0.2+2,y-h*0.2+2,fill="black",tags="actors")
    canvas.create_oval(x+w*0.2-2,y-h*0.2-2,x+w*0.2+2,y-h*0.2+2,fill="black",tags="actors")
    canvas.create_oval(x-w*0.25,y+h*0.1,x+w*0.25,y+h*0.3,fill="red",tags="actors")
    canvas.create_text(x,y-h/2-14,text=name,fill="black",tags="actors",font=("Helvetica",10,"bold"))
    canvas.create_text(x,y+h/2+14,text=f"Lives: {lives}",fill="black",tags="actors",font=("Helvetica",10))

# === APP ===
class PvPApp:
    def __init__(self,root):
        self.root=root; self.canvas=tk.Canvas(root,width=WIDTH,height=HEIGHT,bg="skyblue")
        self.canvas.pack()
        self.title=tk.Frame(root); tk.Button(self.title,text="Multiplayer",command=self.start).pack(padx=10,pady=10)
        self.title.place(relx=0.5,rely=0.5,anchor="center")
        self.client=None; self.server=None; self.running=False
        self.input_state={"left":False,"right":False,"jump":False,"shoot":None}
        root.bind("<KeyPress>",self.on_press); root.bind("<KeyRelease>",self.on_release)
        self.root.protocol("WM_DELETE_WINDOW",self.on_close)

    def start(self):
        name=simpledialog.askstring("Name","Your player name:") or "Player"
        color=simpledialog.askstring("Color","Igrik body colour:") or "green"
        ip=simpledialog.askstring("Multiplayer","Enter host IP (blank to host):")
        if not ip:
            self.server=PvPServer(); self.server.start(); time.sleep(0.2); ip="127.0.0.1"
        self.client=PvPClient(ip,name,color)
        self.title.place_forget()
        self.canvas.create_rectangle(0,GROUND_Y,WIDTH,HEIGHT,fill="green",tags="ground")
        if self.server:
            host_ip=socket.gethostbyname(socket.gethostname())
            self.canvas.create_text(WIDTH/2,20,text=f"Your IP: {host_ip}",fill="white",font=("Helvetica",12,"bold"),tags="actors")
        self.running=True; self.loop()

    def on_press(self,ev):
        if not self.client:return
        if ev.keysym.lower()=="a": self.input_state["left"]=True
        if ev.keysym.lower()=="d": self.input_state["right"]=True
        if ev.keysym=="space": self.input_state["jump"]=True
        if ev.keysym=="Left": self.input_state["shoot"]="left"
        if ev.keysym=="Right": self.input_state["shoot"]="right"
        self.send_input()

    def on_release(self,ev):
        if not self.client:return
        if ev.keysym.lower()=="a": self.input_state["left"]=False
        if ev.keysym.lower()=="d": self.input_state["right"]=False
        if ev.keysym=="space": self.input_state["jump"]=False
        if ev.keysym in ("Left","Right"): self.input_state["shoot"]=None
        self.send_input()

    def send_input(self):
        self.client.send_input(self.input_state["left"],self.input_state["right"],self.input_state["jump"],self.input_state["shoot"])

    def loop(self):
        if not self.running:return
        self.canvas.delete("actors")
        with client_state_lock:
            players=client_state["players"]; fbs=client_state["fireballs"]
        for p in players.values():
            draw_igrik(self.canvas,p["x"],p["y"],PLAYER_W,PLAYER_H,p["color"],p["name"],p["lives"])
        for fb in fbs:
            self.canvas.create_oval(fb["x"]-FIREBALL_R,fb["y"]-FIREBALL_R,
                                    fb["x"]+FIREBALL_R,fb["y"]+FIREBALL_R,fill="orange",tags="actors")
        self.root.after(int(1000/FPS),self.loop)

    def on_close(self):
        self.running=False
        if self.client:self.client.close()
        if self.server:self.server.stop()
        self.root.destroy()

# === MAIN ===
if __name__=="__main__":
    root=tk.Tk(); app=PvPApp(root); root.mainloop()
