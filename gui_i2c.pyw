#GUI FOR I2C MEMORY ATMEL
from tkinter import *
from tkinter import messagebox
import serial, time
import sys
from tkinter import ttk 
import serial.tools.list_ports

#------------------------------------- CALL BACKS ---------------------------------------
def findcomport():
  global pic 
  global have_port
  have_port = False
  ports = serial.tools.list_ports.comports()
  for k in range(len(ports)):
    coms = ports[k]
    strcomport = str(coms)
    
    if "CCS" in strcomport:
      splitport = strcomport.split(' ')
      PORT = splitport[0]
      have_port = True
 
  if (have_port):
    try:
      pic = serial.Serial(PORT, 9600,timeout=1)
      time.sleep(1)
      print("CONNECTED TO "+PORT)
      label_deco.config(bg = "lightgreen")
    except:
      messagebox.showerror(message= "CONNECTION ISSUE!", title= "Error")
  else:
    messagebox.showerror(message= "NO CCS COMPORT FOUND", title= "Error")
  


def en_read ():
  #messagebox.showinfo( "i2c", "leer")
  Send_r.config(state = "normal",cursor = "hand2")
  direction_r.config(state = "normal")
  Send_w.config(state = "disable",cursor = "arrow")
  direction_w.config(state = "disable",cursor = "arrow")
  dato_w.config(state = "disable",cursor = "arrow")

  read_button.config(state = "disable", bg ="blue",cursor = "arrow")
  write_button.config(state = "normal", bg = "silver",cursor = "hand2")
  label_deco.config(bg = "silver")
     
def en_write ():
    #messagebox.showinfo( "i2c", "escribir")
  Send_w.config(state = "normal",cursor = "hand2")
  direction_w.config(state = "normal")
  dato_w.config(state = "normal")

  Send_r.config(state = "disable",cursor = "arrow")
  direction_r.config(state = "disable",cursor = "arrow")

  read_button.config(state = "normal", bg = "silver",cursor = "hand2")
  write_button.config(state = "disable",bg = "green",cursor = "arrow")
  
  label_deco.config(bg = "silver")


def read_data():
  try: 
    dir_int = int(direction_read.get())
    have_direction = True
  except:
    direction_read.set("")
    have_direction = False
    messagebox.showerror(message="Only numeric values are accepted", title="Error")

  if(have_direction):
    
    if(dir_int<4096):
      
      dir_str=str(dir_int)

      comando = 'D'+dir_str+'F'
      pic.write(comando.encode())
      time.sleep(0.2)
      

      comando = 'O'+'2'+'F'
      pic.write(comando.encode())
      time.sleep(0.2)

      try:
        rawString = pic.readline()
        returned_data = rawString.decode('ascii')
        read_data.config(text = "Data: "+returned_data)
        time.sleep(0.2)
        label_deco.config(bg = "yellow")
      except:
        pic.close()
        sys.exit("Getting Data Error")
    
    else:
      messagebox.showwarning(message="Direction value is accepted only from 0 to 4095", title="Warning")

  have_direction = False
  
  


      

def write_data():
  
  try: 
    data_int = int(dato_w.get())
    have_direction_w = True
    
  except:
    dato_w.set("")
    have_direction_w = False
    messagebox.showerror(message="Only numeric values are accepted", title="Error")

  if(have_direction_w):
    if(data_int<256):
      data_str=str(data_int)

      comando = 'E'+data_str+'F'
      pic.write(comando.encode())
      time.sleep(0.2)
    else:
      messagebox.showwarning(message="Data value is accepted only from 0 to 255", title="Warning")

    try: 
      dir_int = int(direction_w.get())
      have_direction = True
    except:
      direction_read.set("")
      have_direction = False
      messagebox.showerror(message="Only numeric values are accepted", title="Error")

  if(have_direction and data_int<256):
    
    if(dir_int<4096):
      
      dir_str=str(dir_int)

      comando = 'D'+dir_str+'F'
      pic.write(comando.encode())
      time.sleep(0.2)

      comando = 'O'+'1'+'F'
      pic.write(comando.encode())
      time.sleep(0.2)

      for k in range(100):
        load_bar['value'] = k
        root.update_idletasks()
        time.sleep(0.01)
      time.sleep(1)
      load_bar['value'] = 0
      label_deco.config(bg = "yellow")

    else:
      messagebox.showwarning(message="Direction value is accepted only from 0 to 4095", title="Warning")

  have_direction_w = False
  have_direction = False


def on_closing():
  if (have_port):
    pic.close()
  root.destroy()


#--------------------- ROOT -----------------------------#
root = Tk()

direction_read = StringVar()

data_int = IntVar()
dir_in = IntVar()

dir_str = StringVar()
data_str = StringVar()

returned_data = StringVar()

have_direction = False
have_dinrectio_w = False


root.title("Memory I2C")
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/3 - windowHeight/2)
root.geometry("+{}+{}".format(positionRight, positionDown))
root.iconbitmap("D:\APLICACIONES DEL MICRO18F45K50\PYTHON-MEM_I2C\icono.ico")
root.resizable(False,False)
#root.geometry("500x300")
#root.config(bg = "blue")

#--------------------- FRAME -----------------------------#
myframe = Frame(root, width = "500", height = "500")
myframe.pack(fill = 'both', expand = 'true')
myframe.config(bg = "Silver")
#myframe.config(width = "650", height = "350")
#myframe.config(bd = 15)
#myframe.config(relief = "groove")
#myframe.config(cursor = "hand2")

#--------------------- TITLES LABELS  -----------------------------#
Label(myframe, text = "WRITE DATA", font = ("Courier New", 16, "bold"), bg = 'silver', fg = "green").grid(row=0, column=1,padx=10)
Label(myframe, text = "READ DATA",font = ("Courier New", 16,"bold"),bg = 'silver',fg = 'blue').grid(row = 0, column = 0,padx=10)

#------------------------------- OPS BUTTONS ------------------------------------
foto_read = PhotoImage (file = "D:\APLICACIONES DEL MICRO18F45K50\PYTHON-MEM_I2C\lectura2.png")
read_button =  Button(myframe, image = foto_read, bd = 5, command = en_read,cursor = "hand2")
read_button.grid(row = 1, column = 0,padx=10,pady=10)

foto_write = PhotoImage (file = "D:\APLICACIONES DEL MICRO18F45K50\PYTHON-MEM_I2C\escritura2.png")
write_button = Button(myframe, image = foto_write,bd = 5,command = en_write,cursor = "hand2")
write_button.grid(row = 1, column = 1,padx=10,pady=10)

#--------------------------------- LABELS AND ENTRYS ------------------------
#-------READ
Label(myframe, text = "Direction", bg = "silver", font = ("Courier New",14)).grid(row=2, column=0)
direction_r = Entry(myframe,font = ("Courier New",12), justify = "center", width = 6, relief = "sunken", bd = 5, state = "disable", textvariable = direction_read)
direction_r.grid(row=3,column=0)
Send_r = Button(myframe, text = "Read Direction", font = ("Courier New",10,'bold'),width = 14, state = "disable", command=read_data)
Send_r.grid(row=4,column=0, pady = 10)
read_data = Label(myframe, font = ("Courier New",14, 'bold'), justify = "center", bg = "silver", fg = "blue")
read_data.grid(row=5,column=0) 

decoration = PhotoImage(file = "D:\APLICACIONES DEL MICRO18F45K50\PYTHON-MEM_I2C\memok.png")
label_deco = Button(myframe, image = decoration, bg = "silver",bd = 3, cursor = "hand2", command = findcomport)
label_deco.grid(row = 6, column = 0)

#------WRITE
Label(myframe, text = "Data", bg = "silver", font = ("Courier New",14)).grid(row=2, column=1)
dato_w = Entry(myframe,font = ("Courier New",12), justify = "center", width = 5,relief = "sunken", bd=5,state = "disable")
dato_w.grid(row=3,column=1)

Label(myframe, text = "Direction", bg = "silver", font = ("Courier New",14)).grid(row=4, column=1)
direction_w = Entry(myframe,font = ("Courier New",12), justify = "center", width = 6, relief = "sunken", bd = 5, state = "disable")
direction_w.grid(row=5,column=1)

Send_w = Button(myframe,text = "Write Data",font = ("Courier New",10,'bold'),width = 14, state = "disable",command=write_data)
Send_w.grid(row=6,column=1,pady = 10) 

load_bar = ttk.Progressbar(myframe, orient = HORIZONTAL, length = 100, mode = "determinate")
load_bar.grid(row=7,column=1, pady = 9)


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

