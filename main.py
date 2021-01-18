from flask import Flask, Response, jsonify, json, request
from flask_cors import CORS

app = Flask(__name__)
app.config["DEBUG"] = True


from matching_algo import MatchingInterviewerService

service = MatchingInterviewerService()

# @app.route('/panel/location/<locationId>/role/<roleId>/department/<departmentId>/round/<roundId>', methods=['GET'])
# def fetch_recos(locationId, roleId, departmentId, roundId):
#     print("Hey", role)
#     location = request.view_args['locationId']
#     department = request.view_args['departmentId']
#     interview_round = request.view_args['roundId']
#     skills_string = request.view_args['skills']
#     skills = skills_string.split(',')
#     data_dict = {"role" : role,"location":location,"department":department,"round":interview_round,"skills_required":skills}
#     service.get_best_x_interviwer_info()
#     data_dict = {}
#     return data_dict


@app.route('/panel/location/<locationId>/role/<roleId>/department/<departmentId>/round/<roundId>', methods=['GET'])
def fetch_recos(locationId, roleId, departmentId, roundId):
    location = request.view_args['locationId']
    role = request.view_args['roleId']
    departmentId = request.view_args['departmentId']
    roundId = request.view_args['roundId']
    skills_string = request.args.get('skills')
    skills = []
    if skills_string:
        skills = [x.strip() for x in skills_string.split(',')]
    data_dict = {'location' : location, 'role' : role, 'department' : departmentId, 'round': roundId, "skills_required": skills}
    x = service.get_best_x_interviwer_info(data_dict)
    print(type(x))
    return jsonify(x)
#     return data_dict



app.run()