import tkinter as tk
from tkinter import font, ttk
import random
import threading
import math
import os
class RainbowCalculator:
 def __init__(self,root):
  self.root=root
  self.root.title("Rainbow Calculator - By Vague")
  self.root.geometry("800x600")
  self.root.resizable(False,False)
  self.root.attributes('-topmost',True)
  self.root.after(100,lambda:self.root.attributes('-topmost',False))
  self.rainbow_offset=0
  self.rainbow_speed=1.5
  self.is_animating_rainbow=True
  self.rainbow_cycle_width=400
  self.title_rainbow_offset=0
  self.title_rainbow_speed=-2.0
  self.bounce_offset=0
  self.bounce_speed=0.15
  self.title_base_y=80
  self.credit_base_y=140
  self.result=None
  self.is_calculating=False
  self.bg_music_file="bg_music.mp3"
  self.calc_music_file="shake_music.mp3"
  self.confetti_particles=[]
  self.canvas=tk.Canvas(root,highlightthickness=0,bg="black")
  self.canvas.pack(fill=tk.BOTH,expand=True)
  self.setup_ui()
  self.animate_rainbow()
  self.animate_title_rainbow()
  self.animate_bounce()
  self.play_bg_music()
 def setup_ui(self):
  try:
   self.title_font=font.Font(family="Comic Sans MS",size=48,weight="bold")
   self.credit_font=font.Font(family="Comic Sans MS",size=14,slant="italic")
   self.label_font=font.Font(family="Comic Sans MS",size=16,weight="bold")
   self.result_font=font.Font(family="Comic Sans MS",size=32,weight="bold")
   self.button_font=font.Font(family="Comic Sans MS",size=20,weight="bold")
  except:
   self.title_font=font.Font(family="Arial",size=48,weight="bold")
   self.credit_font=font.Font(family="Arial",size=14,slant="italic")
   self.label_font=font.Font(family="Arial",size=16,weight="bold")
   self.result_font=font.Font(family="Arial",size=32,weight="bold")
   self.button_font=font.Font(family="Arial",size=20,weight="bold")
  self.title_border=self.canvas.create_rectangle(250,50,550,110,outline="white",width=5)
  self.title_label=self.canvas.create_text(400,self.title_base_y,text="Calculator",font=self.title_font,fill="white",anchor="center")
  self.credit_label=self.canvas.create_text(400,self.credit_base_y,text="Created by Vague",font=self.credit_font,fill="yellow",anchor="center")
  self.controls_frame=tk.Frame(self.canvas,bg="white",bd=3,relief=tk.RAISED)
  self.controls_window=self.canvas.create_window(400,280,window=self.controls_frame,anchor="center")
  tk.Label(self.controls_frame,text="First Number:",font=self.label_font,bg="white",fg="black").grid(row=0,column=0,padx=10,pady=10,sticky="e")
  self.num1_var=tk.StringVar(value="1")
  self.num1_dropdown=ttk.Combobox(self.controls_frame,textvariable=self.num1_var,values=[str(i)for i in range(1,11)],state="readonly",width=10,font=("Arial",14))
  self.num1_dropdown.grid(row=0,column=1,padx=10,pady=10)
  tk.Label(self.controls_frame,text="Operator:",font=self.label_font,bg="white",fg="black").grid(row=1,column=0,padx=10,pady=10,sticky="e")
  self.operator_var=tk.StringVar(value="×")
  self.operator_dropdown=ttk.Combobox(self.controls_frame,textvariable=self.operator_var,values=["×","÷","+","-"],state="readonly",width=10,font=("Arial",14))
  self.operator_dropdown.grid(row=1,column=1,padx=10,pady=10)
  tk.Label(self.controls_frame,text="Second Number:",font=self.label_font,bg="white",fg="black").grid(row=2,column=0,padx=10,pady=10,sticky="e")
  self.num2_var=tk.StringVar(value="1")
  self.num2_dropdown=ttk.Combobox(self.controls_frame,textvariable=self.num2_var,values=[str(i)for i in range(1,11)],state="readonly",width=10,font=("Arial",14))
  self.num2_dropdown.grid(row=2,column=1,padx=10,pady=10)
  self.calc_button=tk.Button(self.canvas,text="Calculate",font=self.button_font,bg="#FF6B6B",fg="white",activebackground="#FF5252",activeforeground="white",relief=tk.RAISED,borderwidth=5,padx=40,pady=15,cursor="hand2",command=self.calculate)
  self.button_window=self.canvas.create_window(400,450,window=self.calc_button,anchor="center")
  self.bg_rects=[]
  self.draw_rainbow_background()
 def hsv_to_rgb(self,h,s,v):
  h=h%360
  c=v*s
  x=c*(1-abs((h/60)%2-1))
  m=v-c
  if 0<=h<60:r,g,b=c,x,0
  elif 60<=h<120:r,g,b=x,c,0
  elif 120<=h<180:r,g,b=0,c,x
  elif 180<=h<240:r,g,b=0,x,c
  elif 240<=h<300:r,g,b=x,0,c
  else:r,g,b=c,0,x
  return(int((r+m)*255),int((g+m)*255),int((b+m)*255))
 def draw_rainbow_background(self):
  if not self.is_animating_rainbow or self.is_calculating:return
  width=800
  height=600
  for rect in self.bg_rects:
   try:self.canvas.delete(rect)
   except:pass
  self.bg_rects=[]
  stripe_width=2
  num_stripes=(width//stripe_width)+(self.rainbow_cycle_width//stripe_width)+2
  normalized_offset=self.rainbow_offset%self.rainbow_cycle_width
  for i in range(num_stripes):
   x=(i*stripe_width)-normalized_offset
   if x+stripe_width<0:continue
   if x>width:break
   absolute_position=(x+normalized_offset)%self.rainbow_cycle_width
   hue=(absolute_position*360/self.rainbow_cycle_width)%360
   rgb=self.hsv_to_rgb(hue,1.0,1.0)
   color=f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
   rect_id=self.canvas.create_rectangle(x,0,x+stripe_width,height,fill=color,outline=color,width=0)
   self.bg_rects.append(rect_id)
  if not self.is_calculating:
   try:
    self.canvas.tag_raise(self.title_border)
    self.canvas.tag_raise(self.title_label)
    self.canvas.tag_raise(self.credit_label)
    self.canvas.tag_raise(self.controls_window)
    self.canvas.tag_raise(self.button_window)
   except:pass
 def animate_rainbow(self):
  if self.is_animating_rainbow and not self.is_calculating:
   self.rainbow_offset+=self.rainbow_speed
   self.draw_rainbow_background()
  self.root.after(30,self.animate_rainbow)
 def animate_title_rainbow(self):
  if not self.is_calculating and self.title_label:
   self.title_rainbow_offset+=self.title_rainbow_speed
   hue=(self.title_rainbow_offset*2)%360
   rgb=self.hsv_to_rgb(hue,1.0,1.0)
   color=f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
   try:self.canvas.itemconfig(self.title_label,fill=color)
   except:pass
   border_hue=(hue+180)%360
   border_rgb=self.hsv_to_rgb(border_hue,1.0,1.0)
   border_color=f"#{border_rgb[0]:02x}{border_rgb[1]:02x}{border_rgb[2]:02x}"
   try:self.canvas.itemconfig(self.title_border,outline=border_color)
   except:pass
  self.root.after(30,self.animate_title_rainbow)
 def animate_bounce(self):
  if not self.is_calculating and self.title_label:
   self.bounce_offset+=self.bounce_speed
   bounce_amount=5*math.sin(self.bounce_offset)
   try:self.canvas.coords(self.title_label,400,self.title_base_y+bounce_amount)
   except:pass
   try:
    current_coords=self.canvas.coords(self.title_border)
    if current_coords:
     self.canvas.coords(self.title_border,250,50+bounce_amount,550,110+bounce_amount)
   except:pass
   try:self.canvas.coords(self.credit_label,400,self.credit_base_y+bounce_amount*0.5)
   except:pass
  self.root.after(50,self.animate_bounce)
 def calculate(self):
  self.is_calculating=True
  self.calc_button.config(state="disabled")
  self.is_animating_rainbow=False
  try:
   self.canvas.itemconfig(self.title_label,text="")
   self.canvas.itemconfig(self.title_border,outline="")
   self.canvas.itemconfig(self.credit_label,text="")
  except:pass
  for rect in self.bg_rects:
   try:self.canvas.delete(rect)
   except:pass
  self.bg_rects=[]
  self.canvas.config(bg="black")
  try:
   self.canvas.itemconfig(self.controls_window,state="hidden")
   self.canvas.itemconfig(self.button_window,state="hidden")
  except:pass
  self.play_calc_music()
  num1=int(self.num1_var.get())
  num2=int(self.num2_var.get())
  operator=self.operator_var.get()
  if operator=="×":self.result=num1*num2
  elif operator=="÷":
   if num2==0:self.result="Error: Division by zero"
   else:self.result=round(num1/num2,2)
  elif operator=="+":self.result=num1+num2
  elif operator=="-":self.result=num1-num2
  self.shake_window()
 def shake_window(self):
  original_x=self.root.winfo_x()
  original_y=self.root.winfo_y()
  total_duration=2000
  shake_count=0
  total_shakes=100
  def shake():
   nonlocal shake_count
   if shake_count<total_shakes:
    progress=shake_count/total_shakes
    intensity=progress*progress
    max_offset=5+(intensity*25)
    offset_x=random.randint(-int(max_offset),int(max_offset))
    offset_y=random.randint(-int(max_offset),int(max_offset))
    self.root.geometry(f"+{original_x+offset_x}+{original_y+offset_y}")
    shake_count+=1
    delay=int(2000/total_shakes)
    self.root.after(delay,shake)
   else:
    self.root.geometry(f"+{original_x}+{original_y}")
    self.show_result()
  shake()
 def show_result(self):
  self.canvas.config(bg="white")
  self.canvas.delete("all")
  self.confetti_particles=[]
  result_text=f"Result: {self.result}"
  self.result_label=self.canvas.create_text(400,300,text=result_text,font=self.result_font,fill="black",anchor="center",width=700)
  self.create_confetti()
  self.animate_confetti()
  self.calc_button=tk.Button(self.canvas,text="Calculate Again",font=self.button_font,bg="#FF6B6B",fg="white",activebackground="#FF5252",activeforeground="white",relief=tk.RAISED,borderwidth=5,padx=30,pady=15,cursor="hand2",command=self.reset_calculator)
  self.button_window=self.canvas.create_window(400,500,window=self.calc_button,anchor="center")
  self.is_calculating=False
 def reset_calculator(self):
  self.canvas.delete("all")
  self.confetti_particles=[]
  self.is_calculating=False
  self.is_animating_rainbow=True
  self.bounce_offset=0
  self.setup_ui()
  self.play_bg_music()
 def create_confetti(self):
  self.confetti_particles=[]
  colors=["#FF6B6B","#4ECDC4","#45B7D1","#FFA07A","#98D8C8","#F7DC6F","#BB8FCE","#85C1E2"]
  for _ in range(50):
   x=random.randint(0,800)
   y=random.randint(0,200)
   color=random.choice(colors)
   size=random.randint(8,15)
   shape=random.choice(["circle","rectangle"])
   if shape=="circle":
    particle=self.canvas.create_oval(x,y,x+size,y+size,fill=color,outline=color)
   else:
    particle=self.canvas.create_rectangle(x,y,x+size,y+size,fill=color,outline=color)
   self.confetti_particles.append({"id":particle,"x":x,"y":y,"size":size,"vx":random.uniform(-2,2),"vy":random.uniform(-3,-1),"rotation":random.uniform(0,360)})
 def animate_confetti(self):
  if not self.confetti_particles:return
  for particle in self.confetti_particles[:]:
   try:
    particle["y"]+=particle["vy"]
    particle["x"]+=particle["vx"]
    particle["vy"]+=0.15
    self.canvas.coords(particle["id"],particle["x"],particle["y"],particle["x"]+particle["size"],particle["y"]+particle["size"])
    if particle["y"]>600:
     self.canvas.delete(particle["id"])
     self.confetti_particles.remove(particle)
   except:
    if particle in self.confetti_particles:self.confetti_particles.remove(particle)
  if self.confetti_particles:self.root.after(30,self.animate_confetti)
 def play_bg_music(self):
  def play_music():
   try:
    import pygame
    pygame.mixer.init()
    if os.path.exists(self.bg_music_file):
     pygame.mixer.music.load(self.bg_music_file)
     pygame.mixer.music.play(-1)
    else:print(f"Background music file '{self.bg_music_file}' not found.")
   except ImportError:print("pygame not installed. Install with: pip install pygame")
   except Exception as e:print(f"Error playing background music: {e}")
  threading.Thread(target=play_music,daemon=True).start()
 def play_calc_music(self):
  def play_music():
   try:
    import pygame
    if not pygame.mixer.get_init():pygame.mixer.init()
    pygame.mixer.music.stop()
    if os.path.exists(self.calc_music_file):
     pygame.mixer.music.load(self.calc_music_file)
     pygame.mixer.music.play()
    else:print(f"Calculation music file '{self.calc_music_file}' not found.")
   except ImportError:print("pygame not installed. Install with: pip install pygame")
   except Exception as e:print(f"Error playing calculation music: {e}")
  threading.Thread(target=play_music,daemon=True).start()
if __name__=="__main__":
 root=tk.Tk()
 app=RainbowCalculator(root)
 root.mainloop()