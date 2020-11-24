import random
import re
import os
import base64
from cryptography.fernet import Fernet
from appfuncions import enckeyprov, savedata, saltprov, keyderive, quicksavedata, quickkeyderive
from zipfile import ZipFile
from kivymd.toast import toast
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDRoundFlatButton
from kivy.properties import ListProperty, StringProperty, BooleanProperty, NumericProperty, OptionProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from android.permissions import request_permissions, Permission


                
class ShowPassbox(MDCard):
    site_name=StringProperty()
    passw=StringProperty()
    set_title=StringProperty()
    flagforsavebutton = True
    focusevent= False
    set_label1=StringProperty()
    set_label2=StringProperty()
    
    def __init__(self, tempsitename, temppassw, temptitle, **kwargs):
        (super(ShowPassbox, self).__init__)(**kwargs)
        self.ids.btngrid.remove_widget(self.ids.confirmbutt)
        self.tempsitename = tempsitename
        self.temppassw = temppassw
        self.temptitle = temptitle
        self.ids.textgrid.remove_widget(self.ids.mlabel)
        self.ids.textgrid.remove_widget(self.ids.mpassw)
        self.remove_widget(self.ids.checkboxgrid)
        if self.temptitle == 'Password Details':
            self.ids.btngrid.remove_widget(self.ids.savebutt)
        if self.temptitle == 'Edit Your Details' or self.temptitle == 'Enter Details' or self.temptitle == 'Enter Details (Quick Save)':
            self.ids.btngrid.remove_widget(self.ids.delbutt)
            if self.temptitle == 'Enter Details (Quick Save)':
                self.size_hint = [0.9, 0.63]
                self.pos_hint = {'center_y':0.65,  'center_x':0.5}
                self.ids.textgrid.size_hint_y=0.65
                self.ids.cardlabel.size_hint_y=0.15
                self.ids.btngrid.size_hint_y=0.2
                self.ids.textgrid.add_widget(self.ids.mlabel)
                self.ids.textgrid.add_widget(self.ids.mpassw)
                self.add_widget(self.ids.checkboxgrid,2)

    
    def delconfirm(self):
        self.set_title = "Warning: Delete details?"
        self.ids.btngrid.remove_widget(self.ids.delbutt)
        self.ids.btngrid.add_widget(self.ids.confirmbutt)
    
    def bindevent(self,*args):
        if self.temptitle=="Password Details":
            self.focusevent= True
        else:
            self.focusevent= False
    
    def showsavebutton(self,textdata):
        if self.flagforsavebutton and self.focusevent:
            self.ids.btngrid.remove_widget(self.ids.delbutt)
            self.ids.btngrid.add_widget(self.ids.savebutt)
            self.flagforsavebutton= False
        else:
            pass

    def saveedit(self):
        global passwlist, savedlist
        if self.temptitle=="Password Details":
            self.delete(self.tempsitename,1)
        if len(self.ids.site.text)==0 or len(self.ids.passw.text)==0:
            toast("Nothing saved") 
        elif self.temptitle=="Edit Your Details":
      	  del passwlist[self.tempsitename]
      	  passwlist[self.ids.site.text]="**usr**"+self.ids.passw.text
      	  self.ids.site.text=""
      	  self.ids.passw.text=""
        elif self.temptitle == 'Enter Details (Quick Save)':
            quicksavedata(self.ids.site.text, self.ids.passw.text, self.ids.mpassw.text)
            self.ids.site.text = ''
            self.ids.passw.text = ''
        else:
            site_name=self.ids.site.text
            passw=self.ids.passw.text
            savedlist.append(site_name)
            passwlist[site_name]=passw
            global saveflag
            saveflag=True
            self.ids.site.text=""
            self.ids.passw.text=""

    def delete(self,site_name,delflag=0):
        global passwlist, savedlist
        del passwlist[site_name]
        savedlist.remove(site_name)


class CustomButton(MDFlatButton):
    pass

class Mainlayout(Screen):
    
    def __init__(self,**kwargs):
        super(Mainlayout,self).__init__(**kwargs)
        
    def on_pre_enter(self):
        if os.path.isfile('.tempdata'):
            saltfile = open('.tempsalt', 'rb')
            salt = saltfile.read()
            saltfile = open('.tempsalt', 'wb')
            saltfile.close()
            datfile = open('.tempdata', 'rb')
            datstr = datfile.read()
            datfile.close()
            os.remove('.tempdata')
            datlist = datstr.split(b'::')[:-1]
            for passw in passwlist:
                if passwlist[passw][:7] == '**usr**':
                    password = passwlist[passw][7:]
            tempkey = quickkeyderive(salt, password)
            encmech = Fernet(tempkey)
            try:
                for dat in datlist:
                    decstr = str(encmech.decrypt(dat))[2:-1]
                    username, password = decstr.split(':')
                    passwlist[username] = password
                    savedlist.append(username)
                toast('Added quick saved passwords')
            except:
                toast("Unable to add quick saved password\nMaybe master password entered was incorrect")
        self.refresh()

    	
    def refresh(self):
        self.ids.passlist.clear_widgets()
        if len(savedlist)>0:
            savedlist.sort()
            splitlett=savedlist[0][0]
            self.ids.passlist.add_widget(MDLabel(text=splitlett.upper(),font_size="25sp",size_hint=[1,None],theme_text_color="Custom", text_color=[0.1176,0.7878,0.2667,1]))
            for s in range(len(savedlist)):
                if savedlist[s][0]==splitlett:
                	self.ids.passlist.add_widget(CustomButton(text=savedlist[s]))
                else: 
                	splitlett=savedlist[s][0]
                	self.ids.passlist.add_widget(MDLabel(text=splitlett.upper(),font_size="25sp", size_hint=[1,None],theme_text_color="Custom", text_color=[0.1176,0.7878,0.2667,1]))
                	self.ids.passlist.add_widget(CustomButton(text=savedlist[s]))
    
    def backup(self):
        global key
        random.seed()
        saltlist=saltprov(2)
        savedsalt=saltlist[random.randint(0,3)]
        usrsalt=""
        for passw in passwlist:
            	if passwlist[passw][:7]=="**usr**":
            		usrsalt=passwlist[passw][7:]
        key = enckeyprov(usrsalt, savedsalt, 19)
        savedata(passwlist, key)
        backupzip = ZipFile(filepath+"mpbackup.zip","w")
        backupzip.write(".data")
        backupzip.write(".salt")
        backupzip.close()
        saltlist=saltprov(1)
        savedsalt=saltlist[random.randint(0,2)]
        key = enckeyprov(usrsalt, savedsalt, 18)
        toast("Backup taken successfully")
    
    def read(self,selectedlabel):   
        self.p = ShowPassbox(selectedlabel,passwlist[selectedlabel], "Password Details")
        self.p.site_name = selectedlabel
        self.p.passw = passwlist[selectedlabel]
        self.p.set_title="Password Details"
        self.p.set_label1="  Site/App:"
        self.p.set_label2="  Password:"
        self.ids.passlist.disabled=True
        self.ids.fab.disabled=True
        self.ids.mainbox.add_widget(self.p,2)
        self.ids.scrollpasslist.size_hint_y=0.55
        self.ids.mainbox.padding= ["0dp","20dp","0dp","0dp"]
        
        
    def showAddbox(self,instance):
        self.ids.fab.close_stack()
        if instance.icon=="plus":
            self.p=ShowPassbox("","", "Enter Details")
            self.p.set_title="Enter Details"
            self.p.site_name=""
            self.p.passw=""
            self.p.set_label1="  Site/App:"
            self.p.set_label2="  Password:"
            self.ids.passlist.disabled=True
            self.ids.fab.disabled=True
            self.ids.mainbox.add_widget(self.p,2)
            self.ids.scrollpasslist.size_hint_y=0.55
            self.ids.mainbox.padding= ["0dp","20dp","0dp","0dp"]
           
        if instance.icon=="circle-edit-outline":
            username=""
            password=""
            for passw in passwlist:
            	if passwlist[passw][:7]=="**usr**":
            		username=passw
            		password=passwlist[passw][7:]
            	
            self.p=ShowPassbox(username,password,"Edit Your Details")
            self.p.set_title="Edit Your Details"
            self.p.site_name=username
            self.p.passw=password
            self.p.set_label1="Username:"
            self.p.set_label2="Password:"
            self.ids.passlist.disabled=True
            self.ids.fab.disabled=True
            self.ids.mainbox.add_widget(self.p,2)
            self.ids.scrollpasslist.size_hint_y=0.55
            self.ids.mainbox.padding= ["0dp","20dp","0dp","0dp"]
            
        if instance.icon=="floppy":
            toast("Taking backup...")
            self.backup()
        
        if instance.icon=="folder-key":
            global key
            toast("Generating new keys...")
            saltlist=saltprov(1)
            random.seed()
            savedsalt=saltlist[random.randint(0,2)]
            usrsalt=""
            for passw in passwlist:
            	if passwlist[passw][:7]=="**usr**":
            		usrsalt=passwlist[passw][7:]
            key=enckeyprov(usrsalt, savedsalt, 18)
            toast("New keys generated")
        
        if instance.icon=="help":
            WarnDialog().open()
    
    def closePassBox(self):
        self.ids.scrollpasslist.size_hint_y=1
        self.ids.mainbox.padding= ["0dp","10dp","0dp","0dp"]
        self.ids.mainbox.remove_widget(self.p)
        self.ids.passlist.disabled=False
        self.ids.fab.disabled=False
        self.refresh()

  
class Loginlayout(Screen):
    set_boxsize=ListProperty()
    setpos=NumericProperty()
    set_label=StringProperty()
    set_color=ListProperty()
    restgridsize=NumericProperty()
    btntext=StringProperty()
    set_passhint=StringProperty()
    loginpass=[]
    set_width=NumericProperty()
    
    def __init__(self,**kwargs):
        super(Loginlayout,self).__init__(**kwargs)
        self.set_color=[1,1,1,1]
        global newuserflag
        if newuserflag==1:
            self.set_label='Welcome New User!'
            self.set_boxsize=[1,0.75]
            self.setpos=0.86
            self.restgridsize=0.7
            self.btntext='CONFIRM'
            self.set_passhint='Enter Master Password'
        else:
            self.set_label='Enter Master Password'
            self.set_passhint=''
            self.btntext='ENTER'
            self.restgridsize=0.4
            self.set_boxsize=[1, 0.6]
            self.setpos=0.89
        Clock.schedule_once(self.removefield,1)
    
    def removefield(self, *args):
        if newuserflag == 0:
            self.ids.loginbox.remove_widget(self.ids['username'])
            self.ids.restoregrid.remove_widget(self.ids.restorebtn)
        else:
            self.ids.restoregrid.remove_widget(self.ids.quickbtn)

    def quicksave(self):
        self.clear_widgets()
        self.p = ShowPassbox('', '', 'Enter Details (Quick Save)')
        self.p.set_title = 'Enter Details (Quick Save)'
        self.p.site_name = ''
        self.p.passw = ''
        self.p.set_label1 = '  Site/App:'
        self.p.set_label2 = '  Password:'
        self.add_widget(self.p)

    def closePassBox(self):
        self.clear_widgets()
        self.add_widget(self.ids.loginbox)
        self.on_enter()

    
    def restore(self,checkpassw):
        global savedsalt, saltlist
        if not os.path.isfile(filepath+"mpbackup.zip"):
            toast("No backup file found. Enter login details")
        else:
            mpbackup=ZipFile(filepath+"mpbackup.zip")
            mpbackup.extractall(filepath)
            saltfile=open(filepath+".salt","rb")
            saltstr=saltfile.read()
            saltlist=saltstr.split(b"::")
            saltfile.close()
            self.check(checkpassw, 1)
    
    def check(self,checkpassw, restoreflag=0):
        global usrsalt, loginapprovflag, key, savedsalt, saltlist
        global passwlist, savedlist, newuserflag
        if self.ids.checkbtn.text=="CONFIRM" and restoreflag==0:
            if len(self.ids.loginpassw.text)<7 or len(self.ids.username.text)<7:
                toast("Username, Password should be at least 7 characters")
            else:
                passwlist[self.ids.username.text]="**usr**"+self.ids.loginpassw.text
                toast("Signing up...")
                usrsalt=self.ids.loginpassw.text
                key = enckeyprov(usrsalt, savedsalt, 18)
                self.manager.current='main'
                toast("Welcome "+self.ids.username.text+"!\nSaving details...")
                loginapprovflag=1
        else:
            iterindex=0
            if restoreflag==1:
                toast("Trying to restore data...")
                datfile=open(filepath+".data","rb")
                encdatastr=datfile.read()
                iterindex=19
                datfile.close()
            else:
                toast("Trying to log in...")
                datfile=open(".data","rb")
                encdatastr=datfile.read()
                iterindex=18
                datfile.close()
            usrsalt=self.ids.loginpassw.text
            result="**error**"
            progress=0
            for salt in saltlist:
                result=keyderive(usrsalt, salt, encdatastr, iterindex)
                if result!="**error**":
                    savedsalt=salt
                    break
                if restoreflag==1:
                    progress+=25
                    toast("Trying to restore data: "+str(progress)+"%")
            if result!="**error**":
                finalstr,key=result.split("::key::")
                key=bytes(key, "ascii")
                templist = finalstr.split("##next##")
                savedlist=[]
                passwlist={}
                for saves in templist:
                	site_name, passw=saves.split(":")
                	passwlist[site_name]=passw
                	if passw[:7]!="**usr**":
                		savedlist.append(site_name)
                loginapprovflag=1
                savedlist.sort()
                if restoreflag==1:
                    os.remove(filepath+".data")
                    os.remove(filepath+".salt")
                    os.remove(filepath+"mpbackup.zip")
                    saltfile=open(".salt","wb")
                    saltstr=savedsalt+b"::"+os.urandom(32)+b"::"+os.urandom(32)
                    saltfile.write(saltstr)
                    saltfile.close()
                    toast("Backup restored successfully\nDon't leave. Loading password list...")
                    key=enckeyprov(self.ids.loginpassw.text, savedsalt, 18)
                else:
                    toast("Logged in successfully\nLoading password list...")
                self.manager.current='main'
                   
            else:
                if restoreflag==1:
                	toast("Fill correct previous login details to restore backup")
                else:
                    toast("Invalid password")
                    self.set_label='Incorrect Password'
                    self.set_color=[1,0,0,1]

class WarnDialog(Popup):
	pass

class AppLayout(FloatLayout):
    def opendialog(self):
    	self.warndialog=WarnDialog()
    	self.warndialog.open()
    
    def removewarn(self):
    	self.remove_widget(self.ids.warnfab)

class ManagePassApp(MDApp): 
    def __init__(self,**kwargs):
        super(ManagePassApp,self).__init__(**kwargs)
        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]) 
        if not os.path.exists("/storage/emulated/0/Android/data/com.managepass"):
            os.mkdir("/storage/emulated/0/Android/data/com.managepass")
        global passwlist, savedlist, newuserflag, savedsalt, saltlist
        newuserflag=0
        if not (os.path.isfile(".salt")):
            random.seed()
            saltlist=saltprov(1)
            savedsalt=saltlist[random.randint(0,2)]
            f2=open(".data","wb")
            f1=open(".tempsalt","wb")
            f1.close()
            f2.close()
            newuserflag=1
        else:
            saltlist=saltprov()
        f2=open(".data",'rb')
        if len(f2.readlines())==0:
            newuserflag=1
        f2.close()
        passwlist={}
        savedlist=[]
        
    def build(self):
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="Green"
        return AppLayout()
    
    def on_stop(self):
        global loginapprovflag
        toast("Encrypting data...")
        if loginapprovflag==1:
        	savedata(passwlist, key)
        	self.current='login'
        	loginapprovflag=0
        	
saveflag = False
global savedsalt, saltlist
saltlist=[]
savedsalt=b''
loginapprovflag=0
global filepath
#filepath=''
filepath="/storage/emulated/0/Android/data/com.managepass/"
minwdt, minhgt = Window.size
ManagePassApp().run()
