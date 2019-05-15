# qa_space

docker-compose -f docker-compose-test.yaml build qa_space_auth build qa_space_auth
docker-compose -f docker-compose-test.yaml up qa_space_auth run qa_space_auth container
docker-compose -f docker-compose-test.yaml down stop all containers


Prepare dbs:
docker-compose -f docker-compose-test.yaml run qa_space_auth python db.py
docker-compose -f docker-compose-test.yaml run qa_space python db.py