#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from tkinter import * 
from math import floor
from tkinter import messagebox
from tkinter import filedialog

#https://www.youtube.com/watch?v=YXPyB4XeYLA

#sempre começar chamando o módulo

root = Tk()


root.title('Calculadora de Risco')
root.iconbitmap('C:/Users/1998a/bolsistas/bolsistas_ico.ico')
root.geometry('450x390')

title = Label(root, text='Calculadora de Risco', padx=50)
title.grid(row=0, column=0, columnspan=2)
title.config(font=("Courier", 20, 'bold'))

pat = Entry(root)
pat_lab = Label(root, text='Patrimônio', padx=50).grid(row=1, column=0)
pat.grid(row=2, column=0)

pat_d = Entry(root)
pat_dlab = Label(root, text='Caixa Disponível', padx=50).grid(row=3, column=0)
pat_d.grid(row=4, column=0)

ris = Entry(root)
ris_lab = Label(root, text=f'Risco Aceitável', padx=50).grid(row=5, column=0)
ris.insert(0, '{:.2%}'.format(0.01))
ris.grid(row=6, column=0)

ent = Entry(root)
ent_lab = Label(root, text='Preço de Entrada', padx=50).grid(row=1, column=1)
ent.grid(row=2, column=1)

out = Entry(root)
out_lab = Label(root, text='Preço de Stop Loss', padx=50).grid(row=3, column=1)
out.grid(row=4, column=1)


def resultado():
    
    pat_v = float(pat.get()) 
    patd_v = float(pat_d.get()) 
    ris_v = float(ris.get()[:-1])/100 
    ent_v = float(ent.get()) 
    out_v = float(out.get()) 
    
    calc = floor(((pat_v*ris_v)/(((1-(out_v)/ent_v))*ent_v)))
    
    if out_v>=ent_v:
        messagebox.showwarning(title='Atenção!',message='O Preço de Saída não pode ser maior que o de Entrada.')
        return 
        
    if pat_v<patd_v:
        messagebox.showwarning(title='Atenção!',message='O Caixa Disponível não pode ser maior que o Patrimônio.')
        return
    
    if patd_v<ent_v:
        messagebox.showwarning(title='Atenção!',message='Caixa Disponível muito baixo para realizar qualquer operação.')
        return
    
    if pat_v*ris_v < (ent_v-out_v):
        messagebox.showwarning(title='Atenção!',message='Risco Aceitável muito baixo para realizar qualquer operação.')
        return
        
    
    if out_v<ent_v and pat_v>=patd_v and patd_v>ent_v and pat_v*ris_v > (ent_v-out_v):     
        
        if calc*ent_v <= patd_v:
            
            ret = Text(root, height=3, width=43)
                  
            ret.insert('insert',f'Você vai arriscar R$ {round(calc*ent_v*(1-(out_v/ent_v)),2)}\ncomprando R$ {round(calc*ent_v,2)} ({calc} ações)!')
            
            ret.grid(row=10,column=0, columnspan=2)
            
        else:
            
            calc = floor(patd_v/ent_v)
            
            risco_novo = calc*(((1-(out_v/ent_v))*ent_v)/pat_v)
            
            ris.delete(0,'end')
            ris.insert(0, '{:.2%}'.format(risco_novo))
            
            messagebox.showwarning(title='Atenção!', 
                                   message=f'Como seu caixa disponível não é suficiente para realizar a operação desejada, seu risco baixou para' + ' {:.2%}.'.format(risco_novo))
           
            ret = Text(root, height=3, width=43)
                  
            ret.insert('insert', f'Você vai arriscar R$ {round(calc*ent_v*(1-(out_v/ent_v)),2)}\ncomprando R$ {round(calc*ent_v,2)} ({calc} ações)!')
            
            ret.grid(row=10, column=0, columnspan=2)
            
Label(root, text='').grid(row=7, column=0, columnspan=2)
        
myButton = Button(root, text='Calcular!', command=resultado,).grid(row=8, column=0, columnspan=2)

Label(root, text='').grid(row=9, column=0, columnspan=2)

root.mainloop() #rodando o programa de fato, fazer o loop


# In[ ]:




