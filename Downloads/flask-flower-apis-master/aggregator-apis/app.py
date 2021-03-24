from flask import Flask, request, json, send_file, Response, stream_with_context
import os
from constants import SECRET
import jwt
import yaml
import shutil
import flwr as fl


app = Flask(__name__)


def returnResponse(statusCode, message):
    data = {'message': message}
    response = app.response_class(status=statusCode, response=json.dumps(
        data), mimetype="application/json")
    return response


@app.route('/create-project', methods=['POST'])
def createProject():
    request_data = request.get_json()
    if request.method == 'POST':
        main_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(os.path.join(main_dir, 'projects')):
            os.mkdir(os.path.join(main_dir, "projects"))
        project_path = os.path.join(main_dir, 'projects')

        projectName = request_data['projectName']

        if not os.path.exists(os.path.join(project_path, projectName)):
            os.mkdir(os.path.join(project_path, projectName))
            os.mkdir(os.path.join(project_path, projectName, 'configs'))
            os.mkdir(os.path.join(project_path, projectName, 'data'))
            os.mkdir(os.path.join(project_path, projectName, 'model'))
            os.mkdir(os.path.join(project_path, projectName, 'preprocess'))
            token = jwt.encode({"projectName": projectName},
                               SECRET, algorithm="HS256")

            token_file = open(os.path.join(
                project_path, projectName, "token.txt"), 'w')
            token_file.write(token)
            token_file.close()

            return returnResponse(200, (projectName + ' created successfully'))
        else:
            return returnResponse(409, (projectName + ' already exists'))


@app.route('/all-projects', methods=['GET'])
def allProjects():
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


@app.route('/delete-project', methods=['DELETE'])
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


@app.route('/<projectName>/server-configs', methods=['GET', 'PUT'])
def serverConfigs(projectName):
    if request.method == 'GET':
        main_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(os.path.join(main_dir, 'projects')):
            return returnResponse(409, "You have no projects")

        project_path = os.path.join(main_dir, "projects")

        if not os.path.exists(os.path.join(project_path, projectName)):
            return returnResponse(409, (projectName + "Does not exist"))

        config_path = os.path.join(project_path, projectName, "configs")

        if not os.path.exists(os.path.join(config_path, "server.yaml")):
            return returnResponse(200, {})
        with open(os.path.join(config_path, "server.yaml"), 'r') as confs:
            return returnResponse(200, yaml.safe_load(confs))

    if request.method == 'PUT':
        main_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(os.path.join(main_dir, 'projects')):
            return returnResponse(409, "You have no projects")

        project_path = os.path.join(main_dir, "projects")

        if not os.path.exists(os.path.join(project_path, projectName)):
            return returnResponse(409, (projectName + " Does not exist"))

        config_path = os.path.join(project_path, projectName, "configs")
        request_data = request.get_json()
        with open(os.path.join(config_path, "server.yaml"), 'w') as conf:
            yaml.safe_dump(request_data, conf)
        return returnResponse(200, "Server configs written")


@app.route('/<projectName>/client-configs', methods=['GET', 'PUT'])
def clientConfigs(projectName):
    if request.method == 'GET':
        main_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(os.path.join(main_dir, 'projects')):
            return returnResponse(409, "You have no projects")
        project_path = os.path.join(main_dir, "projects")

        if not os.path.exists(os.path.join(project_path, projectName)):
            return returnResponse(409, (projectName + "Does not exist"))

        config_path = os.path.join(project_path, projectName, "configs")

        if not os.path.exists(os.path.join(config_path, "client.yaml")):
            return returnResponse(200, {})
        with open(os.path.join(config_path, "client.yaml"), 'r') as confs:
            return returnResponse(200, yaml.safe_load(confs))

    if request.method == 'PUT':
        main_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(os.path.join(main_dir, 'projects')):
            return returnResponse(409, "You have no projects")

        project_path = os.path.join(main_dir, "projects")

        if not os.path.exists(os.path.join(project_path, projectName)):
            return returnResponse(409, (projectName + " Does not exist"))

        config_path = os.path.join(project_path, projectName, "configs")
        request_data = request.get_json()
        with open(os.path.join(config_path, "client.yaml"), 'w') as conf:
            yaml.safe_dump(request_data, conf)
        return returnResponse(200, "Client configs written")


@app.route('/<projectName>/ai-model', methods=['GET', 'PUT'])
def aiModel(projectName):
    #! Not Working Get this to work
    # if request.method == 'GET':
    #     main_dir = os.path.dirname(os.path.abspath(__file__))
    #     if not os.path.exists(os.path.join(main_dir, 'projects')):
    #         return returnResponse(409, "You have no projects")

    #     project_path = os.path.join(main_dir, "projects")

    #     if not os.path.exists(os.path.join(project_path, projectName)):
    #         return returnResponse(409, (projectName + " Does not exist"))

    #     model_path = os.path.join(project_path, projectName, "model")
    #     if not os.path.exists(os.path.join(model_path, 'model.h5')):
    #         return

    #     return send_file(os.path.join(model_path, 'model.h5'), as_attachment=True)

    if request.method == 'PUT':
        main_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(os.path.join(main_dir, 'projects')):
            return returnResponse(409, "You have no projects")

        project_path = os.path.join(main_dir, "projects")

        if not os.path.exists(os.path.join(project_path, projectName)):
            return returnResponse(409, (projectName + " Does not exist"))

        model_path = os.path.join(project_path, projectName, "model")

        model = request.files['file']

        model.save(os.path.join(model_path, "model.h5"))

        return returnResponse(200, "Model successfully uploaded")


@app.route('/<projectName>/preprocessor', methods=['GET', 'PUT'])
def preprocessingScript(projectName):
    #! Not Working Get this to work
    if request.method == 'GET':
        main_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(os.path.join(main_dir, 'projects')):
           return returnResponse(409, "You have no projects")

         project_path = os.path.join(main_dir, "projects")

        if not os.path.exists(os.path.join(project_path, projectName)):
            return returnResponse(409, (projectName + " Does not exist"))

         preprocess_path = os.path.join(project_path, projectName, "preprocess")
         if not os.path.exists(os.path.join(preprocess_path, 'preprocess.py')):
             return

         return send_file(os.path.join(preprocess_path, 'preprocess.py'), as_attachment=True)

    if request.method == 'PUT':
        main_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(os.path.join(main_dir, 'projects')):
            return returnResponse(409, "You have no projects")

        project_path = os.path.join(main_dir, "projects")

        if not os.path.exists(os.path.join(project_path, projectName)):
            return returnResponse(409, (projectName + " Does not exist"))

        preprocess_path = os.path.join(project_path, projectName, "preprocess")

        preprocess = request.files['file']

        preprocess.save(os.path.join(preprocess_path, "preprocess.py"))

        return returnResponse(200, "preprocessing file successfully uploaded")


@app.route('/send-project-details', methods=['GET'])
def sendProjectDetails():
    if request.method == 'GET':
        main_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(os.path.join(main_dir, 'projects')):
            return returnResponse(409, "You have no projects")

        project_path = os.path.join(main_dir, "projects")

        request_data = request.get_json()
        token = request_data['token']
        projectToken = ""

        for dir in os.listdir(project_path):
            with open(os.path.join(project_path, dir, "token.txt"), 'r') as token_file:
                projectToken = token_file.readline()

            if token == projectToken:
                return returnResponse(200, dir)

        return returnResponse(409, "This project does not exist")


@app.route('/<projectName>/start-aggregator', methods=['GET'])
def startAggregator(projectName):
    if request.method == 'GET':
        main_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(os.path.join(main_dir, 'projects')):
            return returnResponse(409, "You have no projects")

        project_path = os.path.join(main_dir, "projects")

        if not os.path.exists(os.path.join(project_path, projectName)):
            return returnResponse(409, (projectName + " Does not exist"))

        config_path = os.path.join(
            project_path, projectName, "configs", "server.yaml")

        def load_server_configs():
            with open(config_path, 'r') as stream:
                return yaml.safe_load(stream)

        # Get server configs
        server_configs = load_server_configs()

        # Create strategy
        strategy_configs = server_configs['strategy']
        strategy = fl.server.strategy.FedAvg(
            min_fit_clients=(strategy_configs['min_fit_clients']
                             if 'min_fit_clients' in strategy_configs else 2),
            min_eval_clients=(strategy_configs['min_eval_clients']
                              if 'min_eval_clients' in strategy_configs else 2),
            min_available_clients=(strategy_configs['min_available_clients']
                                   if 'min_available_clients' in strategy_configs else 2),
        )

        # Start Flower server for four rounds of federated learning
        server_ip = server_configs['ip'] if 'ip' in server_configs else '[::]:8080'

        config = server_configs['config']

        #! Make this return a Server started response and a Ended Response
        def start():
            yield "aggregator starting"
            fl.server.start_server(server_ip, config={"num_rounds": 5})
            yield "aggregator closed"

        return Response(stream_with_context(start()))


if __name__ == "__main__":
    app.run(debug=True)
