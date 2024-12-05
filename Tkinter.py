#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 23:20:20 2024

@author: charanmakkina
"""

import tkinter as tk
import subprocess
import io
from tkinter import filedialog

def run_program_mdcomp():
    app=tk.Tk()
    app.title('DOD Market Data Comparison')
    app.geometry('600x450')
    label_text=['T_Date','T-1_Date','path_T','path_T-1','path_to_Save']
    labels=[]
    entries=[]

    for text in label_text:
        labels.append(tk.Label(app,text=text))
        entries.append(tk.Entry(app,width=30))
    
    labels.append(tk.Label(app,text='SNAP'))
    options=['LDN1200','LDN1500','LDN1615','NY1600']
    selected_option=tk.StringVar()
    selected_option.set(options[0])
    entries.append(tk.OptionMenu(app,selected_option,*options))
    labels.append(tk.Label(app,text='Select the assets'))
    checkbox_vars={'CDS':tk.IntVar(),
                   'CDX':tk.IntVar(),
                   'IRSZCS':tk.IntVar(),
                   'FXO':tk.IntVar(),
                   'INF':tk.IntVar(),
                   'SWO':tk.IntVar()
                   }
    row=5
    column=1
    for choice,var in checkbox_vars.items():
        entry_cb=tk.Checkbutton(app,text=choice,variable=var,onvalue=1,offvalue=0)
        entry_cb.grid(row=row+1,column=column,sticky='w')
        if(row==7):
            row=5
            column=2 
        else:
            row=row+1 
    def browse_path1():
        path1=filedialog.askdirectory()
        if path1:
            entries[2].delete(0,tk.END)
            entries[2].insert(0,path1)
    
    def browse_path2():
        path2=filedialog.askdirectory()
        if path2:
            entries[3].delete(0,tk.END)
            entries[3].insert(0,path2)
    def browse_path3():
        path3=filedialog.askdirectory()
        if path3:
            entries[4].delete(0,tk.END)
            entries[4].insert(0,path3)
    def run_program():
        inputs=[]
        for entry in entries[:5]:
            inputs.append(entry.get())
            
        input_sc=selected_option.get()
        selected_choice=[choice for choice, var in checkbox_vars.items() if var.get()==1]
        inputs.append(','.join(selected_choice))
        if((len(inputs[0])!=0) & (len(inputs[1])!=0) & (len(inputs[2])!=0) & (len(inputs[3])!=0) & 
           (len(inputs[4])!=0) & (len(selected_choice)!=0)):
            if(input_sc=='LDN1200'):
                command=['python','DOD_Comparison_1200.py']+inputs
            elif(input_sc=='LDN1500'):
                command=['python','DOD_Comparison_1500.py']+inputs
            elif(input_sc=='LDN1615'):
                command=['python','DOD_Comparison_1200.py']+inputs
            elif(input_sc=='NY1600'):
                command=['python','DOD_Comparison_1600.py']+inputs
            try:
                result=subprocess.run(command,stdout=subprocess.PIPE,shell=True,text=True)
                stdout_buffer=io.StringIO()
                stderr_buffer=io.StringIO()
                for line in result.stdout:
                    stdout_buffer.write(line)
                for line in result.stderr:
                    stderr_buffer.write(line)
                stdout_data=stdout_buffer.getvalue()
                stderr_data=stderr_buffer.getvalue()
                error_text.delete(1.0,tk.END)
                if(len(stderr_data)==0):
                    error_text.insert(tk.END,f"Success, Check the files in the below path:\n{inputs[4]}\n")
                error_text.insert(tk.END,f"{stdout_data}\n")
                error_text.insert(tk.END,f"{stderr_data}\n")
            except Exception as e:
                error_text.delete(1.0,tk.END)
                error_text.insert(tk.END,f"Error:{str(e)}")
        else:
            error_text.delete(1.0,tk.END)
            error_text.insert(tk.END,"Please select all fields")
        
    run_button=tk.Button(app,text='Run Program',command=run_program)
    def run_outer_close():
        app.destroy()
        run_outer()
    goback_button=tk.Button(app,text='Go Back',command=run_outer_close)
    error_text=tk.Text(app,height=8,width=60)
    def close_app():
        app.destroy()
    def clear_app():
        error_text.delete(1.0,tk.END)
        for entry in entries[0:5]:
            entry.delete(0,tk.END)
        selected_option.set(options[0])
        checkboxes=[]
        for r in range(6,9):
            for c in range(1,3):
                checkboxes.append(app.grid_slaves(row=r,column=c)[0])
        for checkbox in checkboxes:
            checkbox.deselect()
    clear_button=tk.Button(app,text='Clear Fields',command=clear_app)
    close_button=tk.Button(app,text='Close app',command=close_app)
    for r in range(0,7):
        labels[r].grid(row=r,column=0)
    for r in range(0,6):
        entries[r].grid(row=r,column=1)
    browse_button1=tk.Button(app,text='Browse',command=browse_path1)
    browse_button1.grid(row=2,columns=2)
    browse_button2=tk.Button(app,text='Browse',command=browse_path2)
    browse_button2.grid(row=3,columns=2)
    browse_button3=tk.Button(app,text='Browse',command=browse_path3)
    browse_button3.grid(row=4,columns=2)
    error_text.grid(row=11,column=0,columnspan=2)
    run_button.grid(row=9,column=0,columnspan=2)
    clear_button.grid(row=9,column=1,columnspan=2)
    goback_button.grid(row=10,column=0,columnspan=2)
    
    close_button.grid(row=10,column=1,columnspan=2)
    app.mainloop()
def run_program_prodvsQA():
    app=tk.Tk()
    app.title('Prod vs QA Comparison')
    app.geometry('600x450')
    label_text=['path_Prod','path_QA','round_off']
    labels=[]
    entries=[]

    for text in label_text:
        labels.append(tk.Label(app,text=text))
        entries.append(tk.Entry(app,width=30))
    
    def browse_path1():
        path1=filedialog.askdirectory()
        if path1:
            entries[0].delete(0,tk.END)
            entries[0].insert(0,path1)
    
    def browse_path2():
        path2=filedialog.askdirectory()
        if path2:
            entries[1].delete(0,tk.END)
            entries[1].insert(0,path2)

    def run_program():
        inputs=[]
        for entry in entries[:3]:
            inputs.append(entry.get())
            
        if((len(inputs[0])!=0) & (len(inputs[1])!=0) & (len(inputs[2])!=0)):
            command=['python3','Prod_Vs_QA1.py']

            try:
                result=subprocess.run(command,stdout=subprocess.PIPE,shell=True,text=True)
                stdout_buffer=io.StringIO()
                stderr_buffer=io.StringIO()
                for line in result.stdout:
                    stdout_buffer.write(line)
                for line in result.stderr:
                    stderr_buffer.write(line)
                stdout_data=stdout_buffer.getvalue()
                stderr_data=stderr_buffer.getvalue()
                error_text.delete(1.0,tk.END)
                if(len(stderr_data)==0):
                    error_text.insert(tk.END,f"Success, Check the files in the below path:\n{inputs[0]}\n")
                error_text.insert(tk.END,f"{stdout_data}\n")
                error_text.insert(tk.END,f"{stderr_data}\n")
            except Exception as e:
                error_text.delete(1.0,tk.END)
                error_text.insert(tk.END,f"Error:{str(e)}")
        else:
            error_text.delete(1.0,tk.END)
            error_text.insert(tk.END,"Please select all fields")
        
    run_button=tk.Button(app,text='Run Program',command=run_program)
    def run_outer_close():
        app.destroy()
        run_outer()
    goback_button=tk.Button(app,text='Go Back',command=run_outer_close)
    error_text=tk.Text(app,height=8,width=60)
    def close_app():
        app.destroy()
    def clear_app():
        error_text.delete(1.0,tk.END)
        for entry in entries[0:3]:
            entry.delete(0,tk.END)
    clear_button=tk.Button(app,text='Clear Fields',command=clear_app)
    close_button=tk.Button(app,text='Close app',command=close_app)
    for r in range(0,3):
        labels[r].grid(row=r,column=0)
    for r in range(0,3):
        entries[r].grid(row=r,column=1)
    browse_button1=tk.Button(app,text='Browse',command=browse_path1)
    browse_button1.grid(row=0,column=2)
    browse_button2=tk.Button(app,text='Browse',command=browse_path2)
    browse_button2.grid(row=1,column=2)
    error_text.grid(row=6,column=0,columnspan=2)
    run_button.grid(row=4,column=0,columnspan=2)
    clear_button.grid(row=4,column=1,columnspan=2)
    goback_button.grid(row=5,column=0,columnspan=2)
    
    close_button.grid(row=5,column=1,columnspan=2)
    app.mainloop()

def run_outer():
    app1=tk.Tk()
    app1.title('Market Price Controls')
    app1.geometry('400x100')
    label=tk.Label(app1,text='Choose one of the following')
    options=['Prod vs QA Comparison','DOD Market Data Comparison']
    selected_option=tk.StringVar()
    selected_option.set(options[0])
    entry=tk.OptionMenu(app1,selected_option,*options)
    def run_program_outer():
        num=selected_option.get()
        app1.destroy()
        if(num=='DOD Market Data Comparison'):
            run_program_mdcomp()
        if(num=='Prod vs QA Comparison'):
            run_program_prodvsQA()
    
    run_button=tk.Button(app1,text='Run Program',command=run_program_outer)
    label.grid(row=0,column=0)
    entry.grid(row=0,column=1)
    run_button.grid(row=1,column=0,columnspan=2)
    app1.mainloop()

run_outer()
    

    
    

            
            
            
                    
            
