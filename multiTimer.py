# -*- coding: utf-8 -*-

import csv
import pandas as pd
import tkinter as tk 
from tkinter import ttk
from pathlib import Path
from tkinter import filedialog as fd
from datetime import datetime
from tkinter.messagebox import showinfo


class Tache ():
    def __init__(self, th1=None, t=None, x=None, y=None, h=None, m=None, s=None,entrys=None):
        self.s = s
        self.m = m
        self.h = h
        self.th1 = th1
        self.t = t
        self.x = x
        self.y = y
        self.entrys= entrys
    
    def arret_general(self):
        global encore
        encore=False
        self.lancer() 
        
    def arret(self):
        self.entrys[self.x][self.y].after_cancel(self.th1[self.x][self.y])           
        
    def setSeconde(self):
        if self.s[self.x][self.y]==59 and self.m[self.x][self.y]<59:
            self.s[self.x][self.y]=0
            self.m[self.x][self.y]+=1
        elif self.s[self.x][self.y]==59 and self.m[self.x][self.y]==59:
            self.s[self.x][self.y]=0
            self.m[self.x][self.y]=0
            self.h[self.x][self.y]+=1
        else:
            self.s[self.x][self.y]+=1
        
        self.t[self.x][self.y].set("%02d:%02d:%02d" %(self.h[self.x][self.y],self.m[self.x][self.y],self.s[self.x][self.y]))
       
    def lancer(self):

        if encore:
            self.setSeconde()
            self.th1[self.x][self.y]=self.entrys[self.x][self.y].after(1000,lambda: self.lancer())
        else:
            if self.th1[self.x][self.y]:
                self.entrys[self.x][self.y].after_cancel(self.th1[self.x][self.y])          
        
    def demarrer(self):

        global encore
        encore=True
        self.lancer()
              
    def reset(self):        
        self.s[self.x][self.y] = 0
        self.m[self.x][self.y] = 0
        self.h[self.x][self.y] = 0
        self.t[self.x][self.y].set("00:00:00")
        
        
class Hello_IHM(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.entry=[]
        self.entryM=[]
        self.lcarte=[]
        self.lk = []
        self.lll=[]
        self.llc=[]
        self.c=[]
        self.ls_Pre=[]
        self.lc_Pre=[]
        self.tpre=[]
        self.tache_Pre=[]
        self.frames=[]
        self.Bt_Envoi=[]
        self.ltext_Pre=[]
        self.timer_Pre=[]
        self.h_Pre=[]
        self.m_Pre=[]
        self.s_Pre=[]
        self.entrys_Pre=[]
        self.buttons_Pre=[]
        self.buttons_reset_Pre=[]
        self.lBtClick_Envoi=[]
        self.directory = Path(__file__).parent
        self.k=0
        self.lp=0
        self.col=0
        self.bcr=0
        
        self.geometry('1000x500')
        
        self.title("IHM")
        self.config(bg = "white") 
        self.Ptopframe1 = tk.Frame(self)
        self.Ptopframe1.pack(side = "top", fill='both')
        self.Ptopframe2 = tk.Frame(self)
        self.Ptopframe2.pack(side = "top", fill='both')
        self.Pbottomframe = tk.Frame(self)
        self.Pbottomframe.pack(side = "top", fill='both', expand = True)
        
        self.frame_canvas = tk.Frame(self.Pbottomframe)
        self.frame_canvas.grid(row= 1, column=0, pady=(5, 0), sticky='nwse')
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)
        # flexibilité en ligne et colonne
        self.frame_canvas.grid_propagate(False)
        
        # ajouter canvas (forme) dans frame
        self.canvas = tk.Canvas(self.frame_canvas, bg="black")
        self.canvas.grid(row=0, column=0, sticky="nwse")
        
        # barre déroulante verticale et horizontale
        self.vsb = tk.Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)
        
        self.hsb = tk.Scrollbar(self.frame_canvas, orient="horizontal", command=self.canvas.xview)
        self.hsb.grid(row=1, column=0, sticky='we')
        self.canvas.configure(xscrollcommand=self.hsb.set)
        
        self.frame_buttons = tk.Frame(self.canvas, bg="black")
        self.canvas.create_window((0, 0), window=self.frame_buttons, anchor='nw')
        
        try:
            open(r'{}\test.csv'.format(self.directory), 'r')
            
            dataframe = pd.read_csv(r'{}\test.csv'.format(self.directory), sep=',', header=0, index_col=None)
            list1 = dataframe.to_dict('records')
            self.dict1 = list1[-1]
            for cle, val in self.dict1.items():
                self.dict1[cle] = eval(val.strip())
                
        except FileNotFoundError:
            #print("Désolé, le fichier n'existe pas.")
            self.dict1 = {'indexx':[0],
                          'Nom_du_mecano':[0],
                          'P':[0],
                          'S':[0],
                          'E':[0],
                          'U':[0],
                          'O':[0],
                          'A':[0],
                          'BO':[0],
                          'LT':[0],
                          'Quoi':[0]}
            self.csv(self.dict1)
                
        self.BTOngletRecap = tk.Button (self.Ptopframe1, text = "Recap.", command= lambda: self.command_lancer_arreter_recap())
        self.BTOngletRecap.clicked = False
        self.BTOngletRecap.pack(side="right",fill='x', expand=1)
        
        tk.Button (self.Ptopframe2, text = "Add Timer", command= lambda: self.visible(self.frame_buttons)).pack(expand=1,fill='x')
        
                    
        self.bt_stop = tk.Button (self.Ptopframe1, text = "Stop Timers",state=tk.DISABLED, command = lambda: self.command_lancer_arreter(self.bt_stop))
        
        self.bt_stop.pack(side="left",fill='x', expand=1)
        
        self.bt_stop.clicked = False
        self.update() 
     
    def command_lancer_arreter_recap(self):
        self.bcr+=1
        if self.bcr % 2 != 0:
            self.onglet_recapitulatif()
        else:
            self.root2.destroy()
        
        return self.BTOngletRecap.clicked == True
        
    def stop_all_threads(self):
        for x in range(self.lp):
            for y in range(self.col):
                self.tache_Pre[x][y] = Tache(self.timer_Pre, self.ltext_Pre, x, y, self.h_Pre, self.m_Pre, self.s_Pre,self.entrys_Pre).arret_general()
                self.tache_Pre[x][y]
                
    def csv(self,dic):
        with open(r'{}\test.csv'.format(self.directory), 'w', encoding="utf-8") as f :
            writer = csv.writer(f)
            writer.writerow(dic.keys())
            writer.writerow(dic.values())
            
        self.df = pd.read_csv(r'{}\test.csv'.format(self.directory), sep=',')
        
        
    def visible(self, fm):

        # Création du frame contenant les éléments

        self.col+=1
        
        def lappend(ltext,timer,h,m,s,entrys,buttons,lc,buttons_reset):
            ltext.append(list())
            timer.append(list())
            h.append(list())
            m.append(list())
            s.append(list())
            entrys.append(list())
            buttons.append(list())
            lc.append(list())
            buttons_reset.append(list())
            
            
        if self.col>5 or self.lp==0 :
            self.lp+=1
            self.col=1
            self.frames.append(list())
            self.Bt_Envoi.append(list())
            self.entry.append(list())
            self.lcarte.append(list())
            self.lk.append(list())
            self.tache_Pre.append(list())
            self.entryM.append(list())
            self.lBtClick_Envoi.append(list())
            self.tpre.append(list())
            
            lappend(self.ltext_Pre, self.timer_Pre, self.h_Pre, self.m_Pre, self.s_Pre, self.entrys_Pre, self.buttons_Pre, self.lc_Pre, self.buttons_reset_Pre)

        def lappendv(ltext,timerr,h,m,s,entrys,buttons,lc,buttons_reset):
            ltext[-1].append(tk.StringVar(self.frame_buttons,"00:00:00"))
            timerr[-1].append(0)
            h[-1].append(0)
            m[-1].append(0)
            s[-1].append(0)
            entrys[-1].append(tk.Entry(self.frame_buttons))
            buttons[-1].append(tk.Button(self.frame_buttons))
            lc[-1].append(0)
            buttons_reset[-1].append(tk.Button(self.frame_buttons))
        
        self.tache_Pre[-1].append(0)
        self.lk[-1].append(self.k)
        self.frames[-1].append(tk.Canvas(self.frame_buttons, bg="white"))
        self.Bt_Envoi[-1].append(tk.Button(self.frame_buttons))
        self.lcarte[-1].append(tk.StringVar(self.frame_buttons,"NameOfStudent"))
        self.entry[-1].append(tk.Entry(self.frame_buttons))
        self.entryM[-1].append(tk.Entry(self.frame_buttons))
        self.lBtClick_Envoi[-1].append(False)
        self.tpre[-1].append(0)

        lappendv(self.ltext_Pre, self.timer_Pre, self.h_Pre, self.m_Pre, self.s_Pre, self.entrys_Pre, self.buttons_Pre, self.lc_Pre, self.buttons_reset_Pre)

        l = self.lp-1
        self.lll.append(l)
        c = self.col-1
        self.llc.append(c)
        self.k+=1
        
        self.frames[l][c] = tk.Canvas(fm, bg="white")
        
        self.topframe = tk.Frame(self.frames[l][c], bg="white")
        self.topframe.pack(side = "top")
        self.leftframe1 = tk.Frame(self.frames[l][c], bg="white")
        self.leftframe1.pack(side = "top")
        self.leftframe2 = tk.Frame(self.frames[l][c], bg="white")
        self.leftframe2.pack(side = "top")
        self.leftframe3 = tk.Frame(self.frames[l][c], bg="white")
        self.leftframe3.pack(side = "top")
        self.bottomframe = tk.Frame(self.frames[l][c], bg="white")
        self.bottomframe.pack(side = "bottom")
        
        tk.Label(self.topframe, text='Timer'+ str(self.k), bg = "white").pack(side="top")
        self.entry[l][c] = tk.Entry(self.topframe, textvariable = self.lcarte[l][c])
        self.entry[l][c].pack(side="bottom")
        
        tk.Label(self.leftframe1,text="Tim : ", bg = "white").pack(side="left") 

        self.creation_widgets(self.leftframe1, l, c, self.ltext_Pre, self.timer_Pre, self.h_Pre, self.m_Pre, self.s_Pre, self.entrys_Pre, self.buttons_Pre, self.lc_Pre, self.buttons_reset_Pre)

        def archive():

            if not self.lBtClick_Envoi[l][c]:
                self.Bt_Envoi[l][c].config(state=tk.DISABLED)
                datafr = pd.read_csv(r'{}\test.csv'.format(self.directory), sep=',', header=0, index_col=None)
                list1 = datafr.to_dict('records')
                self.dict1 = list1[-1]
                for cle, val in self.dict1.items():
                    self.dict1[cle] = eval(val.strip())

                self.dict1['indexx'].append(int(self.dict1['indexx'][-1])+1)
                self.dict1['Nom_du_mecano'].append(self.entryM[l][c].get())
                self.dict1['P'].append(self.ltext_Pre[l][c].get())
                self.dict1['S'].append(self.ltext_Proc[l][c].get())
                self.dict1['E'].append(0)
                self.dict1['U'].append(0)
                self.dict1['O'].append(0)
                self.dict1['A'].append(self.ltext_Admi[l][c].get())
                self.dict1['BO'].append(0)
                self.dict1['LT'].append(0)
                self.dict1['Quoi'].append(self.entry[l][c].get())
                
                self.csv(self.dict1)
                return self.lBtClick_Envoi[l][c]==True
        
        self.entryM[l][c] = tk.Entry(self.bottomframe, textvariable = tk.StringVar(self.bottomframe,"Comment"))
        self.lBtClick_Envoi[l][c]
        self.Bt_Envoi[l][c]=tk.Button(self.bottomframe, text='Commit time', command= lambda:[archive(),self.frames[l][c].destroy()])
        self.Bt_Envoi[l][c].pack(side="bottom")
        
        self.entryM[l][c].pack(side="bottom")
            
        self.frames[l][c].grid(row=l, column=c, padx=5, pady=5)

        # MAJ taille des élements dans frame
        self.frame_buttons.update_idletasks()
         # Redim le canvas pour montrer exactement 5x3 avec le scrollbar
        self.firstcolumns_width = sum([self.frames[l][c].winfo_width() for j in range(0, 5)])
        self.firstrows_height = sum([self.frames[l][c].winfo_height() for i in range(0, self.lp)])
        self.frame_canvas.config(width=self.firstcolumns_width + self.vsb.winfo_width(), height=self.firstrows_height)
        
        # Mise au point sur canvas avec region déroulée
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
        self.frame_canvas.pack(side="left",fill ='x', expand=1)
        
    def command_lancer_arreter(self, buttons, timer=None, ltext=None, x=None, y=None, h=None, m=None, s=None):
        if id(buttons) == id(self.bt_stop):
            if not buttons.clicked:
                self.bt_stop.config(state=tk.DISABLED)
                    
                for x in range(self.lp):
                    for y in range(self.col):
                        
                        self.tache_Pre[x][y] = Tache(self.timer_Pre, self.ltext_Pre, x, y, self.h_Pre, self.m_Pre, self.s_Pre,self.entrys_Pre).arret_general()
                        self.tache_Pre[x][y]
                        
                if self.lll[-1]==0:
                    ligne=1
                else:  
                    ligne=self.lll[-1]+1  
                    
                for r in range(0,ligne,1):
                    for co in range(0,len(self.lc_Pre[r]),1):
                        self.buttons_Pre[r][co].config(text=">")
                        if self.lc_Pre[r][co] % 2 != 0:
                            self.lc_Pre[r][co]+=1                               
                return True

        elif id(buttons) == id(self.buttons_Pre):
            if not buttons[x][y].clicked:
                self.lc_Pre[x][y]+=1
                if self.lc_Pre[x][y] % 2 != 0:
                    self.bt_stop.config(state=tk.NORMAL)
                    self.tache_Pre[x][y]=Tache(timer, ltext, x, y, h, m, s,self.entrys_Pre).demarrer()
                    self.tache_Pre[x][y]
                    buttons[x][y].config(text="||")
                else:
                    self.tache_Pre[x][y]=Tache(timer, ltext, x, y, h, m, s,self.entrys_Pre).arret()
                    self.tache_Pre[x][y]
                    buttons[x][y].config(text=">")
                return True

    def creation_widgets(self, leftframe, i, j, ltext, timers, h, m, s, labels, buttons, lc, buttons_reset):
        labels[i][j] = tk.Entry(leftframe, textvariable= ltext[i][j]) 
        h[i][j] = int(ltext[i][j].get().split(":")[0])
        m[i][j] = int(ltext[i][j].get().split(":")[1])
        s[i][j] = int(ltext[i][j].get().split(":")[2])
        
        buttons[i][j] = tk.Button(leftframe,text=">",command= lambda x=i, y=j : self.command_lancer_arreter(buttons, timers, ltext, x, y, h, m, s))
        
        buttons[i][j].clicked = False
            
        buttons_reset[i][j] = tk.Button(leftframe,text="R", command= lambda x=i, y=j:Tache(timers,ltext, x, y, h, m, s).reset())
        
        buttons_reset[i][j].pack(side="right")
        buttons[i][j].pack(side="right")
        labels[i][j].pack(side="right")

        
    def onglet_recapitulatif(self):

        self.root2 = tk.Tk()
        self.root2.geometry('400x200')
        self.root2.title("Onglet Récapitulatif")
        def upload_file():
        
            
            l1=self.df.columns.values.tolist() # List of column names as header
            
            for index, rows in self.df.iterrows():
                ma_list=[rows.indexx,rows.Nom_du_mecano,rows.P,rows.S,rows.E,rows.U,rows.O,rows.A,rows.BO,rows.LT,rows.Quoi]
                
            r_set=[]
            for i in range(len(ma_list)):
                r_set.append(eval(ma_list[i]))
    
            for i in l1:
                self.trv.column(i,width=90,anchor='c')
                self.trv.heading(i,text=str(i))
                
            for j in zip(*r_set):
                v=[r for r in j]
                self.trv.insert("", tk.END,iid=v[0],values=v)
                
        self.b1 = tk.Button(self.root2, text='MAJ affichage', width=20,command = lambda:upload_file())
        
        def extract():
            dataframe = pd.DataFrame(self.dict1)
            file_name = fd.askdirectory(title="Choisir le répertoire cible")
            date_h = datetime.now()
            datej = date_h.strftime("%d%m%Y")
            dataframe.to_excel(r'{}\BDD_{}_chronomètre.xlsx'.format(file_name,datej),index=False)
            showinfo(title='Enregistrement', message="Fichier enregistré")
            
        self.b2 = tk.Button(self.root2, text='Extract au format Excel', width=20,command = lambda: extract())
        
        self.b1.pack(side = "top", fill='both')
        self.b2.pack(side = "top", fill='both')
        
        self.df = pd.read_csv(r'{}\test.csv'.format(self.directory), sep=',', header=0, index_col=None)
        self.l1=self.df.columns.values.tolist() # List of column names as header
        str1=tk.StringVar()
        str1 = "Lignes:" + str(self.df.shape[0])+ "\nColonnes:"+str(self.df.shape[1])
        self.lb1=tk.Label(self.root2,text=str1)
        self.lb1.pack(side = "top", fill='both')

        self.topframe2 = tk.Frame(self.root2, bg='white')
        self.topframe2.pack(pady=20)
        treeYScroll = ttk.Scrollbar(self.topframe2)
        treeYScroll.pack(side='right', fill='y')

        self.trv=ttk.Treeview(self.topframe2 ,selectmode='browse',height=10,show='headings', columns=self.l1, yscrollcommand= treeYScroll.set)
        treeYScroll.configure(command=self.trv.yview)

        self.trv.pack(side = "top", fill='both')
        self.root2.protocol('WM_DELETE_WINDOW', self.command_lancer_arreter_recap)  
        self.root2.update()
        self.root2.mainloop()
    

def quit_app():
    app.stop_all_threads()
    app.quit()
    app.destroy()   

            
if __name__ == '__main__' :
        app = Hello_IHM()
        app.protocol('WM_DELETE_WINDOW', quit_app)  # root is your root window
        app.mainloop()

