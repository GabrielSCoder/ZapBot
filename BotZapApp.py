#!/usr/bin/env python
# coding: utf-8

# In[9]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import pandas as pd
import urllib
from tkinter import *
from tkinter import filedialog
import logging
logging.basicConfig(level=logging.INFO,filename="execucao.log")


# In[14]:


def convert(l):
    x = []
    aux = ""    
    for i in l:
        aux = i.replace('+','')
        aux = aux.replace('-','')
        aux = aux.replace(' ','')
        x.append(aux)
    return x

def raise_frame(frame):
    frame.tkraise()

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("excel files",
                                                        "*.xlsx*"),
                                                       ("all files",
                                                        "*.*")))
    label_file_explorer.configure(text="Carregado!")
    global ff
    ff = filename


# In[15]:


def bot_start():
    nome_grupo = inputtxt.get("1.0",'end-1c')
    contatos = inputtxt2.get("1.0",'end-1c')
    saida = inputtxt3.get("1.0",'end-1c') 
    
    try:
        time.sleep(5)
        navegador.find_element(By.CSS_SELECTOR, f"span[title='{nome_grupo}']").click()
        time.sleep(5)
        navegador.find_element(By.XPATH, '//*[@id="main"]/header').click()
        time.sleep(5)
        participantes = navegador.find_element(By.XPATH, '//*[@id="app"]/div/div/div[5]/span/div/span/div/div/section/div[1]/div/div[3]/span/span/button')
        navegador.find_element(By.XPATH, '//*[@id="app"]/div/div/div[5]/span/div/span/div/div/section/div[6]/div[2]/button').click()
        navegador.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div[2]').click()
        ActionChains(navegador).send_keys(Keys.ARROW_DOWN).perform()

        n = participantes.text.split()
    except:
        logging.error("Deu ruim no bot_start")
        
    lnum = []
    try:
        conts = int(n[0])-1
        conts = conts - int(contatos)
    except:
        logging.error("Erro no numero de contatos")
    time.sleep(3)
    while len(lnum) < conts:
        nums = navegador.find_element(By.CLASS_NAME, "nne8e")
        naa = nums.text.split('\n')
        for i in naa:
            if i[0] == "+":
                lnum.append(i)
                lnum = list(dict.fromkeys(lnum))
        ActionChains(navegador).send_keys(Keys.ARROW_DOWN).perform()
        ActionChains(navegador).send_keys(Keys.ARROW_DOWN).perform()
        ActionChains(navegador).send_keys(Keys.ARROW_DOWN).perform()
        ActionChains(navegador).send_keys(Keys.ARROW_DOWN).perform()
    
    convert_nums = convert(lnum)
    try:
        d = {'numeros':convert_nums}
        df = pd.DataFrame(data=d)
        nome_tabela = ""
        df.to_excel(f"{saida}.xlsx",index=False)
    except:
        logging.error("deu erro no salvamento da planilha")


# In[16]:


def bot_send():
    try:
        msg = inputtxt02.get("1.0",'end-1c')
        tabela = pd.read_excel(ff)
    except:
        logging.error("Erro no bot_send no get msg ou da tabela")
    
    for linha in tabela.index:
        numero = tabela.loc[linha,'numeros']
        texto = urllib.parse.quote(msg)
        link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"

        navegador.get(link)

        while len(navegador.find_elements(By.ID, 'side')) < 1:
            time.sleep(1)
            
        time.sleep(2)

        if len(navegador.find_elements(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')) < 1:
            #navegador.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
            navegador.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')


            time.sleep(1)
        else:
            pass


# In[18]:


navegador = webdriver.Chrome()
navegador.get("https://web.whatsapp.com")
action = ActionChains(navegador)
    
while len(navegador.find_elements(By.ID, 'side')) < 1:
    time.sleep(1)

time.sleep(1)

ff = ""
testescreen1 = Tk()
testescreen1.title("BOTZAP")

#testescreen1.geometry("400x400")


f0 = Frame(testescreen1)
f1 = Frame(testescreen1)
f2 = Frame(testescreen1)
f3 = Frame(testescreen1)

for frame in (f0,f1, f2, f3):
    frame.grid(row=0, column=0, sticky='news')

lb0 = Label(f0,text="ESCOLHA O DESEJA FAZER:",padx=100,pady=10).grid(column=0,row=0)
lxx = Label(f0,text="").grid(column=0,row=1)
btn00 = Button(f0,text="Pegar numeros",command=lambda: raise_frame(f1)).grid(column=0,row=2)
lxxx = Label(f0,text="").grid(column=0,row=3)
btn01 = Button(f0,text="Enviar mensagens",command=lambda: raise_frame(f2)).grid(column=0,row=4)

indic = Label(f1,text="Nome do grupo(Copie e cole até os emojis):",pady=10,padx=0).grid(column=0,row=0)
inputtxt = Text(f1,height = 1, width = 40)
inputtxt.grid(column=0,row=1)
indic2 = Label(f1,text="Quantidade de contatos desse grupo que você tem salvo:",padx=25,pady=15)
indic2.grid(column=0,row=2)
inputtxt2 = Text(f1,height = 1, width = 10)
inputtxt2.grid(column=0,row=3)
indic3 = Label(f1,text="Nome do arquivo excel de saída:",padx=25,pady=15)
indic3.grid(column=0,row=4)
inputtxt3 = Text(f1,height = 1, width = 30)
inputtxt3.grid(column=0,row=5)
confirma = Button(f1,text="OK", command=lambda:bot_start())
confirma.grid(column=0,row=7)
aaa = Label(f1,text="").grid(column=0,row=6)    
back = Button(f1,text="Voltar",command=lambda: raise_frame(f0)).grid(column=0,row=8)

label_file_explorer = Label(f2,text = "Carregue uma planilha",width = 20, height = 4,fg = "blue")
button_explore = Button(f2,text = "Browse Files",command = browseFiles).grid(column=0,row=1)  
indic02 = Label(f2,text="Mensagem para enviar",padx=40,pady=15).grid(column=0,row=2)  
inputtxt02 = Text(f2,width = 40,height=8,padx=30)
inputtxt02.grid(column=0,row=3)
label_file_explorer.grid(column = 0, row = 0)
btn02 = Button(f2,text="Enviar",command=lambda: bot_send()).grid(column=0,row=4)
back = Button(f2,text="Voltar",command=lambda:raise_frame(f0)).grid(column=0,row=5)

raise_frame(f0)
testescreen1.mainloop()

