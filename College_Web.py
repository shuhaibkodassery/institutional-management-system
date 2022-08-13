from flask import Flask,render_template,request,session
import time
from DBConnection import Db

app = Flask(__name__)
app.secret_key = 'hi'

@app.route('/')
def admin_add_login():
    return render_template("login.html")

@app.route('/login_post',methods=['post'])
def login_post():
    username=request.form["textfield"]
    password = request.form["textfield2"]
    db=Db()
    qry="select * from login WHERE username='"+username+"' and password='"+password+"'"
    res=db.selectOne(qry)
    if res!=None:
        session['login_id']= res['lid']

        type=res['type']
        if type=='admin':
            return render_template("admin/admin_home.html")
        elif type=='sub_admin':
            return render_template("subadmin/subadmin_home.html")
        elif type=='student':
            return  render_template("student/student_home.html")
        elif type == 'hod':
            return render_template("hod/hod_home.html")
        elif type == 'parent':
            return render_template("parent/home.html")
        elif type == 'staff':
            return render_template("staff/home.html")
        else:
            return '''<script>alert('Invalid User');window.location='/'</script>'''
    else:
        return '''<script>alert('Invalid User');window.location='/'</script>'''





@app.route('/admin_add_course')
def admin_add_course():
    c=Db()
    qry="SELECT * FROM `department`"
    res=c.select(qry)
    print(res)
    return render_template("admin/couse.html",data=res)

@app.route('/admin_add_course_post',methods=['post'])
def admin_add_course_post():
    department=request.form["select"]
    course_code = request.form["textfield"]
    course_name = request.form["textfield2"]
    sem = request.form["sem"]
    db=Db()
    qry= "INSERT INTO course(`did`,`course_code`,`course_name`,`sem`)VALUES ('" + department + "','" + course_code + "','" + course_name + "','" + sem + "')"
    res= db.insert(qry)
    print(res)
    return admin_add_course()
@app.route('/admin_view_couse')
def admin_view_couse():
    qry="SELECT course.*,department.* from course INNER JOIN department ON course.did=department.did"
    c=Db()
    res=c.select(qry)
    return render_template("admin/view course.html",data=res)

@app.route('/admin_delete_course/<course_id>')
def admin_delete_course(course_id):
    qry="delete FROM course where course_id='"+course_id+"'"
    db=Db()
    res=db.delete(qry)
    return admin_view_couse()


@app.route('/admin_edits_course/<course_id>')
def admin_edits_course(course_id):
    qry="SELECT * FROM `course` WHERE `course_id`='"+course_id+"'"
    db=Db()
    res=db.selectOne(qry)

    qry3 = "SELECT `department`.* FROM `department`,`course` WHERE `course`.`did`=`department`.`did` AND `course`.`course_id`='" + course_id + "'"
    db = Db()
    res3 = db.selectOne(qry3)

    qry12 = "SELECT * FROM department"
    db = Db()
    res22 = db.select(qry12)
    return render_template("admin/edit_course.html",data=res,dd=res22,db=res3)

@app.route('/admin_edit_course_post',methods=['post'])
def admin_edit_course_post():
    department=request.form["select"]
    course_code = request.form["textfield"]
    course_name = request.form["textfield2"]
    sem = request.form["sem"]
    db=Db()
    hh=request.form['hh']
    qry= "UPDATE `course` SET `did`='"+department+"',`course_code`='"+course_code+"',`course_name`='"+course_name+"',`sem`='"+sem+"' WHERE `course_id`='"+hh+"'"
    res= db.update(qry)
    print(res)
    return admin_view_couse()
@app.route('/admin_add_course_search_post',methods=['post'])
def admin_add_course_search_post():
    dept=request.form["textfield"]
    db=Db()
    qry= "SELECT course.*,department.* from course INNER JOIN department ON course.did=department.did WHERE department_name='"+dept+"'"
    res = db.select(qry)
    return render_template("admin/view course.html", data=res)



@app.route('/admin_add_dept')
def admin_add_dept():
    return render_template("admin/department.html")

@app.route('/admin_add_dept_post',methods=['post'])
def admin_add_dept_post():
    department_name=request.form["textfield"]
    db=Db()
    qry="INSERT INTO `department`(`department_name`)VALUES('"+ department_name+"')"
    res=db.insert(qry)
    print(res)
    return render_template('admin/department.html')

@app.route('/admin_view_dept')
def admin_view_dept():
    qry="SELECT * FROM department"
    db=Db()
    res=db.select(qry)
    return render_template("admin/view department.html",data=res)



@app.route('/admin_delete_dept/<did>')
def admin_delete_dept(did):
    qry="delete FROM department where did='"+did+"'"
    db=Db()
    res=db.delete(qry)
    return admin_view_dept()



@app.route('/admin_edit_dept/<did>')
def admin_edit_dept(did):
    qry="SELECT * FROM `department` WHERE `did`='"+did+"'"
    db=Db()
    res=db.selectOne(qry)
    return render_template("admin/edit_deot.html",data=res)


@app.route('/admin_edits_post',methods=['post'])
def admin_edits_post():
    did=request.form['nn']
    department_name=request.form["textfield"]
    db=Db()
    qry="UPDATE `department` SET `department_name`='"+department_name+"' WHERE `did`='"+did+"' "
    res=db.update(qry)
    print(qry)
    return admin_view_dept()
@app.route('/admin_add_dept_search_post',methods=['post'])
def admin_add_dept_search_post():
    dept=request.form["textfield"]
    db=Db()
    qry= "SELECT * FROM `department`WHERE `department_name`='"+dept+"'"
    res = db.select(qry)
    return render_template("admin/view department.html", data=res)



@app.route('/admin_add_hod_assign')
def admin_add_hod_assign():
    c=Db()
    qry="SELECT * FROM `department`"
    res=c.select(qry)
    qry2="SELECT * FROM staff"
    res2=c.select(qry2)
    return render_template("admin/hod assignment.html", data=res,data2=res2)

@app.route('/admin_add_hod_assign_post',methods=['post'])
def admin_add_hod_assign_post():
    department=request.form["select"]
    staff=request.form["select2"]
    db=Db()
    ch="select * from hod_assignment WHERE did='"+department+"'"
    res2=db.selectOne(ch)
    if res2 is None:
        qry="INSERT INTO `hod_assignment`(`did`,`staff_lid`)VALUES('"+department+"','"+staff+"')"
        res=db.insert(qry)
        print(res)
    else:
        qry = "update `hod_assignment` set `staff_lid`='" + staff + "' where  `did`='" + department + "'"
        res = db.update(qry)
        print(res)


    q="UPDATE `login` SET `type`='hod' WHERE `lid`='"+staff+"'"
    r=db.update(q)
    return admin_add_hod_assign()
@app.route('/admin_view_hod_assign')
def admin_view_hod_assign():
    qry="SELECT hod_assignment.*,staff.*,department.* FROM hod_assignment INNER JOIN staff ON hod_assignment.staff_lid=staff.staff_lid INNER JOIN `department` ON `department`.`did`=`hod_assignment`.`did`"
    db=Db()
    res=db.select(qry)
    q="select * from department"
    re=db.select(q)
    return render_template("admin/view_hod.html",data=res,dept=re)





#@app.route('/admin_edit_hod')
#def admin_edit_hod():


    #return render_template("admin/view_hod.html")
@app.route('/admin_delete_hod/<hid>')
def admin_delete_hod(hid):
    qry="delete FROM hod_assignment where hid='"+hid+"'"
    db=Db()
    res=db.delete(qry)
    return admin_view_hod_assign()
@app.route('/admin_edit_hod/<hid>')
def admin_edit_hod(hid):
    qry="SELECT * FROM `hod_assignment` WHERE `hid`='"+hid+"'"
    print(qry)
    db=Db()
    res=db.selectOne(qry)
    qry1="select * from staff"
    res1=db.select(qry1)
    qry2="select * from department"
    res2=db.select(qry2)

    return render_template("admin/edit_hod.html",data=res,data1=res1,res=res2)
@app.route('/admin_edit_hod_post',methods=['post'])
def admin_edit_hod_post():
    dept = request.form["dept"]
    db=Db()
    qry="UPDATE `hod_assignment` SET `department_name`='"+dept+"' WHERE `did`='"+hid+"' "
    res=db.update(qry)
    print(qry)
    return admin_view_dept()

@app.route('/admin_add_password')
def admin_add_password():
    return render_template("admin/password.html")

@app.route('/admin_add_password_post',methods=['post'])
def admin_add_password_post():
    current_password=request.form["textfield"]
    new_password=request.form["textfield2"]
    confirm_password=request.form["textfield3"]
    db=Db()
    qry="SELECT * FROM login WHERE password='"+current_password+"'"
    res=db.selectOne(qry)
    if res!=None:
        if (new_password==confirm_password):
            qry1="UPDATE login SET `password`='"+new_password+"' WHERE lid ='"+str(session['login_id'])+"' "
            db.update(qry1)
            return '''<script>alert("password created");window.location="/"</script>'''
        else:
            return '''<script>alert("new password and confirm password not matching");window.location="/admin_add_password"</script>'''
    else:
        return '''<script>alert("old password not matching");window.location="/admin_add_password"</script>'''

@app.route('/admin_add_subadmin')
def admin_add_subadmin():
    return render_template("admin/sub_admin.html")

@app.route('/admin_add_subadmin_post',methods=['post'])
def admin_add_subadmin_post():
    name=request.form["textfield"]
    gender= request.form["radio"]
    phone= request.form["textfield2"]
    photo= request.files["fileField"]
    email= request.form["textfield3"]
    designation= request.form["textfield4"]
    import datetime
    dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    photo.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\punishment\\" + dt + ".jpg")
    path = "/static/punishment/" + dt + ".jpg"

    db = Db()
    qry = "INSERT INTO `subadmin`(`name`,`phone`,`email`,`designation`,`photo`,`gender`)VALUES('" + name + "','" +phone+ "','" +email+ "','" +designation+ "','" +path+ "','" +gender+ "')"
    res = db.insert(qry)
    print(res)
    return '''<script>alert("data entered succesfully");window.location="/admin_add_subadmin"</script>'''

@app.route('/admin_view_subadmin')
def admin_view_subadmin():
    qry="SELECT * FROM subadmin"
    db=Db()
    res=db.select(qry)
    return render_template("admin/view subadmin.html",data=res)


@app.route('/admin_view_subadmin2/<course_id>')
def admin_view_subadmin2(course_id):
    qry="delete FROM subadmin where subadmin_id='"+course_id+"'"
    db=Db()
    res=db.delete(qry)
    return admin_view_subadmin()



@app.route('/admin_view_subadmin3/<course_id>')
def admin_view_subadmin3(course_id):
    qry="SELECT * FROM `subadmin` WHERE `subadmin_id`='"+course_id+"'"
    db=Db()
    res=db.selectOne(qry)
    return render_template("admin/edit_subadmin.html",data=res)



@app.route('/admin_edit_subadmin_post',methods=['post'])
def admin_edit_subadmin_post():
    name=request.form["textfield"]
    gender= request.form["radio"]
    phone= request.form["textfield2"]
    email= request.form["textfield3"]
    designation= request.form["textfield4"]
    db=Db()
    sid=request.form['idk']
    if 'fileField' in request.files:
        photo = request.files["fileField"]
        if photo.filename!="":
            import datetime
            dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
            photo.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\punishment\\" + dt + ".jpg")
            path = "/static/punishment/" + dt + ".jpg"
            db = Db()
            qry = "UPDATE `subadmin` SET `name`='"+name+"',`phone`='"+phone+"',`email`='"+email+"'," \
                  "`designation`='"+designation+"',`photo`='"+path+"',`gender`='"+gender+"' WHERE `subadmin_id`='"+sid+"'"
            res = db.update(qry)
            print(res)
            return '''<script>alert("updated succesfully");window.location="/admin_view_subadmin"</script>'''
        else:
            qry = "UPDATE `subadmin` SET `name`='" + name + "',`phone`='" + phone + "',`email`='" + email + "'," \
            "`designation`='" + designation + "',`gender`='" + gender + "' WHERE `subadmin_id`='" + sid + "'"
            res = db.update(qry)
            print(res)
            return '''<script>alert("data entered succesfully");window.location="/admin_view_subadmin"</script>'''
    else:
        qry = "UPDATE `subadmin` SET `name`='" + name + "',`phone`='" + phone + "',`email`='" + email + "',designation`='" + designation + "',`gender`='" + gender + "' WHERE `subadmin_id`='" + sid + "'"
        res = db.update(qry)
        print(res)
        return '''<script>alert("data entered succesfully");window.location="/admin_view_subadmin"</script>'''
        

@app.route('/admin_add_sub_post',methods=['post'])
def admin_add_sub_post():
    sub=request.form["textfield"]
    db=Db()
    qry= "SELECT * from subadmin WHERE `name`LIKE '%"+sub+"%'"
    res = db.select(qry)
    return render_template("admin/view subadmin.html", data=res)
@app.route('/admin_add_punishment')
def admin_add_punishment():
    return render_template("admin/punishment.html")

@app.route('/admin_add_punishment_post',methods=['post'])
def admin_add_punishment_post():
    name=request.form["textfield"]
    photo=request.files["imageField"]
    reason=request.form["textfield2"]
    punishment= request.form["textfield3"]
    from_date= request.form["textfield4"]
    to_date= request.form["textfield5"]
    import datetime
    dt=datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    photo.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\punishment\\"+dt+".jpg")
    path="/static/punishment/"+dt+".jpg"


    db=Db()
    qry="INSERT INTO `punishment`(`slid`,`photo`,`reason`,`punishment`,`from_date`,`to_date`)VALUES('"+str(session['login_id'])+"','"+path+"','"+reason+"','"+punishment+"','"+from_date+"','"+to_date+"')"
    res=db.insert(qry)
    print(res)
    return 'ok'

@app.route('/admin_view_punishment')
def admin_view_punishment():
    qry = "SELECT `punishment`.*,`student`.`sname` FROM `punishment` INNER JOIN`student` ON `punishment`.`slid`=`student`.`slid`  "
    db=Db()
    res=db.select(qry)
    return render_template("admin/view punishment.html",data=res)
@app.route('/admin_add_punishment_search_post',methods=['post'])
def admin_add_punishment_search_post():
    frm = request.form["textfield"]
    to=request.form["textfield2"]
    db=Db()
    qry= "SELECT * FROM `punishment`WHERE `from_date`BETWEEN '"+frm+"' AND '"+to+"'"
    res = db.select(qry)
    return render_template("admin/view punishment.html", data=res)
@app.route('/admin_delete_punishment/<pid>')
def admin_delete_punishment(pid):
    qry="delete FROM punishment where pid='"+pid+"'"
    db=Db()
    res=db.delete(qry)
    return admin_view_punishment()
@app.route('/admin_edit_punishment/<pid>')
def admin_edit_punishment(pid):
    qry="SELECT * FROM `punishment` WHERE `pid`='"+pid+"'"
    db=Db()
    res=db.selectOne(qry)
    return render_template("admin/punishment_edit.html",data=res)
@app.route('/admin_edit_punishment_post',methods=['post'])
def admin_edit_punishment_post():
    name=request.form["textfield"]
    photo = request.files["imageField"]
    reason=request.form["textfield2"]
    punishment=request.form["textfield3"]
    from_date= request.form["textfield4"]
    to_date= request.form["textfield5"]
    pun_id= request.form["pun_id"]

    db = Db()

    if 'imageField' in request.files:
        photo = request.files["imageField"]


        if photo.filename != "":
            import datetime
            dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
            photo.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\punishment\\" + dt + ".jpg")
            path = "/static/punishment/" + dt + ".jpg"
            qry="UPDATE `punishment` SET `name`='"+name+"',`photo`='"+path+"', `reason`='"+reason+"',`punishment`='"+punishment+"', `from_date`='"+from_date+"',`to_date`='"+to_date+"' WHERE `pid`='"+pun_id+"'"

            res=db.update(qry)
            print(res)
            return '''<script>alert("data edited successfully");window.location="/admin_view_punishment"</script>'''
        else:
            db=Db()
            qry="UPDATE `punishment` SET `name`='"+name+"',`photo`='"+path+"', `reason`='"+reason+"',`punishment`='"+punishment+"', `from_date`='"+from_date+"',`to_date`='"+to_date+"' WHERE `pid`='"+pun_id+"'"
            res=db.update(qry)
            print(res)
            return '''<script>alert("data edited succesfully");window.location="/admin_view_punishment"</script>'''
    else:
        db = Db()
        qry = "UPDATE `punishment` SET `name`='" + name + "',`reason`='" + reason + "',`punishment`='" + punishment + "',`from_date`='" + from_date + "',`to_date`='" + to_date + "' where `pid`='" + pun_id + "'"
        res = db.update(qry)
        print(res)
        return '''<script>alert("data edited succesfully");window.location="/admin_view_punishment"</script>'''


@app.route('/admin_add_fee')
def admin_add_fee():
    c=Db()
    qry="SELECT * FROM `course`"
    res=c.select(qry)
    print(res)
    return render_template("admin/fee.html", data=res)



@app.route('/admin_view_fee')
def admin_view_fee():
    qry = "SELECT * FROM fee"
    db=Db()
    res=db.select(qry)
    return render_template("admin/viewfee.html",data=res)
@app.route('/admin_add_fee_search_post',methods=['post'])
def admin_add_fee_search_post():
    course= request.form["textfield"]
    db=Db()
    qry= "SELECT fee.*,course.* FROM `fee` INNER JOIN course ON fee.cid=course.course_id WHERE course_name LIKE '%"+course+"%'"
    res = db.select(qry)
    return render_template("admin/viewfee.html", data=res)

@app.route('/admin_add_fee_post',methods=['post'])
def admin_add_fee_post():
    course=request.form["select"]
    sem= request.form["select1"]
    fee= request.form["textfield3"]
    due_date= request.form["textfield4"]
    last_date= request.form["textfield5"]
    db = Db()
    qry = "INSERT INTO `fee`(`cid`,`sem`,`fee`,`due_date`,`late_date`)VALUES('" +course+ "','" + sem + "','" +fee + "','" +due_date+ "','" +last_date + "')"
    res = db.insert(qry)
    print(res)
    return '''<script>alert("data entered succesfully");window.location="/admin_add_fee"</script>'''
@app.route('/admin_delete_fee/<fid>')
def admin_delete_fee(fid):
    qry="delete FROM fee where fid='"+fid+"'"
    db=Db()
    res=db.delete(qry)
    return admin_view_fee()

@app.route('/admin_add_admin_home')
def admin_add_admin_home():
    return render_template("admin/admin_home.html")

# ----------------------------subadmin------------------------------------------------------------
@app.route('/subadmin_add_password')
def subadmin_add_password():
    return render_template("admin/password.html")

@app.route('/subadmin_add_password_post',methods=['post'])
def subadmin_add_password_post():
    current_password=request.form["textfield"]
    new_password=request.form["textfield2"]
    confirm_password=request.form["textfield3"]
    db=Db()
    qry="SELECT * FROM login WHERE password='"+current_password+"'"
    res=db.selectOne(qry)
    if res!=None:
        if (new_password==confirm_password):
            qry1="UPDATE login SET `password`='"+new_password+"' WHERE lid ='"+str(session['login_id'])+"' "
            db.update(qry1)
            return '''<script>alert("password created");window.location="/"</script>'''
        else:
            return '''<script>alert("new password and confirm password not matching");window.location="/subadmin_add_password"</script>'''
    else:
        return '''<script>alert("old password not matching");window.location="/subadmin_add_password"</script>'''

@app.route('/subadmin_add_notification')
def subadmin_add_notification():
    return render_template("subadmin/notification.html")
@app.route('/subadmin_view_notification')
def subadmin_view_notification():
    qry = "SELECT * FROM `notification`"
    db=Db()
    res=db.select(qry)
    return render_template("subadmin/view notifation.html", data=res)
@app.route('/subadmin_add_notification_post',methods=['post'])
def subadmin_add_notification_post():
    title=request.form["textfield"]
    content=request.form["textarea"]
    date=request.form["textfield1"]
    db=Db()
    qry="INSERT INTO `notification`(`lid`,`title`,`content`,`date`) VALUES('"+str(session['login_id'])+"','"+title+"','"+content+"','"+date+"')"
    res=db.insert(qry)
    print(res)
    return '''<script>alert("data entered succesfully");window.location="/subadmin_add_notification"</script>'''
@app.route('/subadmin_delete_notification/<nid>')
def subadmin_delete_notification(nid):
    qry="delete FROM notification where nid='"+nid+"'"
    db=Db()
    res=db.delete(qry)
    return subadmin_view_notification()

@app.route('/subadmin_edit_notification/<nid>')
def subadmin_edit_notification(nid):
    qry="SELECT * FROM `notification` WHERE `nid`='"+nid+"'"
    db=Db()
    res=db.selectOne(qry)
    return render_template("subadmin/notification_edit.html", data=res)

@app.route('/subadmin_edit_notification_post',methods=['post'])
def subadmin_edit_notification_post():
    not_id = request.form['n']
    title=request.form["textfield"]
    content=request.form["textarea"]
    date=request.form["textfield1"]
    db=Db()
    qry="UPDATE `notification` SET `title`='"+title+"',`content`='"+content+"',`date`='"+date+"' WHERE `nid`='"+not_id+"' "
    res=db.update(qry)
    print(qry)
    return '''<script>alert('Updated');window.location='/subadmin_view_notification'</script>'''
@app.route('/subadmin_add_notification_search_post',methods=['post'])
def subadmin_add_notification_search_post():
    frm=request.form["textfield"]
    to=request.form["textfield1"]
    db=Db()
    qry= "SELECT * FROM `notification`WHERE `date` BETWEEN '"+frm+"' AND '"+to+"'"
    res = db.select(qry)
    return render_template("subadmin/view notifation.html", data=res)




@app.route('/subadmin_add_staff')
def subadmin_add_staff():
    qr="SELECT * FROM `department`"
    d=Db()
    res=d.select(qr)
    return render_template("subadmin/staff.html",dept=res)
@app.route('/subadmin_add_staff_post',methods=['post'])
def subadmin_add_staff_post():
    staff_name= request.form["textfield"]
    dept= request.form["dept"]
    gender= request.form["radio"]
    dob= request.form["dob"]
    photo=request.files["imageField"]
    qualification=request.form["textfield2"]
    experience=request.form["textfield3"]
    contact= request.form["textfield4"]
    email= request.form["textfield5"]
    import datetime
    dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    photo.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\staff\\" + dt + ".jpg")
    path = "/static/staff/" + dt + ".jpg"
    db=Db()
    import random
    psw=str(random.randint(0000,99999))
    qry1="INSERT INTO `login`(`username`,`password`,`type`)VALUE('"+email+"','"+psw+"','staff')"
    lid=db.insert(qry1)


    qry="INSERT INTO `staff`(`staff_name`,`gender`,`dob`,`photo`,`qualification`,`experience`,`contact`,`email`,`staff_lid`,`did`) VALUES('"+staff_name+"','"+gender+"','"+dob+"','"+path+"','"+qualification+"','"+experience+"','"+contact+"','"+email+"','"+str(lid)+"','"+dept+"')"
    res = db.insert(qry)
    print(res)
    return '''<script>alert("data entered succesfully");window.location="/subadmin_add_staff"</script>'''
@app.route('/subadmin_view_staff')
def subadmin_view_staff():
    qry = "SELECT `staff`.*,`department`.* FROM `staff` INNER JOIN `department` ON `staff`.did=`department`.did"
    db=Db()
    res=db.select(qry)
    return render_template("subadmin/view staff.html", data=res)
@app.route('/subadmin_delete_staff/<staff_id>')
def subadmin_delete_staff(staff_id):
    qry="delete FROM staff where staff_id='"+staff_id+"'"
    db=Db()
    res=db.delete(qry)
    return subadmin_view_staff()

@app.route('/subadmin_edit_staff/<staff_id>')
def admin_edit_staff(staff_id):
    db=Db()
    qry="SELECT * FROM `staff` WHERE `staff_id`='"+staff_id+"'"
    res=db.selectOne(qry)
    qry1="SELECT * FROM `department`"
    res1=db.select(qry1)
    return render_template("subadmin/staff_edit.html",data=res, dept=res1)

@app.route('/subadmin_edit_staff_post',methods=['post'])
def subadmin_edit_staff_post():
    staff_name= request.form["textfield"]
    staffid= request.form['staffid']
    dept= request.form["dept"]
    gender= request.form["radio"]
    dob= request.form["dob"]
    photo=request.files["imageField"]
    qualification=request.form["textfield2"]
    experience=request.form["textfield3"]
    contact= request.form["textfield4"]
    email= request.form["textfield5"]

    import datetime
    dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    photo.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\staff\\" + dt + ".jpg")
    path = "/static/staff/" + dt + ".jpg"
    db=Db()
    qry ="UPDATE `staff` SET `did`='"+dept+"',`staff_name`='"+staff_name+"',`gender`='"+gender+"',`dob`='"+dob+"',`photo`='"+path+"',`qualification`='"+qualification+"',`experience`='"+experience+"',`contact`='"+contact+"',`email`='"+email+"' where `staff_id`='"+staffid+"'"
    res = db.update(qry)
    print(res)
    return subadmin_view_staff()
@app.route('/subadmin_add_staff_search_post',methods=['post'])
def subadmin_add_staff_search_post():
    staff_name=request.form["textfield"]
    db=Db()
    qry= "SELECT `staff`.*,`department`.* FROM `staff` INNER JOIN `department` ON `staff`.did=`department`.did WHERE `staff_name`='"+staff_name+"'"
    res = db.select(qry)
    return render_template("subadmin/view staff.html", data=res)









@app.route('/subadmin_add_student')
def subadmin_add_student():
    c=Db()
    qry= "SELECT * FROM course"
    res= c.select(qry)
    return render_template("subadmin/student.html", data=res)

    return render_template("subadmin/student.html")


@app.route('/subadmin_student_post',methods=['post'])
def subadmin_add_student_post():
    sname= request.form["textfield"]
    gender= request.form["radio"]
    course=request.form["select"]
    print("-------course",course)
    sem= request.form["textfield2"]
    photo= request.files["imageField"]
    admission_no= request.form["textfield3"]
    dob= request.form["dob"]
    contact = request.form["textfield4"]
    email = request.form["textfield5"]
    import datetime
    dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    photo.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\student\\" + dt + ".jpg")
    path = "/static/student/" + dt + ".jpg"
    db = Db()
    qry = "INSERT INTO `student`(`sname`,`gender`,`cid`,`sem`,`photo`,`admission_no`,`dob`,`contact`,`email`) VALUES('" + sname+ "','" + gender + "','"+course+"','" +sem+ "','" + path + "','" +admission_no+ "','" +dob+ "','" + contact + "','" + email + "')"
    res = db.insert(qry)
    print(res)
    return '''<script>alert("data entered succesfully");window.location="/subadmin_add_student"</script>'''


@app.route('/subadmin_view_student')
def subadmin_view_student():
    qry = "SELECT `student`.*,`course`.* FROM `student` INNER JOIN `course` ON `student`.cid=`course`.course_id"
    db = Db()
    res = db.select(qry)
    return render_template("subadmin/view student.html", data=res)

@app.route('/subadmin_delete_student/<sid>')
def subadmin_delete_student(sid):
    qry="delete FROM student where sid='"+sid+"'"
    db=Db()
    res=db.delete(qry)
    return '''<script>alert('Deleted');window.location='/subadmin_view_student'</script>'''

@app.route('/subadmin_edit_student/<sid>')
def subadmin_edit_student(sid):
    qry="SELECT * FROM `student` WHERE `sid`='"+sid+"'"
    db=Db()
    res=db.selectOne(qry)
    qry1 = "SELECT * FROM `course`"
    res1 = db.select(qry1)
    return render_template("subadmin/edit_student.html",data=res,dept=res1)

@app.route('/subadmin_edit_student_post',methods=['post'])
def subadmin_edit_student_post():
    sname= request.form["textfield"]
    s_id= request.form["sid"]
    gender= request.form["radio"]
    course=request.form["dept"]
    sem= request.form["textfield2"]
    photo= request.files["imageField"]
    admission_no= request.form["textfield3"]
    dob= request.form["dob"]
    contact = request.form["textfield4"]
    email = request.form["textfield5"]

    db = Db()
    import datetime
    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    photo.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\student\\" + dt + ".jpg")
    path = "/static/student/" + dt + ".jpg"

    qry="UPDATE `student` SET `sname`='"+sname+"',`gender`='"+gender+"',`cid`='"+course+"',`sem`='"+sem+"',`photo`='"+path+"',`admission_no`='"+admission_no+"',`dob`='"+dob+"',`contact`='"+contact+"',`email`='"+email+"' WHERE `sid`='"+s_id+"' "
    res=db.update(qry)
    print(qry)
    return '''<script>alert('Updated');window.location='/subadmin_view_student'</script>'''
@app.route('/subadmin_add_student_search_post',methods=['post'])
def subadmin_add_student_search_post():
    student=request.form["textfield"]
    db=Db()
    qry= "SELECT * FROM `student`WHERE `sname`='"+student+"'"
    res = db.select(qry)
    return render_template("subadmin/view student.html", data=res)





@app.route('/subadmin_add_punishment')
def subadmin_add_punishment():
    return render_template("subadmin/punishment.html")

@app.route('/subadmin_add_punishment_post',methods=['post'])
def subadmin_add_punishment_post():
    name=request.form["textfield"]
    photo=request.files["imageField"]
    reason=request.form["textfield2"]
    punishment= request.form["textfield3"]
    from_date= request.form["textfield4"]
    to_date= request.form["textfield5"]
    import datetime
    dt=datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    photo.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\punishment\\"+dt+".jpg")
    path="/static/punishment/"+dt+".jpg"


    db=Db()
    qry="INSERT INTO `punishment`(`name`,`photo`,`reason`,`punishment`,`from_date`,`to_date`)VALUES('"+name+"','"+path+"','"+reason+"','"+punishment+"','"+from_date+"','"+to_date+"')"
    res=db.insert(qry)
    print(res)
    return '''<script>alert("data entered succesfully");window.location="/subadmin_add_punishment"</script>'''

@app.route('/subadmin_view_punishment')
def subadmin_view_punishment():
    qry = "SELECT * FROM punishment"
    db = Db()
    res = db.select(qry)
    return render_template("subadmin/view punishment.html", data=res)
@app.route('/subadmin_delete_punishment/<pid>')
def subadmin_delete_punishment(pid):
    qry="delete FROM punishment where pid='"+pid+"'"
    db=Db()
    res=db.delete(qry)
    return subadmin_view_punishment()
@app.route('/subadmin_edit_punishment/<pid>')
def subadmin_edit_punishment(pid):
    qry="SELECT * FROM `punishment` WHERE `pid`='"+pid+"'"
    db=Db()
    res=db.selectOne(qry)
    return render_template("subadmin/punishment_edit.html",data=res)
@app.route('/subadmin_edit_punishment_post',methods=['post'])
def subadmin_edit_punishment_post():
    name=request.form["textfield"]
    photo = request.files["imageField"]
    reason=request.form["textfield2"]
    punishment=request.form["textfield3"]
    from_date= request.form["textfield4"]
    to_date= request.form["textfield5"]
    pun_id= request.form["pun_id"]

    db = Db()

    if 'imageField' in request.files:
        photo = request.files["imageField"]


        if photo.filename != "":
            import datetime
            dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
            photo.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\punishment\\" + dt + ".jpg")
            path = "/static/punishment/" + dt + ".jpg"

            qry="UPDATE `punishment` SET `name`='"+name+"',`photo`='"+path+"', `reason`='"+reason+"',`punishment`='"+punishment+"', `from_date`='"+from_date+"',`to_date`='"+to_date+"' WHERE pid='"+pun_id+"'"
            res=db.update(qry)
            print(res)
            return '''<script>alert("data edited successfully");window.location="/subadmin_view_punishment"</script>'''
        else:
            db = Db()
            qry ="UPDATE `punishment` SET `name`='"+name+"',`photo`='"+path+"', `reason`='"+reason+"',`punishment`='"+punishment+"', `from_date`='"+from_date+"',`to_date`='"+to_date+"' WHERE pid='"+pun_id+"'"
            res = db.update(qry)
            print(res)
            return '''<script>alert("data edited succesfully");window.location="/subadmin_view_punishment"</script>'''
    else:
        db = Db()
        qry = "UPDATE `punishment` SET `name`='" + name + "',`reason`='" + reason + "',`punishment`='" + punishment + "',`from_date`='" + from_date + "',`to_date`='" + to_date + "' where pid='" + pun_id + "'"
        res = db.update(qry)
        print(res)
        return '''<script>alert("data edited succesfully");window.location="/subadmin_view_punishment"</script>'''
@app.route('/subadmin_add_punishment_search_post',methods=['post'])
def subadmin_add_punishment_search_post():
    frm = request.form["textfield"]
    to=request.form["textfield2"]
    db=Db()
    qry= "SELECT * FROM `punishment`WHERE `from_date`BETWEEN '"+frm+"' AND '"+to+"'"
    res = db.select(qry)
    return render_template("subadmin/view punishment.html", data=res)





@app.route('/subadmin_add_subadmin_home')
def admin_add_subadmin_home():
    return render_template("subadmin/subadmin_home.html")

#------------hod-------------------------------------


@app.route('/hod_change_password')
def hod_change_password():
    return render_template('hod/change_password.html')

@app.route('/hod_change_password_post', methods=['post'])
def hod_change_password_post():
    current_password = request.form['textfield']
    new_password = request.form['textfield2']
    confirm_password = request.form['textfield3']

    db = Db()
    qry = "SELECT * FROM login WHERE lid='"+str(session['login_id'])+"'"
    print(qry)
    res = db.selectOne(qry)


    if res is not None:
        if confirm_password==new_password:
            qry1 = "UPDATE login SET `password`='"+confirm_password+"' WHERE lid='"+str(session['login_id'])+"'"
            db.update(qry1)
            return '''<script>alert('Password created');window.location='/'</script>'''
        else:
            return '''<script>alert('Password mismatch');window.location='/hod_change_password'</script>'''
    else:
        return '''<script>alert('Please enter your current password');window.location='/hod_change_password'</script>'''



@app.route('/hod_add_staff')
def hod_add_staff():
    return render_template("hod/view staff.html")


@app.route('/hod_view_staff')
def hod_view_staff():

    db=Db()
    qry = 'select * from staff'
    res= db.select(qry)
    return render_template("hod/view staff.html", data=res)

@app.route('/hod_view_staff_search_post',methods=['post'])
def hod_view_staff_search_post():
    staffname=request.form["textfield"]
    db=Db()
    qry = "select * from staff where  staff_name like '%"+staffname+"%'"
    res = db.select(qry)
    return render_template("hod/view staff.html", data=res)


@app.route('/hod_edit_staff/<staff_id>')
def hod_edit_staff(staff_id):
    qry="select * from staff where where staff_id='"+staff_id+"'"
    db=Db()
    res=db.selectone(qry)
    return


@app.route('/hod_delete_staff/<staff_id>')
def hod_delete_staff(staff_id):
    qry="delete FROM staff where staff_id='"+staff_id+"'"
    db=Db()
    res=db.delete(qry)
    return '''<script>alert('Deleted');window.location='/hod_view_staff'</script>'''




@app.route('/hod_add_subject')
def hod_add_subject():
    db = Db()
    qry = "SELECT * FROM `course`"
    res = db.select(qry)
    return render_template("hod/subject.html", data=res)
@app.route('/hod_add_subject_post', methods=['post'])
def hod_add_subject_post():
    course = request.form['textfield']
    sem=request.form["textfield2"]
    subject_code=request.form["textfield3"]
    subject_name=request.form["textfield4"]
    db=Db()
    qry1="INSERT INTO `subject`(`cid`,`sem`,`sub_code`,`sub_name`) VALUES('"+course+"','"+sem+"','"+subject_code+"','"+subject_name+"')"
    res=db.insert(qry1)
    print(res)
    return '''<script>alert('Added Successfully');window.location='/hod_add_subject'</script>'''

@app.route('/hod_view_subject')
def hod_view_subject():
    c=Db()
    qry="SELECT `subject`.*,`course`.`course_name` FROM `course` INNER JOIN `subject` ON `subject`.`cid`=`course`.`course_id`"
    res=c.select(qry)
    qry1 = "select * from course"
    res1 = c.select(qry1)
    return render_template("hod/view subject.html",data=res, data1=res1)

@app.route('/hod_view_subject_search', methods=['post'])
def hod_view_subject_search():
    course = request.form['select']
    db = Db()
    qry1= "select * from course"
    res1 = db.select(qry1)
    qry = "SELECT `subject`.*,`course`.`course_name` FROM `course` INNER JOIN `subject` ON `subject`.`cid`=`course`.`course_id` WHERE `course`.`course_name` LIKE '%"+course+"%'"
    res = db.select(qry)
    return render_template("hod/view subject.html",data=res, data1=res1)



@app.route('/delete_subject/<sid>')
def delete_subject(sid):
    db = Db()
    qry = " DELETE FROM `subject` WHERE `sub_id` = '"+sid+"'"
    res = db.delete(qry)
    return '''<script>alert('Deleted');window.locatio='/hod_view_subject'</script>'''

@app.route('/edit_subject/<sid>')
def edit_subject(sid):
    db = Db()
    qry = "SELECT * FROM `subject` WHERE `sub_id` ='"+sid+"'"
    res = db.selectOne(qry)

    qry1 ="select * from course"
    res1=db.select(qry1)


    return render_template('hod/edit_subject.html',res=res,res1=res1)

@app.route('/edit_subject_post', methods=['post'])
def edit_subject_post():
    iid = request.form["id"]
    cid=request.form["textfield"]
    sem=request.form["textfield2"]
    sub_code=request.form["textfield3"]
    sub_name=request.form["textfield4"]
    db=Db()
    qry="update subject set cid='"+cid+"',sem='" + sem+ "' ,sub_code='"+sub_code+"',sub_name='"+sub_name+"' where sub_id='"+str(iid)+"'"
    res = db.update(qry)
    return '''<script>alert('update Successfully');window.location='/hod_view_subject'</script>'''
@app.route('/hod_add_staff_subject_allocation')
def hod_add_subject_allocation():
    c = Db()
    qry = "SELECT * FROM course"
    res = c.select(qry)
    qry1="select * from staff"
    res1=c.select(qry1)
    qry2="select * from subject"
    res2=c.select(qry2)
    return render_template("hod/staff subject allocation.html", data=res, res1=res1, res2=res2)

@app.route('/hod_add_staff_subject_allocation_post', methods=['post'])
def hod_add_staff_subject_allocation_post():
    course_name= request.form['textfield1']
    staff= request.form["textfield"]
    subject= request.form["textfield3"]
    semester = request.form['textfield2']
    db = Db()
    qry1 = "INSERT INTO `subject_allocation`(sub_id,staff_id) VALUES('" + subject + "','" + staff+ "')"
    res = db.insert(qry1)
    print(res)
    return '''<script>alert('Added Successfully');window.location='/hod_add_staff_subject_allocation'</script>'''

@app.route('/hod_view_staff_subject_allocation')
def hod_view_staff_subject_allocation():
    c = Db()
    qry1 = "SELECT * FROM SUBJECT"
    res1 = c.select(qry1)
    qry = "SELECT `course`.`course_name`,`subject`.sub_name, `subject`.`sem`, staff.staff_name,staff.email,subject_allocation.alloc_id FROM  course INNER JOIN  SUBJECT ON `course`.`course_id`=`subject`.`cid` INNER JOIN subject_allocation ON `subject_allocation`.`sub_id`=`subject`.`sub_id` INNER JOIN  staff ON `staff`.`staff_id`=`subject_allocation`.`staff_id` "
    res = c.select(qry)
    return render_template("hod/view staff allocation.html", data=res, data1=res1
                           )
#
# @app.route('/hod_add_staff_subject_allocation_post')
# def hod_add_staff_subject_allocation_post():
#    return render_template("hod/staff subject allocation.html")

@app.route('/staff_subject_allocation_search', methods =['post'])
def staff_subject_allocation_search():
    select_sub = request.form['select']
    db = Db()
    qry1 = "SELECT * FROM SUBJECT"
    res1 = db.select(qry1)
    qry = "SELECT `course`.`course_name`,`subject`.sub_name, `subject`.`sem`, staff.staff_name,staff.email,subject_allocation.alloc_id FROM  course INNER JOIN  SUBJECT ON `course`.`course_id`=`subject`.`cid` INNER JOIN subject_allocation ON `subject_allocation`.`sub_id`=`subject`.`sub_id` INNER JOIN  staff ON `staff`.`staff_id`=`subject_allocation`.`staff_id` WHERE `subject`.`sub_name` LIKE '%"+select_sub+"%' "
    res = db.select(qry)
    return render_template("hod/view staff allocation.html", data=res, data1=res1)


@app.route('/delete_staff_allocate/<id>')
def delete_staff_allocate(id):
    db = Db()
    qry = "DELETE FROM `subject_allocation` WHERE `alloc_id`='"+id+"'"
    res = db.delete(qry)
    return '''<script>alert('Deleted');window.location='/hod_view_staff_subject_allocation'</script>'''


@app.route('/edit_staff_allocate/<id>')
def edit_staff_allocate(id):
    db = Db()
    qry = "SELECT * FROM `subject_allocation` WHERE `alloc_id` ='"+id+"'"
    res = db.selectOne(qry)
    qry1 = "SELECT * FROM course"
    res1 = db.select(qry1)
    qry2 = "select * from staff"
    res2 = db.select(qry2)
    qry3 = "select * from subject"
    res3 = db.select(qry3)
    return render_template('hod/edit_staff_sub_allocation.html', edit=res, data=res1, )

@app.route('/hod_add_timetable')
def hod_add_timetable():
    c = Db()
    qry = "SELECT * FROM course"
    res = c.select(qry)
    qry1="select * from subject"
    res1=c.select(qry1)
    return render_template("hod/timetable.html", data=res,res1=res1)

@app.route('/hod_add_time_table_post',methods=['post'])
def hod_add_time_table_post():
    subject= request.form["textfield"]
    course= request.form["textfield1"]
    sem=request.form["textfield2"]
    day= request.form["textfield3"]
    hour=request.form["textfield4"]
    db = Db()
    qry1 = "INSERT INTO `time_table`(sub_id,day,hour,couse_id,sem) VALUES('" + subject + "','"+day+"','"+hour+"','" + course+ "','"+sem+"')"
    res = db.insert(qry1)
    print(res)
    return '''<script>alert('Added Successfully');window.location='/hod_add_timetable'</script>'''

@app.route('/hod_add_complaints')
def hod_add_complaints():

    return render_template("hod/complaints.html")

@app.route('/hod_view_complaints')
def hod_view_complaints():
   return render_template("hod/complaints.html")

@app.route('/hod_add_complaints_post',methods=['post'])
def hod_add_complaints_post():
    complaint=request.form["textarea"]
    db = Db()
    qry1 = "INSERT INTO `complaint`(complint,date,status,replay,lid) VALUES('" + complaint + "',curdate(),'pending','pending','"+str(session['login_id'])+"')"
    res = db.insert(qry1)
    print(res)
    return '''<script>alert('send Successfully');window.location='/hod_add_complaints'</script>'''



@app.route('/hod_view_complaint')
def hod_view_complaint():
    db = Db()
    qry = "SELECT * FROM complaint WHERE lid = '"+str(session['login_id'])+"'"
    res = db.select(qry)
    return render_template('hod/view complaints.html', data=res)

@app.route('/delete_send_complaint/<id>')
def delete_send_complaint(id):
    db = Db()
    qry = "DELETE FROM `complaint` WHERE cid = '"+id+"'"
    res = db.delete(qry)
    return '''<script>alert('Deleted');window.location='/hod_view_complaint'</script>'''


@app.route('/hod_add_notification')
def hod_add_notification():
   return render_template("hod/notification.html")

@app.route('/hod_view_notification')
def hod_view_notification():
   return render_template("hod/notification.html")

@app.route('/hod_add_notification_post')
def hod_add_notification_post():
   return render_template("hod/notification.html")

@app.route('/hod_add_feedback')
def hod_add_feedback():
   return render_template("hod/feedback.html")

@app.route('/hod_view_feedback')
def hod_view_feedback():
   return render_template("hod/feedback.html")

@app.route('/hod_add_feedback_post')
def hod_add_feedback_post():
   return render_template("hod/feedback.html")
















@app.route('/hod_add_hod_home')
def hod_add_hod_home():
    return render_template("hod/hod_home.html")




#------------hod end--------------------------------------------------------------------------





#---------------------module-5-----student---------------------------


@app.route('/student_add_password')
def student_add_password():
    return render_template('student/password.html')

@app.route('/student_add_password_post', methods=['post'])
def student_add_password_post():

    cur_password = request.form['textfield']
    new_password = request.form['textfield2']
    con_password = request.form['textfield3']

    db = Db()
    qry = "SELECT * FROM login WHERE `password`='"+cur_password+"'"
    res = db.selectOne(qry)

    if res!=None:
        if new_password == con_password:
            qry1="UPDATE login SET `password`='"+new_password+"' WHERE lid ='"+str(session['login_id'])+"'"
            res = db.update(qry1)
            return '''<script>alert('Password Created');window.location='/'</script>'''
        else:
            return '''<script>alert('Password mismatch');window.location='/student_add_password'</script>'''
    else:
        return '''<script>alert('Please enter your current password');window.location='/student_add_password'</script>'''





@app.route('/student_view_note')
def student_view_note():
    qry = "SELECT `notes`.*, `course`.`course_name`, `subject`.`sub_name` FROM `subject` INNER JOIN `notes` ON `notes`.`sub_id`=`subject`.`sub_id` INNER JOIN `course` ON `course`.`course_id`=`notes`.`course_id`"
    db = Db()
    res = db.select(qry)
    return render_template("student/view notes.html", data=res)

@app.route('/student_notes_search_post',methods=['post'])
def student_notes_search_post():
    course=request.form["textfield"]
    db=Db()
    qry= "SELECT `notes`.*, `course`.`course_name`, `subject`.`sub_name` FROM `subject` INNER JOIN `notes` ON `notes`.`sub_id`=`subject`.`sub_id` INNER JOIN `course` ON `course`.`course_id`=`notes`.`course_id` WHERE `course_name`='"+course+"'"
    res = db.select(qry)
    return render_template("student/view notes.html", data=res)
@app.route('/student_send_complaint')
def student_send_complaints():
    return render_template('student/complaints.html')

@app.route('/student_send_complaint_post',methods=['post'])
def student_send_complaints_post():
    complaint=request.form["textarea"]
    db=Db()
    qry="INSERT INTO complaint(`lid`,`type`,`complint`,`reply`,`date`,`status`) VALUES ('"+str(session['login_id'])+"','student','"+complaint+"','pending',CURDATE(),'pending')"
    db.insert(qry)
    return render_template('student/complaints.html')
@app.route('/student_view_complaint')
def student_view_complaints():
    qry="SELECT * FROM complaint WHERE lid='"+str(session['login_id'])+"'"
    db=Db()
    res=db.select(qry)
    return render_template('student/complanits view.html',data=res)
@app.route('/student_delete_complaint/<cid>')
def student_delete_complaint(cid):
    qry="delete FROM complaint where cid='"+cid+"'"
    db=Db()
    res=db.delete(qry)
    return student_view_complaints()


@app.route('/student_view_timetable')
def student_view_timetable():

    q="SELECT `slid`,`cid`,`sem` FROM `student` WHERE `student`.`slid`='"+str(session['login_id'])+"'"
    db = Db()
    resa=db.selectOne(q)
    if resa is not None:

        cid=resa['cid']
        sem=resa['sem']



        hr=["1","2","3","4","5"]
        day=["monday","tuesday","wednesday","thursday","friday"]

        a=[]

        for i in day:

            f=[]


            for k in hr:
                qry = "SELECT * FROM `time_table` where course_id='" + str(cid) + "' and sem='" + str(sem) + "' and hour='"+k+"' and day='"+i+"'"
                res = db.selectOne(qry)
                if res is not None:

                    subid=str(res['sub_id'])
                    qry1="SELECT `sub_name` FROM `subject` WHERE `sub_id`='"+subid+"'"
                    res1=db.selectOne(qry1)


                    f.append(res1['sub_name'])
                else:
                    f.append("Free")


            a.append(f)

        return render_template('student/view timetable.html',a=a)
    else:
        return render_template("student/student_home.html")
@app.route('/student_view_profile')
def student_view_pofile():
    qry="SELECT * FROM `student`"
    db=Db()
    res=db.select(qry)
    return render_template('student/student profile.html',data=res)

@app.route('/student_send_feedback')
def student_send_feedback():
    return render_template('student/feedback.html')

@app.route('/student_send_feedback_post',methods=['post'])
def student_send_feedback_post():
    feedback=request.form["textarea"]
    db=Db()
    qry="INSERT INTO feedback(`lid`,`feedback`,`date`,`type`) VALUES ('"+str(session['login_id'])+"','"+feedback+"',CURDATE(),'student')"
    db.insert(qry)
    return '''<script>alert('feedback send');window.location='/student_send_feedback'</script>'''
@app.route('/student_add_student_home')
def student_add_student_home():
    return render_template("student/student_home.html")

@app.route('/student_view_notification')
def student_view_notification():
    qry = "SELECT * FROM `notification`"
    db=Db()
    res=db.select(qry)
    return render_template("student/view notifation.html", data=res)



@app.route('/student_view_attendance')
def student_view_attendance():

    return render_template('student/attendance view.html')

@app.route('/student_view_attendance_post',methods=['post'])
def student_view_attendance_post():
    year=request.form["select"]
    month=request.form["select2"]

    sid=str(session["login_id"])

    hr=["1","2","3","4","5"]

    db=Db()
    attendence=[]
    for i in range(1,32):
        f=year+"-"+month+"-"+str(i)
        aa=[]
        for i in hr:

            qry = "SELECT  slid FROM `attendence` WHERE `slid`='" + sid + "' and year(date)='" + year + "' and month(date)='" + month + "' and date='"+f+"' and hour='"+str(i)+"'"

            res=db.selectOne(qry)
            if res is not None:
                print(qry)
                aa.append("P")
            else:
                aa.append("A")
        attendence.append(aa)

    print(res)
    print("-------------------------------------------------")
    print(attendence)
    return render_template('student/attendance view.html',data=attendence,cnt=len(attendence))

@app.route('/student_view_internal_mark')
def student_view_internal_mark():
    # qry="select * from internal_mark"
    # db=Db()
    # res=db.select(qry)
    return render_template('student/view internal mark.html')

@app.route('/student_view_internal_mark_post',methods=['post'])
def student_view_internal_mark_post():
    sem=request.form["select"]
    db=Db()
    qry="SELECT `internal_mark`.*, `subject`.`sub_name` FROM `subject` INNER JOIN `internal_mark` ON `internal_mark`.`sub_id`=`subject`.`sub_id` WHERE slid='"+str(session['login_id'])+"' and subject.sem='"+sem+"'"
    res=db.select(qry)
    print(res)

    return render_template('student/view internal mark.html',data=res)


@app.route('/student_viewpunishment')
def student_viewpunishment():

    db=Db()
    qry="SELECT * FROM `punishment` WHERE slid='"+session["login_id"]+"'"
    res=db.select(qry)

    return render_template("student/view_punishment.html",res=res)


# staff section starts


@app.route('/staff_add_password')
def staff_add_password():
    return render_template('staff/password.html')

@app.route('/staff_add_password_post', methods=['post'])
def staff_add_password_post():

    cur_password = request.form['textfield']
    new_password = request.form['textfield2']
    con_password = request.form['textfield3']

    db = Db()
    qry = "SELECT * FROM login WHERE `password`='"+cur_password+"'"
    res = db.selectOne(qry)

    if res!=None:
        if new_password == con_password:
            qry1="UPDATE login SET `password`='"+new_password+"' WHERE lid ='"+str(session['login_id'])+"'"
            res = db.update(qry1)
            return '''<script>alert('Password Created');window.location='/'</script>'''
        else:
            return '''<script>alert('Password mismatch');window.location='/staff_add_password'</script>'''
    else:
        return '''<script>alert('Please enter your current password');window.location='/staff_add_password'</script>'''












@app.route('/staff_addinternalmark')
def staff_addinternalmark():
    return render_template("staff/addinternalmark.html")

@app.route('/staff_attendancemarking')
def staff_attendancemarking():
    return render_template("staff/attendancemarking.html")


@app.route("/staff_addrating")
def staff_addrating():
    return render_template("staff/sentapprating.html")



@app.route('/staff_viewnotification')
def staffviewnotification():

    db=Db()
    qry="select * from notification"
    res=db.select(qry)

    return render_template("staff/viewnotification.html",res=res)

@app.route('/staff_viewassignedsubject')
def staff_viewassignedsubject():
    db=Db()
    qry="SELECT subject.*,`course`.`course_code`,`course`.`course_name` FROM SUBJECT INNER JOIN `subject_allocation` ON `subject`.`sub_id`=`subject_allocation`.`sub_id` INNER JOIN `staff` ON `staff`.`staff_id`=`subject_allocation`.`staff_id` INNER JOIN `course` ON `course`.`course_id`=`subject`.`cid` WHERE `staff`.`staff_lid`='"+str(session["login_id"])+"'"
    res=db.select(qry)

    return render_template("staff/viewallocatedsubject.html",data=res)



@app.route('/staff_add_notes')
def staff_add_notes():
    qry="select * from subject"
    db=Db()
    res=db.select(qry)
    qry1="select * from course"
    res1=db.select(qry1)

    return render_template("staff/uploadnotes.html",data=res,data1=res1)


@app.route('/staff_add_notes_post',methods=['post'])
def staff_add_notes_post():
    subject=request.form['select']
    note=request.form['textfield']
    file=request.files['fileField']
    course=request.form['select2']
    import datetime
    dt=datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    file.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\notes\\"+dt+".pdf")
    path="/static/notes/"+dt+".pdf"
    qry="INSERT INTO `notes` (`sub_id`,`course_id`,`notes`,`description`,`staff_lid`) VALUES ('"+subject+"','"+course+"','"+path+"','"+note+"','"+str(session['login_id'])+"')"
    db=Db()
    res=db.insert(qry)
    return "<script>alert('notes uploaded succesfully');window.location='/staff_add_notes'</script>"

@app.route('/staff_view_note')
def staff_view_note():
    qry = "SELECT `notes`.*, `course`.`course_name`, `subject`.`sub_name` FROM `subject` INNER JOIN `notes` ON `notes`.`sub_id`=`subject`.`sub_id` INNER JOIN `course` ON `course`.`course_id`=`notes`.`course_id`"
    db = Db()
    res = db.select(qry)
    return render_template("staff/view notes.html", data=res)

@app.route('/staff_notes_search_post',methods=['post'])
def staff_notes_search_post():
    course=request.form["textfield"]
    db=Db()
    qry= "SELECT `notes`.*, `course`.`course_name`, `subject`.`sub_name` FROM `subject` INNER JOIN `notes` ON `notes`.`sub_id`=`subject`.`sub_id` INNER JOIN `course` ON `course`.`course_id`=`notes`.`course_id` WHERE `course_name`='"+course+"'"
    res = db.select(qry)
    return render_template("staff/view notes.html", data=res)

@app.route('/staff_delete_note/<note_id>')
def staff_delete_note(note_id):
    qry="delete FROM notes where note_id='"+note_id+"'"
    db=Db()
    res=db.delete(qry)
    return '''<script>alert('Deleted');window.location='/staff_view_note'</script>'''
@app.route('/staff_edit_note/<note_id>')
def staff_edit_note(note_id):
    qry="SELECT `notes`.*, `course`.`course_name`, `subject`.`sub_name` FROM `subject` INNER JOIN `notes` ON `notes`.`sub_id`=`subject`.`sub_id` INNER JOIN `course` ON `course`.`course_id`=`notes`.`course_id` where notes.note_id='"+note_id+"'"
    db=Db()
    res=db.selectOne(qry)
    qry1= "select * from subject"
    res1= db.select(qry1)
    qry2 = "select * from course"
    res2 = db.select(qry2)

    return render_template("staff/edit note.html",data=res,data1=res1,data2=res2)



@app.route('/staff_edit_note_post',methods=['post'])
def staff_edit_note_post():
    subject = request.form['select']
    note = request.form['textfield']
    file = request.files['fileField']
    course = request.form['select2']
    nid=request.form['nid']
    db = Db()

    if 'filefield' in request.files:
        file = request.files["imageField"]


        if file.filename != "":
            import datetime
            dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
            file.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\notes\\" + dt + ".pdf")
            path = "/static/notes/" + dt + ".pdf"

            qry="UPDATE `notes` SET `sub_id`='"+subject+"',`course_id`='"+course+"',`notes`='"+path+"', `description`='"+note+"' WHERE note_id='"+nid+"'"
            res=db.update(qry)
            print(res)
            return '''<script>alert("data edited successfully");window.location="/staff_view_note"</script>'''
        else:
            db = Db()
            qry ="UPDATE `notes` SET `sub_id`='"+subject+"',`course_id`='"+course+"',`notes`='"+path+"', `description`='"+note+"' WHERE note_id='"+nid+"'"
            res = db.update(qry)
            print(res)
            return '''<script>alert("data edited succesfully");window.location="/staff_view_note"</script>'''
    else:
        db = Db()
        qry = "UPDATE `notes` SET `sub_id`='"+subject+"',`course_id`='"+course+"',`description`='"+note+"' WHERE note_id='"+nid+"'"
        res = db.update(qry)
        print(res)
        return '''<script>alert("data edited succesfully");window.location="/staff_view_note"</script>'''

@app.route('/staff_send_feedback')
def staff_send_feedback():
        return render_template('staff/feedback.html')

@app.route('/staff_send_feedback_post', methods=['post'])
def staff_send_feedback_post():
        feedback = request.form["textarea"]
        db = Db()
        qry = "INSERT INTO feedback(`lid`,`feedback`,`date`,`type`) VALUES ('" + str(session['login_id']) + "','" + feedback + "',CURDATE(),'staff')"
        db.insert(qry)
        return '''<script>alert('feedback send');window.location='/staff_send_feedback'</script>'''

@app.route('/staff_view_timetable')
def staff_view_timetable():
    qry="SELECT `subject`.`sub_name`,`time_table`.`day`,`time_table`.`hour`,`subject_allocation`.`staff_id`,`course`.`sem`,`course`.`course_name` FROM `subject` INNER JOIN `subject_allocation` ON `subject`.`sub_id`=`subject_allocation`.`sub_id` INNER JOIN `time_table` ON `subject`.`sub_id`=`time_table`.`sub_id` INNER JOIN `staff` ON `staff`.`staff_id`=`subject_allocation`.`staff_id` INNER JOIN `course` ON `course`.`course_id`=`subject`.`cid`WHERE `staff`.`staff_lid`='"+str(session['login_id'])+"'"
    print(qry)
    db=Db()
    res=db.select(qry)
    return render_template('staff/staff timetable.html',data=res)

@app.route('/staff_view_punishment')
def staff_view_punishment():
    qry = "SELECT * FROM punishment"
    db = Db()
    res = db.select(qry)
    return render_template("staff/view punishment.html", data=res)

@app.route('/staff_view_student')
def staff_view_student():

    db=Db()
    qry="SELECT `student`.*,`course`.`course_name` FROM `student` INNER JOIN `course` ON `student`.`cid`=`course`.`course_id`"
    res=db.select(qry)

    return render_template("staff/view student.html",data=res)

# staff section ends





#--------------------------parent------------------













if __name__ == '__main__':
    app.run(debug=True)
