from firebase import firebase

firebase = firebase.FirebaseApplication('https://iot-smart-garden-44a0f.firebaseio.com/', None)
result = firebase.get('/iot-smart-garden-44a0f/enter the project bucket here/','motor_state')
print(motor_state)


