from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import os
from django.core.files.storage import FileSystemStorage
import pymysql
import pyaes, pbkdf2, binascii, os, secrets
import matplotlib.pyplot as plt
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import base64
import io
import cv2

global uname, resume_name

def getKey(): #generating AES key based on Diffie common secret shared key
    password = "s3cr3t*c0d3"
    passwordSalt = str("0986543")#get AES key using diffie
    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
    return key

def encrypt(plaintext): #AES data encryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    ciphertext = aes.encrypt(plaintext)
    return ciphertext

def decrypt(enc): #AES data decryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    decrypted = aes.decrypt(enc)
    return decrypted

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})  

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})

def UserLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumebuilder',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    uname = username
                    index = 1
                    break		
        if index == 1:
            context= {'data':'welcome '+uname}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'UserLogin.html', context)        

def SignupAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        fullname = request.POST.get('t3', False)
        contact = request.POST.get('t4', False)
        gender = request.POST.get('t5', False)
        email = request.POST.get('t6', False)
        address = request.POST.get('t7', False)
        edu1 = request.POST.get('t8', False)
        edu2 = request.POST.get('t9', False)
        edu3 = request.POST.get('t10', False)
        edu4 = request.POST.get('t11', False)
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumebuilder',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"
                    break
        if output == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumebuilder',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO signup VALUES('"+username+"','"+password+"','"+fullname+"','"+contact+"','"+gender+"','"+email+"','"+address+"','"+edu1+"','"+edu2+"','"+edu3+"','"+edu4+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = 'Signup Process Completed'
        context= {'data':output}
        return render(request, 'Signup.html', context)
      
def UpdateProfile(request):
    if request.method == 'GET':
        global uname
        password=""
        fullname=""
        contact=""
        gender=""
        email=""
        address=""
        edu1=""
        edu2=""
        edu3=""
        edu4=""
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumebuilder',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM signup where username='"+uname+"'")
            rows = cur.fetchall()
            for row in rows:
                uname = row[0]
                password = row[1]
                fullname = row[2]
                contact = row[3]
                gender = row[4]
                email = row[5]
                address = row[6]
                edu1 = row[7]
                edu2 = row[8]
                edu3 = row[9]
                edu4 = row[10]
        output = '<tr><td><font size="3" color="black">Username</b></td>'
        output += '<td><input type="text" name="t1" style="font-family: Comic Sans MS" size="30" value="'+uname+'" readonly/></td></tr>'
        output += '<tr><td><font size="3" color="black">Password</b></td><td><input name="t2" type="password" size="30" value="'+password+'"></td></tr>'
        output += '<tr><td><font size="3" color="black">Full&nbsp;Name</b></td><td><input type="text" name="t3" style="font-family: Comic Sans MS" size="50" value="'+fullname+'"></td></tr>'
        output += '<tr><td><font size="3" color="black">Contact&nbsp;No</b></td><td><input name="t4" type="Text" size="15" value="'+contact+'"></td></td></tr>'
        output += '<tr><td><font size="3" color="black">Gender</b></td><td><input name="t5" type="Text" size="15" value="'+gender+'" readonly></td></td></tr>'
        output += '<tr><td><font size="3" color="black">Email&nbsp;ID</b></td><td><input type="text" name="t6" style="font-family: Comic Sans MS" size="50" value="'+email+'"/></td></tr>'
        output += '<tr><td><font size="3" color="black">Address</b></td><td><input name="t7" type="Text" size="70" value="'+address+'"></td></td></tr>'
        output += '<tr><td><font size="3" color="black">Educational&nbsp;Details1</b></td><td><input name="t8" type="Text" size="70" value="'+edu1+'"></td></td></tr>'
        output += '<tr><td><font size="3" color="black">Educational&nbsp;Details2</b></td><td><input name="t9" type="Text" size="70" value="'+edu2+'"></td></td></tr>'
        output += '<tr><td><font size="3" color="black">Educational&nbsp;Details3</b></td><td><input name="t10" type="Text" size="70" value="'+edu3+'"></td></td></tr>'
        output += '<tr><td><font size="3" color="black">Educational&nbsp;Details4</b></td><td><input name="t11" type="Text" size="70" value="'+edu4+'"></td></td></tr>'
        output += '<tr><td></td><td><input type="submit" value="Submit"></td>'
        context= {'data1':output}
        return render(request, 'UpdateProfile.html', context)

def sharedResume(uname, sharing_users, resume_name):
    for i in range(len(sharing_users)):
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumebuilder',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO share VALUES('"+uname+"','"+sharing_users[i]+"','"+resume_name+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()        

def UpdateProfileAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        fullname = request.POST.get('t3', False)
        contact = request.POST.get('t4', False)
        gender = request.POST.get('t5', False)
        email = request.POST.get('t6', False)
        address = request.POST.get('t7', False)
        edu1 = request.POST.get('t8', False)
        edu2 = request.POST.get('t9', False)
        edu3 = request.POST.get('t10', False)
        edu4 = request.POST.get('t11', False)
        uname = username
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumebuilder',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "delete from signup where username='"+username+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumebuilder',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO signup VALUES('"+username+"','"+password+"','"+fullname+"','"+contact+"','"+gender+"','"+email+"','"+address+"','"+edu1+"','"+edu2+"','"+edu3+"','"+edu4+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            output = 'Profile updated successfully'
        context= {'data':output}
        return render(request, 'UserScreen.html', context)
    
def GenerateResume(request):
    if request.method == 'GET':
        global uname
        output = '<tr><td><font size="" color="black">Choose&nbsp;Shared&nbsp;Users</b></td><td><select name="t9" multiple>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumebuilder',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] != uname:
                    output += '<option value="'+row[0]+'">'+row[0]+'</option>'
        output += "</select></td></tr>"
        context= {'data1':output}
        return render(request, 'GenerateResume.html', context)

def getDetails(uname):
    password=""
    fullname=""
    contact=""
    gender=""
    email=""
    address=""
    edu1=""
    edu2=""
    edu3=""
    edu4=""
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumebuilder',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select * FROM signup where username='"+uname+"'")
        rows = cur.fetchall()
        for row in rows:
            uname = row[0]
            password = row[1]
            fullname = row[2]
            contact = row[3]
            gender = row[4]
            email = row[5]
            address = row[6]
            edu1 = row[7]
            edu2 = row[8]
            edu3 = row[9]
            edu4 = row[10]
    return uname, password, fullname, contact, gender, email, address, edu1, edu2, edu3, edu4            
    

def GenerateResumeAction(request):
    if request.method == 'POST':
        global uname, resume_name
        uname, password, fullname, contact, gender, email, address, edu1, edu2, edu3, edu4 = getDetails(uname)
        font = request.POST.get('t1', False)
        title = request.POST.get('t2', False)
        project1 = request.POST.get('t3', False)
        project2 = request.POST.get('t4', False)
        project3 = request.POST.get('t5', False)
        skills = request.POST.get('t6', False)
        activities = request.POST.get('t7', False)
        image = request.FILES['t8'].read()
        sharing_users = request.POST.getlist('t9')
        if os.path.exists("ResumeApp/static/test.png"):
            os.remove("ResumeApp/static/test.jpg")
        with open("ResumeApp/static/test.jpg", "wb") as file:
            file.write(image)
        file.close()

        plt.rcParams['font.family'] = font
        plt.rcParams['font.sans-serif'] = 'STIXGeneral'
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axvline(x=.5, ymin=0, ymax=1, color='#007ACC', alpha=0.0, linewidth=50)
        plt.axvline(x=.99, color='#000000', alpha=0.5, linewidth=300)
        plt.axhline(y=.88, xmin=0, xmax=1, color='#ffffff', linewidth=3)
        ax.set_facecolor('white')
        plt.axis('off')
        address = address.replace(",", "\n")
        skills = skills.replace(",", "\n")
        edu1 = edu1.replace(",", "\n")
        edu2 = edu2.replace(",", "\n")
        edu3 = edu3.replace(",", "\n")
        edu4 = edu4.replace(",", "\n")
        project1 = project1.replace(",", "\n")
        project2 = project2.replace(",", "\n")
        project3 = project3.replace(",", "\n")
        activities = activities.replace(",", "\n")

        plt.annotate('Resume', (.02,.98), weight='regular', fontsize=8, alpha=.6)
        plt.annotate(fullname, (.02,.94), weight='bold', fontsize=12)
        plt.annotate(title, (.02,.91), weight='regular', fontsize=10)
        plt.annotate(address, (.7,.906), weight='regular', fontsize=8, color='#ffffff')

        plt.annotate('Education Details1', (.02,.86), weight='bold', fontsize=10, color='#58C1B2')
        plt.annotate('Schooling', (.02,.832), weight='bold', fontsize=8)
        plt.annotate(edu1, (.04,.78), weight='regular', fontsize=6)
        plt.annotate('Education Details2', (.02,.745), weight='bold', fontsize=10, color='#58C1B2')
        plt.annotate('Intermediate', (.04,.71), weight='bold', fontsize=8)
        plt.annotate(edu2, (.02,.672), weight='regular', fontsize=6)
        plt.annotate('Education Details3', (.04,.638), weight='bold', fontsize=10, color='#58C1B2')
        plt.annotate('Graduation', (.02,.6), weight='bold', fontsize=8)
        plt.annotate(edu3, (.02,.54), weight='regular', fontsize=6)
        plt.annotate('Education Details4', (.02,.508), weight='bold', fontsize=10, color='#58C1B2')
        plt.annotate('Masters', (.02,.493), weight='bold', fontsize=8)
        plt.annotate(edu4, (.04,.445), weight='regular', fontsize=6)

        plt.annotate('Recent Project Development', (.02,.4), weight='bold', fontsize=10)
        plt.annotate('Project1', (.02,.385), weight='regular', fontsize=10)
        plt.annotate(project1, (.04,.337), weight='regular', fontsize=6)
        plt.annotate('Project2', (.02,.295), weight='regular', fontsize=10)
        #plt.annotate('Description', (.02,.28), weight='regular', fontsize=8, alpha=.6)
        plt.annotate(project2, (.04,.247), weight='regular', fontsize=6)
        plt.annotate('Project3', (.02,.185), weight='regular', fontsize=10)
        #plt.annotate('Description', (.02,.155), weight='bold', fontsize=10)
        plt.annotate(project3, (.02,.14), weight='regular', fontsize=6)
        plt.annotate('Skills', (.7,.8), weight='bold', fontsize=10, color='#ffffff')
        plt.annotate(skills, (.7,.56), weight='regular', fontsize=10, color='#ffffff')
        plt.annotate('Extra Activity', (.7,.43), weight='bold', fontsize=10, color='#ffffff')
        plt.annotate(activities, (.7,.345), weight='regular', fontsize=10, color='#ffffff')
        count = 0
        for root, dirs, directory in os.walk('ResumeApp/static/files'):
            for j in range(len(directory)):
                count = count + 1
        count += 1
        arr_code = mpimg.imread('ResumeApp/static/test.jpg')
        imagebox = OffsetImage(arr_code, zoom=0.5)
        ab = AnnotationBbox(imagebox, (0.84, 0.8))
        ax.add_artist(ab)
        resume_name = 'ResumeApp/static/files/'+uname+"_"+str(count)+".png"
        plt.savefig('ResumeApp/static/files/'+uname+"_"+str(count)+".png", dpi=300, bbox_inches='tight')
        img = cv2.imread('ResumeApp/static/files/'+uname+"_"+str(count)+".png")
        img = cv2.resize(img, (1222, 2601))
        os.remove('ResumeApp/static/files/'+uname+"_"+str(count)+".png")
        cv2.imwrite('ResumeApp/static/files/'+uname+"_"+str(count)+".png", img)
        with open('ResumeApp/static/files/'+uname+"_"+str(count)+".png", "rb") as file:
            data = file.read()
        file.close()
        enc = encrypt(data)
        os.remove('ResumeApp/static/files/'+uname+"_"+str(count)+".png")
        with open('ResumeApp/static/files/'+uname+"_"+str(count)+".png", "wb") as file:
            file.write(enc)
        file.close()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        sharedResume(uname, sharing_users, uname+"_"+str(count)+".png")
        context= {'data':'Resume Preview', 'img': img_b64}
        return render(request, 'UserScreen.html', context)

def Download(request):
    if request.method == 'GET':
        global username
        output = "Error in saving auth image"
        fname = request.GET.get('fname', False)
        with open ("ResumeApp/static/files/"+fname, "rb") as file:
            data = file.read()
        file.close()
        data = decrypt(data)
        response = HttpResponse(data, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % fname
        return response    
        
def ViewPrevious(request):
    if request.method == 'GET':
        global uname
        font = '<font size="" color="black">'
        output = '<table border="1" align="center" width="100%"><tr><th>'+font+'Resume Name</th><td>'+font+'Resume Image</th><td>'+font+'Download Resume</th></tr>'
        for root, dirs, directory in os.walk('ResumeApp/static/files'):
            for j in range(len(directory)):
                if uname in directory[j]:
                    with open ("ResumeApp/static/files/"+directory[j], "rb") as file:
                        data = file.read()
                    file.close()
                    data = decrypt(data)
                    if os.path.exists("ResumeApp/static/test.jpg"):
                        os.remove("ResumeApp/static/test.jpg")
                    with open ("ResumeApp/static/test.jpg", "wb") as file:
                        file.write(data)
                    file.close()    
                    output+="<tr><td>"+font+directory[j]+"</td>"
                    output += '<td><img src="static/test.jpg" height="200" width="200"/>'
                    output+='<td><a href=\'Download?fname='+directory[j]+'\'><font size=3 color=black>Click Here to Download</font></a></td></tr>'
        context= {'data':output}
        return render(request, "UserScreen.html", context)        
        
def ViewShared(request):
    if request.method == 'GET':
        global uname
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        font = '<font size="" color="black">'
        output = '<table border="1" align="center" width="100%"><tr><th>'+font+'Resume Owner Name</th><th>'+font+'Sharing Username</th>'
        output += '<th>'+font+'Resume Image</th><th>'+font+'Download Resume</th></tr>'        
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumebuilder',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM share where share_users='"+uname+"'")
            rows = cur.fetchall()
            for row in rows:
                output+="<tr><td>"+font+row[0]+"</td>"
                output+="<td>"+font+row[1]+"</td>"
                filename = row[2]
                with open ("ResumeApp/static/files/"+filename, "rb") as file:
                    data = file.read()
                file.close()
                data = decrypt(data)
                if os.path.exists("ResumeApp/static/test.jpg"):
                    os.remove("ResumeApp/static/test.jpg")
                with open ("ResumeApp/static/test.jpg", "wb") as file:
                    file.write(data)
                file.close()    
                output += '<td><img src="static/test.jpg" height="200" width="200"/>'
                output+='<td><a href=\'Download?fname='+filename+'\'><font size=3 color=black>Click Here to Download</font></a></td></tr>'
        context= {'data':output}
        return render(request, "UserScreen.html", context)        



        

