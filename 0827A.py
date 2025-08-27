import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Firebase database 인증 및 앱 초기화
cred = credentials.Certificate('testkey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://test-c7ea9-default-rtdb.firebaseio.com/' 
})


ref = db.reference('fill_A')
A=(ref.get())
ref = db.reference('fill_B')
B=(ref.get())
ref = db.reference('fill_C')
C=(ref.get())

A=A+10
B=B-2
C=C+7

ref = db.reference()
ref.update({'fill_A' : A})
ref.update({'fill_B' : B})
ref.update({'fill_C' : C})