# rest-flask-vv

# an app allows 5 tipes of request on task :
# GET (all), GET (for 1) POST, PUT, DELETE
# 
# and 3 type on users :
# GET (all), POST, DELETE
# 
# curl commands for check examples :
#
# Get all tasks :
# curl -u SuperUser:qwerty https://rest-flask-vv.herokuapp.com//todo/api/v1.0/tasks
#
# Get one task by id, last number URI :
# curl -u SuperUser:qwerty https://rest-flask-vv.herokuapp.com//todo/api/v1.0/tasks/1
#
# Add task :
# curl -u SuperUser:querty -X POST https://rest-flask-vv.herokuapp.com//todo/api/v1.0/tasks -H "Content-Type: application/json" -d "{\"title\":\"Read a book\", \"description\":\"Nice book\"}"
#
# Update task :
# curl -X PUT -u SuperUser:qwerty https://rest-flask-vv.herokuapp.com//todo/api/v1.0/tasks/2 -H "Content-Type: application/json" -d "{\"title\":\"Nice book Updated\",\"done\":true}"
#
#
# There are 3 different security keys for each operation with users
#
# Get all users :
# curl -X GET -u SuperUser:qwerty -H "Content-Type: application/json" -d "{\"secret_key\":\"AJ!#r0vU4Ts1A*
#
# Add user :
# curl -u YourUniqueUserName:qwerty -X POST -H "Content-Type: application/json" -d "{\"name\":\"SuperUser443\",\"password\":\"qwerty\",\"secret_key\":\"2.-q6uw$,pqbc[(bM{Sly~ExT/Hkru\"}" https://rest-flask-vv.herokuapp.com//todo/api/v1.0/users
#
#
# Delete user :
# curl -X DELETE -u SuperUser:qwerty -H "Content-Type: application/json" -d "{\"secret_key\":\"2.-q6uw$,pqbc[(bM{Sly~ExT/Hkru\"}" https://rest-flask-vv.herokuapp.com//todo/api/v1.0/users/<user_id>
#
#
#
# took an idea from https://habr.com/ru/post/246699/