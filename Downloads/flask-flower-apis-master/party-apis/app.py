from flask import Flask as flask
from flask import request
from gen_directory_agg import gen
from projects import send_projects, delete_project
from gen_model import get_model
import yaml
from constants import *

app = flask(__name__)

def returnResponse(statusCode, message):
    data = {'message': message}
    response = app.response_class(status=statusCode, response=json.dumps(
        data), mimetype="application/json")
    return response


@app.route('/obtain-project/<token>', methods=['GET'])
def obtainProject(token):
    if request.method == 'GET':

        url = 'http://0.0.0.0:5000/send-project-details/'+token

        print(url)
        res = requests.get(url)
        return res.json()

@app.route('/all-projects', methods=['GET'])
def getProjects():
   if request.method == 'GET':
        main_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(os.path.join(main_dir, 'projects')):
            return returnResponse(409, "You have no projects")

        project_path = os.path.join(main_dir, "projects")

        projects = []
        for dir in os.listdir(project_path):
            projects.append(dir)

        if len(projects) == 0:
            return returnResponse(409, "You have no projects")

        return returnResponse(200, projects)

@app.route('/delete-project/<id>', methods=['DELETE'])
def deleteProject():
     if request.method == 'DELETE':
       def deleteProject():
    if request.method == 'DELETE':
        main_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(os.path.join(main_dir, 'projects')):
            return returnResponse(409, "You have no projects")

        project_path = os.path.join(main_dir, "projects")

        request_data = request.get_json()
        projectName = request_data['projectName']

        if not os.path.exists(os.path.join(project_path, projectName)):
            return returnResponse(409, (projectName + " Does not exist"))

        shutil.rmtree(os.path.join(project_path, projectName))

        return returnResponse(200, (projectName + " successfully deleted"))





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)