'''
Created on 7 set 2019

@author: Lorenzo
'''
from datetime import datetime as dt
from json     import dumps , load
from os.path  import isfile, split
from random   import SystemRandom
from time     import sleep
from tkinter  import (
           BooleanVar,
           Button    ,
           Entry     ,
           Frame     ,
           IntVar    ,
           Label     ,
           LabelFrame,
           Scrollbar,
           Listbox,
           Menu      ,
           Menubutton,
           Toplevel,
           PhotoImage,
           Spinbox   ,
           StringVar ,
           Tk        )
from tkinter.messagebox import askyesno
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk
from urllib .request    import urlopen
from tkinter.constants import *

from tkinterhtml import HtmlFrame

_title        = 'Dungeons & Dragons Master Tool'

class popupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Enter the character name")
        self.l.pack()
        self.e=Entry(top)
        self.e.bind("<Return>", (lambda event: self.cleanup()))
        self.e.focus()
        self.e.pack()
        self.l1=Label(top,text="Enter the HP")
        self.l1.pack()
        self.e1=Entry(top)
        self.e1.bind("<Return>", (lambda event: self.cleanup()))
        self.e1.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.name=self.e.get()
        self.hp=self.e1.get()
        self.top.destroy()

class popupWindowMonster(object):
    
    
    def __init__(self,master):
        top=self.top=Toplevel(master)
        html_label = HtmlFrame(top, horizontal_scrollbar="auto", vertical_scrollbar=True)
        html_label.pack(fill="both", expand=True)
        html_label.set_content(main.html)
        
        self.b=Button(top,text='Esci',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.top.destroy()
        
class MainFrame(Frame):
    
    def popupmsg(self, monster_name, html):
        popup = Tk()
        popup.wm_title(monster_name)
        html_label = HtmlFrame(popup, horizontal_scrollbar="auto", vertical_scrollbar=True)
        html_label.pack(fill="both", expand=True)
        html_label.set_content(html)
        B1 = ttk.Button(popup, text="Close", command = popup.destroy)
        B1.pack()
        popup.mainloop()
        
    def set_defaults(self):
        self.master.title(_title)
        self.fpath = 'c:/d&d'
        self.always_on_top.set(False)
        
    def pin(self):
        self.master.wm_attributes('-topmost', self.always_on_top.get())

    def add_character(self):
        self.w = popupWindow(self.master)
        self.add_button["state"] = "disabled" 
        self.master.wait_window(self.w.top)
        self.add_button["state"] = "normal"
        self.next_button["state"] = "normal"
        self.roll_button["state"] = "normal"
        self.list_index+=1
        self.tree.insert("", self.list_index, self.list_index.__str__(), text=self.entryValue("nome"), values=(self.entryValue("hp"), ""))

    def roll_dice(self, dice_faces):
        rng = SystemRandom()
        return rng.randint(1, dice_faces)   
    
    def roll_initiative(self):
        for i in self.tree.get_children():
            val = self.tree.item(i, "values")
            if val[1] == "":
                self.tree.set(i, 'one', self.roll_dice(20))
        self.treeview_sort_column(self.tree, "one", True)
         
    def entryValue(self, campo):
        if campo == "nome":
            return self.w.name
        if campo == "hp":
            return self.w.hp
        return ""
    
    def next_character(self):
        self.list_selected_index+=1
        if self.list_selected_index > len(self.tree.get_children()):
            self.list_selected_index=1
        self.tree.selection_set(self.list_selected_index)
    
    def remove_character(self):
        self.tree.delete(self.tree.focus())
        
    def remove_all_characters(self):
        self.tree.delete(*self.tree.get_children())
        self.list_index=0
        self.list_selected_index=0
        self.next_button["state"] = "disabled" 
        self.roll_button["state"] = "disabled"


    def set_saved_title(self, fpath):
        fname = split(fpath)[-1].replace('.json', '')
        self.master.title('{}  -  {}'.format(fname, _title))

    def set_unsaved_title(self, *args):
#         if len(roller_groups) < 1:
#             return
        title = self.master.title()
        if title == _title:
            title = '{}  -  {}'.format('Unsaved', title)
        if '*' not in title:
            title = '*' + title

        self.master.title(title)

    def ask_proceed(self):
        if '*' in self.master.title():
            if not askyesno('Unsaved changes!', 'There are unsaved changes!\r\nWould you like to proceed anyway?'):
                return False
        return True
        
    def load_monster_name(self):
        fpath = "C:/Users/Lorenzo/temp/srd_5e_monsters.json"
        if not fpath or not isfile(fpath):
            return
        
        self.dictionary = {}
        listanomi = []
        with open(fpath, 'r') as f:
            monsters_file = load(f)
        try:
            for monster in monsters_file:
                listanomi.append(monster["name"])
                self.dictionary[monster["name"]] = monster
        except KeyError:
            pass
        return listanomi
        
    def load_monster(self, monsterName):

        try:
            
            self.html = '<div style="width:90%; font-family:Arial,Helvetica,sans-serif;font-size:16px;">'
            self.html = self.convert_json_to_html(self.dictionary[monsterName], self.html)
            self.html = self.html + '</div>'
            self.html = self.html + '</body>'
            self.html = self.html + '</html>'
        except KeyError:
            pass


    def convert_json_to_html(self, monster, html):
        
        gradient = '<div style="background:#A73335;height:5px;margin:7px 0px;"></div>'
        keys = monster.keys()
        html = html + '<div style="font-size:225%;font-family:Georgia, serif;font-variant:small-caps;font-weight:bold;color:#A73335;">' + monster["name"] + '</div>'
        html = html + '<div style="font-style:italic;">' + monster["meta"] + '</div>'
        html = html + gradient
        html = html + '<div class="red">'
        html = html + '    <div ><span style="font-weight:bold;color:#A73335;">Armor Class: </span><span>' + monster["Armor Class"] + '</span></div>'
        html = html + '    <div><span style="font-weight:bold;color:#A73335;">Hit Points: </span><span>' + monster["Hit Points"] + '</span></div>'
        html = html + '    <div><span style="font-weight:bold;color:#A73335;">Speed: </span><span>' + monster["Speed"] + '</span></div>'
        html = html + '</div>'            
        html = html + gradient
        html = html + '<table style="width:60%;border:0px;border-collapse:collapse;color:#A73335;">'
        html = html + '    <tr>'
        html = html + '            <th style="width:20%;text-align:center;">STR</th>'
        html = html + '            <th style="width:20%;text-align:center;">DEX</th>'
        html = html + '            <th style="width:20%;text-align:center;">CON</th>'
        html = html + '            <th style="width:20%;text-align:center;">INT</th>'
        html = html + '            <th style="width:20%;text-align:center;">WIS</th>'
        html = html + '            <th style="width:20%;text-align:center;">CHA</th>'
        html = html + '    </tr>'
        html = html + '    <tr>'
        html = html + '            <td style="width:20%;text-align:center;">' + monster["STR"] + ' ' + monster["STR_mod"] + '</td>'
        html = html + '            <td style="width:20%;text-align:center;">' + monster["DEX"] + ' ' + monster["DEX_mod"] + '</td>'
        html = html + '            <td style="width:20%;text-align:center;">' + monster["CON"] + ' ' + monster["CON_mod"] + '</td>'
        html = html + '            <td style="width:20%;text-align:center;">' + monster["INT"] + ' ' + monster["INT_mod"] + '</td>'
        html = html + '            <td style="width:20%;text-align:center;">' + monster["WIS"] + ' ' + monster["WIS_mod"] + '</td>'
        html = html + '            <td style="width:20%;text-align:center;">' + monster["CHA"] + ' ' + monster["CHA_mod"] + '</td>'
        html = html + '    </tr>'
        html = html + '</table>'
        html = html + gradient
        if "Saving Throws" in keys:
            html = html + '<div><span style="font-weight:bold;">Saving Throws: </span><span>' + monster["Saving Throws"] + '</span></div>'
        if "Skills" in keys:
            html = html + '<div><span style="font-weight:bold;">Skills: </span><span>' + monster["Skills"] + '</span></div>'
        if "Damage Immunities" in keys:
            html = html + '<div><span style="font-weight:bold;">Damage Immunities: </span><span>' + monster["Damage Immunities"] + '</span></div>'
        if "Damage Resistances" in keys:
            html = html + '<div><span style="font-weight:bold;">Damage Resistances: </span><span>' + monster["Damage Resistances"] + '</span></div>'
        if "Condition Immunities" in keys:
            html = html + '<div><span style="font-weight:bold;">Condition Immunities: </span><span>' + monster["Condition Immunities"] + '</span></div>'
        if "Senses" in keys:
            html = html + '<div><span style="font-weight:bold;">Senses: </span><span>' + monster["Senses"] + '</span></div>'
        if "Languages" in keys:
            html = html + '<div><span style="font-weight:bold;">Languages: </span><span>' + monster["Languages"] + '</span></div>'
        if "Challenge" in keys:
            html = html + '<div><span style="font-weight:bold;">Challenge: </span><span>' + monster["Challenge"] + '</span></div> '
        
        html = html + gradient
        
        if "Traits" in keys:
            html = html + '<div style="font-size:175%;font-variant:small-caps;margin:17px 0px 0px 0px;">Traits</div>'
            html = html + '<div>' + monster["Traits"] + '</div>'
            html = html + gradient
        
        if "Actions" in keys:
            html = html + '<div style="font-size:175%;font-variant:small-caps;margin:17px 0px 0px 0px;">Actions</div>'
            html = html + '<div>' + monster["Actions"] + '</div>'
            html = html + gradient
        
        if "Legendary Actions" in keys:
            html = html + '<div style="font-size:175%;font-variant:small-caps;margin:17px 0px 0px 0px;">Legendary Actions</div>'
            html = html + '<div>' + monster["Legendary Actions"] + '</div>'
            html = html + gradient
        
        if "img_url" in keys:
            html = html + '<div><img src=' + monster["img_url"] + '></div>'
            
#             for key in item.keys():
#                 if key == "name" and oldkey == "":
#                     html = html + '<div style="font-size:225%;font-family:Georgia, serif;font-variant:small-caps;font-weight:bold;color:#A73335;">' + item[key] + '</div>'
#                 elif key == "name" and oldkey != "":
#                     html = html + ('<h3 style="color: blue; text-align: left">') + oldkey + ('</H3>')
#                 else:
#                     keyPrint = key.replace("_", " ").capitalize()
#                     
#                     html = html + "<b>" + keyPrint + ": </b>" + str(item[key]) + "<br>"
#                 
#                 if (type(item[key]) is list):
#                     html = self.convert_json_to_html(item[key], html, key)
#                 print(html)
        return html

    def load_config(self):
        autosave = False
        if not self.ask_proceed():
            return

        fpath = askopenfilename(filetypes=[('JSON', '*.json'), ('All', '*.*')], defaultextension='.json')
        if not fpath or not isfile(fpath):
            return
        self.fpath = fpath

#         self.clear_groups()

#         with open(fpath, 'r') as f:
#             group_dict = load(f)
# 
#         try:
#             settings_dict = group_dict.pop('settings')
#             autosave      = (settings_dict['autosave'])
#             self.use_random_org.set(settings_dict['use_random_org'])
#             self.allow_odd     .set(settings_dict['allow_odd'     ])
#             self.always_on_top .set(settings_dict['always_on_top' ])
#         except KeyError:
#             pass
# 
#         g = 0
#         for group_name, group_settings in group_dict.items():
#             self.create_group(g, len(group_settings['rollers']))
# 
#             group = roller_groups[g]
#             group.name.set(group_name)
#             group.index = group_settings['index']
# 
#             r = 0
#             h = 0
#             for roller_name, roller_settings in group_settings['rollers'].items():
#                 roller = group.rollers[r]
#                 roller.name.set(roller_name)
#                 for attr, value in roller_settings.items():
#                     try:
#                         getattr(roller, attr).set(value)
#                     except AttributeError:
#                         setattr(roller, attr, value)
#                 roller.reset(loading=True)
#                 h = len(roller.history) - 1
#                 r += 1
# 
#             group.navigate_history(desired_index=h)
#             g += 1
# 
#         roller_groups.sort(key=lambda x: x.index)
# 
#         maintain_group_indices()
#         for group in roller_groups:
#             group.rollers.sort(key=lambda x: x.index)
#             group.maintain_roller_indices()
#             for roller in group.rollers:
#                 roller.apply_modifiers()
# 
#         maintain_tabstops()

        self.pin()
        self.autosave.set(autosave)
        self.set_saved_title(fpath)
        
    def save_config(self, fpath=''):
        if not fpath:
            fpath = asksaveasfilename(filetypes=[('JSON', '*.json'), ('All', '*.*')], defaultextension='.json')
        if not fpath:
            if '*' in self.master.title():
                pass
            return
        self.fpath = fpath

#         d1 = {}
#         d1['settings'] = {'use_random_org': self.use_random_org.get(),
#                           'allow_odd'     : self.allow_odd     .get(),
#                           'always_on_top' : self.always_on_top .get(),
#                           'autosave'      : self.autosave      .get()}
#         for group in roller_groups:
#             group.maintain_roller_indices()
#             d2 = {}
#             d2['index'] = group.index
#             d2['rollers'] = {}
#             for roller in group.rollers:
#                 name = roller.name.get()
#                 while name in d2['rollers']:
#                     name += '!'
#                 d2['rollers'][name] = {'index'    : roller.index          ,
#                                        'history'  : roller.history        ,
#                                        'dice_qty' : roller.dice_qty .get(),
#                                        'die_faces': roller.die_faces.get(),
#                                        'modifier' : roller.modifier .get(),
#                                        'finalmod' : roller.finalmod .get()}
#             name = group.name.get()
#             if name in d1:
#                 name += '!'
#             d1[name] = d2
# 
#         with open(fpath, 'w') as f:
#             f.write(dumps(d1, indent=2, separators=(',', ': ')))

        self.set_saved_title(fpath)
        
            
    def __init__(self, master):
        Frame.__init__(self, master)
    
        self.master = master
    
        self.always_on_top  = BooleanVar()
    
        self.set_defaults()
    
        self.menubar = Menu(master)
        
        self.list_index=0
        self.list_selected_index=0
    
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='New'       , underline=0, command=        self.add_character                , accelerator='Ctrl+N'      )
        self.filemenu.add_command(label='Remove'    , underline=0, command=        self.remove_character             , accelerator='Ctrl+R'      )
        self.filemenu.add_command(label='Load'      , underline=0, command=        self.load_config                  , accelerator='Ctrl+L'      )
        self.filemenu.add_separator() #      ------------------
        self.filemenu.add_command(label='Save'      , underline=0, command=lambda: self.save_config(fpath=self.fpath), accelerator='Ctrl+S'      )
    
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_checkbutton(label='Always on top'     , underline=10, variable=self.always_on_top  , command=self.pin                              )
    
        self.menubar.add_cascade(label='Characters', underline=0, menu=self.filemenu)
        self.menubar.add_cascade(label='Config', underline=0, menu=self.editmenu)
    
        self.menubar.config(relief='flat')
    
        master.config(menu=self.menubar)
    
        self.bind_all('<Control-n>'      , lambda e: self.add_character()        )
        self.bind_all('<Control-r>'      , lambda e: self.remove_character()                )
        self.bind_all('<Control-s>'      , lambda e: self.save_config(fpath=self.fpath))
        self.bind_all('<Control-l>'      , lambda e: self.load_config()                )
        
        # gives weight to the cells in the grid
        master.grid()
        rows = 0
        while rows < 50:
            master.rowconfigure(rows, weight=1)
            master.columnconfigure(rows, weight=1)
            rows += 1
            
        self.tabControl = ttk.Notebook(master)
        
        # Defines and places the notebook widget
        self.tabControl.grid(row=1, column=0, columnspan=25, rowspan=49, sticky='NESW')
         
        # Adds tab 1 of the notebook
        page1 = ttk.Frame(self.tabControl)
        page1.pack(side = LEFT, expand=1, fill="both", padx=5, pady=5)
        self.tabControl.add(page1, text='Initiative')
        self.add_button = Button(page1, text="Add Char", fg="black", command = self.add_character)
        delete_button = Button(page1, text="Delete Char", fg="black", command = self.remove_character)
        self.roll_button = Button(page1, text="Roll Dice", fg="black", command = self.roll_initiative)
        clear_button = Button(page1, text="Clean", fg="black", command = self.remove_all_characters)
        self.next_button = Button(page1, text="Next Char", fg="black", command = self.next_character)
#         greenbutton.place(x = 20, y = 30, width=120, height=25)
#         greenbutton1.place(x = 20, y = 60, width=120, height=25)
        
        self.tree=ttk.Treeview(page1, selectmode=BROWSE, columns=("life", "one"))
        self.tree.column("#0", width=250, minwidth=250, stretch=True)
        self.tree.column("life", width=40, minwidth=40, stretch=True)
        self.tree.column("one", width=70, minwidth=70, stretch=True)
        self.tree.heading("#0", text="Character",anchor="w")
        self.tree.heading("life", text="HP",anchor="w")
        self.tree.heading("one", text="Initiative",anchor="w", command=lambda _col="one": self.treeview_sort_column(self.tree, _col, True))
#         
        
        self.tree.pack(side=TOP,fill=X)
        self.add_button.pack(side = LEFT, padx=5, pady=5, anchor="s")
        delete_button.pack(side = LEFT, padx=5, pady=5, anchor="s")
        self.roll_button.pack(side = LEFT, padx=5, pady=5, anchor="s")
        clear_button.pack(side = LEFT, padx=5, pady=5, anchor="s")
        self.next_button.pack(side = LEFT, padx=5, pady=5, anchor="s")
        self.next_button["state"] = "disabled"
        self.roll_button["state"] = "disabled"

        # Adds tab 2 of the notebook
        page2 = ttk.Frame(self.tabControl)
        self.tabControl.add(page2, text='Characters')        

        # Adds tab 2 of the notebook
        page3 = ttk.Frame(self.tabControl)       
        self.tabControl.add(page3, text='Monsters')  
        
        
        monsterList = self.load_monster_name() 

        selectButton = Button(page3, text='Select', underline = 0, command=self.selection)
        scrollbar = Scrollbar(page3, orient=VERTICAL)
        self.search_var = StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.update_list())
        self.listBoxFilter = Entry(page3, textvariable=self.search_var, width=13)
        self.monsterListBox = Listbox(page3, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.monsterListBox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listBoxFilter.pack(side=TOP, padx=5, pady=5, anchor="n")
        selectButton.pack(side=TOP, padx=5, pady=5, anchor="n")
        self.monsterListBox.pack(side=TOP, fill=BOTH, expand=1)
        for item in monsterList:
            self.monsterListBox.insert(END, item)
        self.monsterListBox.bind('<Double-1>', lambda x: selectButton.invoke())

        
        #html_label = HtmlFrame(page3, horizontal_scrollbar="auto", vertical_scrollbar=True)
        #html_label.pack(fill="both", expand=True)
        #html_label.set_content(self.html)

        # Adds tab 2 of the notebook
        page4 = ttk.Frame(self.tabControl)
        self.tabControl.add(page4, text='Spells')        
         
        # Adds tab 2 of the notebook
        page5 = ttk.Frame(self.tabControl)
        self.tabControl.add(page5, text='Rules')        

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)
    
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
    
        # reverse sort next time
        #tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def selection(self):
        try:
            self.load_monster(self.monsterListBox.selection_get())
            self.wm = popupWindowMonster(self.master)
             #self.popupmsg(self.monsterListBox.selection_get(), self.html)
        except:
            pass
        

    def update_list(self):
        search_term = self.search_var.get()
     
        monsterList = self.load_monster_name() 
        self.monsterListBox.delete(0, END)
     
        for item in monsterList:
            if search_term.lower() in item.lower():
                self.monsterListBox.insert(END, item)

if __name__ == '__main__':
    root = Tk()
    root.resizable(True,True)
    width = 400
    heigth = 400
    s_width = root.winfo_width()
    s_heigth = root.winfo_height()
    
    x = (s_width/2) - (width/2)
    y = (s_heigth/2) - (heigth/2)
    
    root.geometry("%dx%d+%d+%d" % (width, heigth, 100, 100) )
    
    icon = PhotoImage(data=b'R0lGODlhIAAgAKECAAAAAD9IzP///////yH5BAEKAAMALAAAAAAgACAAAAJ5nI85AOoPGZyxLUvzNVL7roDeISJl9XQqhjorx07iecosHVNzPpI339v4gq4f0QSsaZTKDBPoTEJbtl5zOGIEttzu9hoCeMcBsI8cEAjGZi1ZzZ7C0Oi2mB63deF47nO/1vclJbjFN5hyJ3hYJsXwCBkp+TRZOYlQAAA7')
    root.iconphoto(root, icon)

    def on_closing():
        title = root.title()
        if '*' in title:
            if askyesno('Unsaved changes!', 'There are unsaved changes!\r\nWould you like to quit anyway?'):
                root.destroy()
        else:
            if askyesno('Quit?', 'Really quit?'):
                root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)

    main = MainFrame(root)
#     main.grid()

    root.mainloop()
