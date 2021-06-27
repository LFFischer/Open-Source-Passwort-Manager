## Leon F. Fischer für UAS BS&RN 2021 ##
## Version 1.0 for Windows##
import os
from re import T
import string
import pyperclip #pip install pyperclip  ##Zum zwischenablage-bearbeiten
import keyboard #pip install keyboard   ##for menu selects via tasten
from cryptography.fernet import Fernet  #pip3 install cryptography  ## Für verschlüsselung
from getpass import getpass     ##Für sichere eingaben
import threading                ##Für background timer
import secrets                  ##Für random password generation from string parts



## Variablen

Where='menu' # In welchem menu wir uns befinden                  
selected = 1 # welcher Menü Punkt ausgewählt ist
move=True    # Ob cursor sich bewegen darf
masteraccsess=False # Ob das masterpasswort from eine zeitspanne bestätigt ist
inclip=False  # Ob etwas in der Zwischenablage ist

lcase = True  # Für alphabet, siehe unten
ucase = True    
dcase = True
pcase = True

buffer=''     #Buffer für masterpasswort änderung
todel=''      #Zu löschender string
time=300.0  #Timer für masteraccsess
ctime=30.0  #Timer für clipboard reset

## Text der Menü punkte

menu=['Recall\t','New\t','Options\t','Support Us ','\x1b[6;31m'+'<-Exit\t'+'\x1b[0m']
options=['Delete Password\t','Change Master-Password\t','Change Password Interval\t','Request Plaintext Table\t','\x1b[6;33m'+'<-Back\t'+'\x1b[0m']
newpass=['Generate'+'\x1b[6;32m'+'(Recomended)'+'\x1b[0m\t','Custom\t','\x1b[6;33m'+'<-Back\t'+'\x1b[0m']
deleteit=['Confirm','\x1b[6;33m'+'<-Back\t'+'\x1b[0m']
length=5



def  testformaster(): #masterpassword tester from file, returns Bool
        global masteraccsess
        global buffer
        accses=False
        for d in range(1, 4):
            testformaster=getpass("Input Masterpassword to confirm: ")
            if(testformaster==''):
                break
            with open('verysecure.txt','rt') as file:
                for line in file:
                    #print('1') 
                    if testformaster in line:
                        #print('2')
                        nline=line.split("=")
                        #print(nline)
                        nline2=nline[1].split('\n')
                        #print(nline2)
                        if(nline[0]=='Masterpass'):
                            #print('3')
                            if nline2[0]==testformaster:
                                #print('4')            
                                accses=True
                                buffer=testformaster
                                masteraccsess=True
                                file.close()
                                mastertimer()
                                return accses
                                break
               
                    
            if(accses==False):
                print("Please try again: ")
                

        if(accses==False):
            clear() #Clears full console
            print('Security Error press any key to return.')
            input()
        return accses

def getbuffer():            ## Returns masterpassswort from buffer is accsess is allowed
    if masteraccsess==True:
        if buffer != '':
            return buffer

def cliptimer(): ## starts 30sek timer that calls cliptimer2()
    global inclip
    if(inclip==True):
        threading.Timer(30.0,cliptimer2).start()

def cliptimer2(): ## Executes clipboard purge when called
    pyperclip.copy('')
    global inclip
    inclip=False

def mastertimer(): ## Triggers mastertimer2() after a set time, default:5min
    global masteraccsess
    if(masteraccsess==True):
        threading.Timer(time, mastertimer2).start()

def mastertimer2(): ## Resets buffer and disallowes masteraccsess
    global masteraccsess
    global buffer
    #print('lul')
    #input()
    buffer=''
    masteraccsess=False
        


def show_options(): #displays options menu
    global move
    move=True
    global selected
    global length
    length =6
    global Where
    Where='options'
    print("\n" * 2)
    print('\x1b[6;33m'+'Choose an option via arrow keys:'+'\x1b[0m')
    for i in range(1, length):
        print(options[i-1], "{1}".format(i,"\x1b[6;33m"+"<-"+"\x1b[0m" if selected == i else " ")) #prints menu and moves < selector thingy when triggered
    print("\nPress Enter to continue...")    

def show_newpass(): #displays new passwort menu
    global move
    move=True
    clear()
    global selected
    global length
    length =4
    global Where
    Where='newpass'
    print("\n" * 2)
    print('\x1b[6;34m'+'Choose an option via arrow keys:'+'\x1b[0m')
    for i in range(1, length):
        print(newpass[i-1], "{1}".format(i,"\x1b[6;49m"+"<-"+"\x1b[0m" if selected == i else " ")) #prints menu and moves < selector thingy when triggered
    print("\nPress Enter to continue...") 

def show_alphabet(): # generates Password generation options and shows them toggles on or off
    global lcase,ucase,dcase,pcase
    global move
    move=True
    global selected
    global length
    length =6
    global Where
    Where='alpha'
    alphaoptions=['Lowercase='+str(lcase),'Uppercase='+str(ucase),'Digits='+str(dcase),'Puncuation='+str(pcase),"\x1b[6;32m"+'Confirm?'+"\x1b[0m"]
    print("\n" * 2)
    print('\x1b[6;33m'+'Choose an option via arrow keys:'+'\x1b[0m')
    for i in range(1, length):
        print(alphaoptions[i-1], "{1}".format(i,"\x1b[6;33m"+"<-"+"\x1b[0m" if selected == i else " ")) 
        #prints menu and moves <- selector thingy when triggered with help from up & down functions
    print("\nPress Enter to change selected option...\nPress Enter on '\x1b[6;32m"+'Confirm?'+"\x1b[0m' to confirm...")   

def show_delete(): #displays delete confirm menu
    global move
    global todel
    move=True
    clear()
    global selected
    global length
    length =3
    global Where
    Where='delete'
    print("\n" * 3)
    print('\x1b[6;34m'+'You are about to delete:'+'\x1b[6;31m'+'"'+todel+'"'+'\x1b[0m','\x1b[0m')
    print('\x1b[6;34m'+'Choose an option via arrow keys:'+'\x1b[0m')
    for i in range(1, length):
        print(deleteit[i-1], "{1}".format(i,"\x1b[6;34m"+"<-"+"\x1b[0m" if selected == i else " ")) #prints menu and moves < selector thingy when triggered
    print("\nPress Enter to continue...")   

def show_menu(): #displays main menu
    global move
    move=True
    global selected
    global length
    length =6
    global Where
    Where='menu'
    print("\n" * 2)
    print('\x1b[6;32m'+'Choose an option via arrow keys:'+'\x1b[0m')
    for i in range(1, length):
        print(menu[i-1], "{1}".format(i,"\x1b[6;32m"+"<-"+"\x1b[0m" if selected == i else " ")) 
        #prints menu and moves < selector thingy when triggered
    print("\nPress Enter to continue...")

def up(): # moves cursor up
        global selected
        global move
        if(move==True):
            if selected == 1:
                return
            selected -= 1
            clear()
            if(Where=='menu'):
                show_menu()
            elif(Where=='options'):
                show_options()
            elif(Where=='newpass'):
                show_newpass()
            elif(Where=='delete'):
                show_delete()
            elif(Where=='alpha'):
                show_alphabet()

def down(): # moves cursor down
        global selected
        global move
        if(move==True):
            if selected == length-1:
                return
            selected += 1
            clear()
            if(Where=='menu'):
                show_menu()
            elif(Where=='options'):
                show_options()
            elif(Where=='newpass'):
                show_newpass()
            elif(Where=='delete'):
                show_delete()
            elif(Where=='alpha'):
                show_alphabet()

keyboard.add_hotkey('up', up) # triggers up() when arrow up is pressed
keyboard.add_hotkey('down', down) # triggers down() when arrow down is pressed

def recallpassword(): # finds,cuts, and presents your selected passwords 
                      # if masterpassword is correct
        global inclip
        exists=False
        clear()
        lookup1=input("Recall password for which service?  :") 
        lookup2='->'+lookup1.lower()
        with open('verysecure.txt','rt') as file:
            for line in file:
                if lookup2 in line.lower():
                    nline=line.split("=>")
                    word=nline
                    if(lookup2 in nline[0].lower()):
                        nline=nline[0].split("->")  

                        exists=True
                        break

                
                
        
        if(exists==True):
            if masteraccsess==True:
                word=word[1].split('_>')
                print(word)
                clear()
                pyperclip.copy(word[0])
                print('Success, your password for '+'\x1b[6;32m'+nline[1]+'\x1b[0m'+' has been copied to clipboard!\n')
                print('Use username/login: \n'+word[1])
            elif masteraccsess==False:
                if(testformaster()==True):
                    word=word[1].split('_>')
                    clear()
                    pyperclip.copy(word[0])
                    print('Success, your password for '+'\x1b[6;32m'+nline[1]+'\x1b[0m'+' has been copied to clipboard!\n')
                    print('Use username/login: \n'+word[1])
                

            print('Never share your passwords with unautherised persons!\n')
            print('Thank you for using this service!\nPlease consider supporting us, simply select option 4-Support in the main menu.')
            inclip=True
            cliptimer()
            input()
            clear()
            show_menu()

        else:
            print('"',lookup1,'"', 'does not exist!\n You can generate a new password by selecting "new" in the Main-menu.')
            input()

def save(title,passw,uname): # puts provided strings into the file
    saveline='->'+title+'=>'+passw+'_>'+uname
    f=open('verysecure.txt','a+')
    f.write(saveline+"\n")
    f.close

    return True

def getalphabet(): # switches the password generation options valiables on or off, 
                   # to be displayed when the menu is printed
    clear()        # it mostly just swaps True for False and False for True
    global lcase,ucase,dcase,pcase
    alphabet=''
    #selected = 1
    show_alphabet()
    input()
    if(selected==1): #lower
        if(lcase==True):
            lcase=False
        elif(lcase==False):
            lcase=True
        getalphabet()
    if(selected==2):
        if(ucase==True):
            ucase=False
        elif(ucase==False):
            ucase=True
        getalphabet()
    if(selected==3):
        if(dcase==True):
            dcase=False
        elif(dcase==False):
            dcase=True
        getalphabet()
    if(selected==4):
        if(pcase==True):
            pcase=False
        elif(pcase==False):
            pcase=True
        getalphabet()
    if(selected==5):
        if lcase+ucase+dcase+pcase == False: #Checks if at least one option is selected
            print('At lest one option needs to be active!')
            input()
            getalphabet()
        else:  #adds selected character sets to a string to have a password generated from them
            if lcase == True:
                alphabet=alphabet+string.ascii_lowercase
            if ucase == True:
                alphabet=alphabet+string.ascii_uppercase
            if dcase == True:
                alphabet=alphabet+string.digits
            if pcase == True:
                alphabet=alphabet+string.punctuation

            return alphabet #Returns new string to newpassword()



def newpassword(): # Makes a new password and takes you through menues to help with that
    clear()
    global selected,inclip
    global move
    title=input("New password Title: ")
    if checkexistance(title)==False:
        selected = 1
        show_newpass()
        input()
        if(selected==1): #Option 1: Password generation service
            move=False
            clear()
            while True:
                uname=input('Username: ')
                if uname != '':
                    break
                else: print('Username cannot be empty!')
            print('Input Password length\n20+ is recomended!')
            length=int(input('Password length (in numbers):'))
            if length==0:
                length=20
            elif length=='':
                length=20

            selected=1
            alphabet = getalphabet() #alphabet from above arives here...

            while True:
                
                newword = ''.join(secrets.choice(alphabet) for i in range(int(length))) # ...and is used to make a password

                if '=>' in newword:  # these test if things that would break the save system are part of the password
                    print()
                elif '->' in newword: # a new password is made if that's the case
                    print()
                elif '_>' in newword:
                    print()
                elif '\n' in newword:
                    print()
                else:
                    break
            


            
            if(save(title,newword,uname)==True): # Password gets saves via the save function explained above
                clear()
                print('Password saved succsessfully and coppied into clipboard for 30 secounds,\nPress any key to return.')
                pyperclip.copy(newword) # Password gets coppied to clipboard
                inclip=True 
                cliptimer() # timer starts to clear the clipboard after 30seks
                newword=''
                input()
            
        elif(selected==2): # Option 2: Input your own password
            move=False
            clear()
            while True:
                
                    while True:
                        print('We recomend using a mix of lettes,symbols, and numbers.') # Free tech tip 
                        newword=input("Type new Password: ")
                        if(newword!=''):

                            if '=>' in newword:  # these test if things that would break the save system are part of the password
                                print()
                            elif '->' in newword: # a new password is made if that's the case
                                print()
                            elif '_>' in newword:
                                print()
                            elif "\n" in newword:
                                print()
                            else:
                                break
                            clear()
                            print('Password contains forbiden character sets!')
                        else:
                            print('Password cannot be empty!')
                    while True:
                        uname=input('Username: ')
                        if uname != '':
                            break
                        else: print('Username cannot be empty!')
                    if(save(title,newword,uname)==True): # saves custom password just like it would above
                        print('Password saved succsessfully,\nPress any key to return.')
                        input()
                        break
                

        elif(selected==3): # option 3: Back, returns to main menu
            move=False
            input()
    else:
        print('A password with that name already exists!')
        print('To update a password please delete it first.')
        print("\nPress Enter to continue...") 
        input()
            
def checkexistance(lookup1): # tests if an input is already in the Title section
            clear()
            exists=False 
            if(True):
                lookup2='->'+lookup1.lower()
                with open('verysecure.txt','rt') as file:
                    for line in file:
                        if lookup2 in line:
                            nline=line.split("=>")
                            if(lookup2 == nline[0]):                        
                                exists=True
                                file.close
                                break
            return exists

def statusisenc(): # Tests if the file was is encrypted when the programm is started
    status=True
    with open('verysecure.txt','rt') as file:
                    for line in file:
                        if 'File==OK' in line:
                            status=False # It's supposed to be!
    return status

def dooptions(): # The options menu
        global Where
        global selected
        global move
        selected=1
        Where='options'
        clear()
        again=True
        show_options()
        input()

        if(selected==1): #Option 1: delete a password
            clear()
            global todel
            exists=False 
            move=False
            delete=''

            lookup1=input("Delete password for which service?  :") 
            lookup2='->'+lookup1.lower()
            with open('verysecure.txt','rt') as file:
                for line in file:
                     if lookup2 in line.lower():
                        nline=line.split("=>")
                        if(lookup2 in nline[0].lower()):
                            nline=nline[0].split("->") 
                            todel=nline[1].upper()                       
                            exists=True
                            delete=line
                            file.close
                            break
            if exists==True:
                selected=1
                show_delete()
                input()
                if(selected==1): #delete
                    clear()
                    exists=False 
                    move=False
                    login=False
            
                    if masteraccsess==False:
                        if(testformaster()==True):
                            login=True
                    elif masteraccsess==True:
                        login=True
                    
                    if login==True:
                        with open('verysecure.txt', 'r') as file:
                            data = file.read().replace(delete, '')
                            file.close()
                            
                            
                        
                        file = open('verysecure.txt','w')
                        file.write(data)
                        file.close()
                        data=''
                        print('Password delete succsessfully!')
                        print("\nPress Enter to continue...") 
                        input()
                if(selected==2): #abort
                    clear()
                    exists=False 
                    move=False

                    
            else:
                print('"',lookup1,'"', 'does not exist!\n You can generate a new password by selecting "new" in the Main-menu.')
                input()


            
                

            
            

    #______________________________________________________________________________________________________________________________________                

        elif(selected==2): #Option 2: change masterpassword
            move=False
            login=False
            clear()
            if masteraccsess==False:
                if(testformaster()==True):
                    login=True
            elif masteraccsess==True:
                login=True
            
            if login==True:
                delete='Masterpass='+getbuffer()
                Newpass1=input('New Password: ')
                Newpass2=input('New Password again: ')
                if(Newpass1==Newpass2):  # new pasword need to match
                    with open('verysecure.txt', 'r') as file:
                        new='Masterpass='+Newpass2 
                        data = file.read().replace(delete,new) # old password gets replaced with the new one
                        file.close()
                        
                    
                        file = open('verysecure.txt','w')
                        file.write(data)
                        file.close()
                        Newpass1=''
                        Newpass2=''
                        data=''
                        clear()
                        print('Password chnaged succsessfully!')
                        input()
                        clear()
                        
                else:
                    print("Passwords don't match!")
                    input()
                    clear()
                    
                    

        #______________________________________________________________________________________________________________________________________
        elif(selected==3): #Option 3: change timer
            global time
            move=False
            login=False
            if(masteraccsess==False):
                if testformaster()==True:
                    login=True
            elif masteraccsess==True:
                login=True

            
            if login==True:
                timer=input('New logout interval in secounds: ')
                time=int(timer) # timer gets chnaged until programm is closed
                mastertimer()
                print('Timer settings saved.\nTimer reset.')
                input('Press any key to continue: ')


        #______________________________________________________________________________________________________________________________________
        elif(selected==4): #Option 4: print plaintext table - Prints full file
            move=False
            login=False
            if(masteraccsess==False):
                if testformaster()==True:
                    login=True
            elif masteraccsess==True:
                login=True

            if(login==True):
                with open('verysecure.txt', 'r') as file:
                    plain=file.read()
                    clear()
                    print(plain)
                    plain=''
                    file.close()
                    input('Press any key to return:')        
        #______________________________________________________________________________________________________________________________________
        elif(selected==5): #back to main
            move=False
            again=False


        if(again==True):
            dooptions()
            

# Not in readable code for security! 
# This function would create or overwrite the key.key file 
# def write_key(): 
#     """
#     Generates a key and save it into a file
#     """
#     key = Fernet.generate_key()
#     with open("key.key", "wb") as key_file:
#         key_file.write(key)

def load_key(): # Loads key from key.key file
    
    return open("key.key", "rb").read()

def encrypt(filename, key): # Used key to encrypt the data file
    
    f = Fernet(key)
   
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
   

    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def decrypt(filename, key): # Used key to decrypt the data file
    
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)

def clearvars(): # Clears potential security risks and the clipboard
    global buffer
    global todel
    global key
    buffer =''
    todel = ''
    key= ''
    pyperclip.copy('')



#-----------------------------------------------------------------
#main body start



clear = lambda: os.system('cls') # Defines clear for windows
file = "verysecure.txt" # defines target for en or de-cryption
key = load_key() # defines 'key' as the key.key files key


if(statusisenc()==False):  #Exeption handler in case of crash or unsafe shutdown of manager!
    clear()
    print('Plese always exit the program with the Exit option for security!')
    print("\nPress Enter to continue...")   
    input()
else:
    decrypt(file, key) # If the file is properly encrypted, it decrypts it








while True: # Main menu will run in a loop until exited

    
    clear()
    print('\nWelcome to Passwordmanager.')
    print('What would you like to do?')

    

    
    show_menu()
    input()

    if(selected==1):
        move=False
        recallpassword() #See above
        
    elif(selected==2):
        move=False
        newpassword() #See above

    elif(selected==3):
        move=False
        dooptions() #See above
            
            
    elif(selected==4): # Offers a good option to support indie open source development
        move=False
        clear()
        print('Donations are always welcome!')
        print('https://www.paypal.com/paypalme/thisisnotascamiswear','\n\n\n\n')
        input()
    
    elif(selected==5):# exits the programm by exiting the loop
        clear()
        break
    
    clear()
    selected = 1

encrypt(file, key)# Encrypts file before closing
clearvars()       # Clears varibales that will not be cleared by a timer



    
        

    
    
    
