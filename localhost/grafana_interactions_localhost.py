from grafana_api.grafana_face import GrafanaFace
import json
import requests
#login to the grafana api through the library
grafana_api = GrafanaFace(auth=('admin','admin'), port=3001)

# ORGANIZATIONS 
def _organization_check(organization): #checks if org exists or not in order to create it
	orgs = grafana_api.organizations.list_organization()
	for i in range(len(orgs)):
		if str(organization) in orgs[i]['name']:
			print ("organization already created")
			return 1
	return 0

def _create_organization(organization):
	url='http://admin:admin@localhost:3001/api/orgs'
	data={
		"name":organization,
	}
	headers={"Content-Type": 'application/json'}
	response = requests.post(url, json=data,headers=headers)
	print (response.text)

def _get_current_organization():
	url='http://admin:admin@localhost:3001api/org/'
	response = requests.get(url)
	organization_details = response.json()
	print(organization_details["name"])
	return str(organization_details["name"])

def _get_organization_id(organization_name):
	orgs = grafana_api.organizations.list_organization()
	print (orgs)
	for i in range(len(orgs)):
		if str(organization_name) in orgs[i]['name']:
			return orgs[i]['id']
	return 0 #there is no organization ID zero in grafana


def _change_current_organization_to(new_organization):
	org_id = _get_organization_id(new_organization)
	print ('organization id ', org_id)
	url='http://admin:admin@localhost:3001/api/user/using/' + str(org_id)
	headers={"Content-Type": 'application/json'}
	response = requests.post(url, headers=headers)
	print (response.text)
	print("current organization is now ", new_organization)

def _delete_organization(org_name):
	org_id = _get_organization_id(org_name)
	if org_id != 0:
		print ("deleting organization..", org_name)
		url= 'http://admin:admin@localhost:3001/api/orgs/' + str(org_id)
		headers={"Content-Type": 'application/json'}
		response = requests.delete(url, headers=headers)
		print (response.text)
	else:
		print("organization does not exist")


# USERS 

def _get_all_users(): #returns all users of the selected organization
	url='http://admin:admin@localhost:3001/api/org/users'
	response = requests.get(url)
	user_list = response.json()
	for i in range(len(user_list)):
		print(user_list[i]['login'])
	return user_list

def _user_check(user_org, user):
	#switch to user_org
	_change_current_organization_to(user_org)
	user_list = _get_all_users()
	for i in range(len(user_list)):
		if user_list[i]['login'] == user:
			return user_list[i]['userId']
	return 0 #user not found


def _create_user(user): #creates it and does not assign it to anything
	print("****************************************")
	url='http://admin:admin@localhost:3001/api/admin/users'
	data={
		"name": user["name"],
		"email": user["email"],
		"login":  user["login"],
		"password": user["password"],
	}
	headers={"Content-Type": 'application/json'}
	response = requests.post(url, json=data,headers=headers)
	print (response.text)

def _assign_user_to_organization(organization, user, role):
	org_id=_get_organization_id(organization)
	url='http://admin:admin@localhost:3001/api/orgs/'+ str(org_id)+ '/users'
	data={
		"loginOrEmail": user["login"],
		"role": str(role),
		
	}
	headers={"Content-Type": 'application/json'}
	response = requests.post(url, json=data,headers=headers)
	print (response.text)

def _get_global_user_id(user_login): #without switching to org
	url='http://admin:admin@localhost:3001/api/users/lookup?loginOrEmail=' + str(user_login)
	headers={"Content-Type": 'application/json'}
	response = requests.get(url, headers=headers)
	print (response.text)
	user_data = response.json()
	if 'id' not in user_data: #user does not exists
		print("no such user")
		return 0
	else:
		print(user_data['id'])
		return user_data['id']


def _delete_user(user_login):
	print ("deleting user .. ", user_login)
	user_id = _get_global_user_id(user_login)
	if user_id != 0:
		url = 'http://admin:admin@localhost:3001/api/admin/users/' + str(user_id)
		headers={"Content-Type": 'application/json'}
		response = requests.delete(url, headers=headers)
		print (response.text)

def _remove_user_from_org(user_login):
	print ("removing user from current organization .. ", user_login)
	user_id = _get_global_user_id(user_login)
	if user_id != 0:
		url = 'http://admin:admin@localhost:3001/api/org/users/' + str(user_id)
		headers={"Content-Type": 'application/json'}
		response = requests.delete(url, headers=headers)
		print (response.text)

# DATASOURCES
def _create_datasource(name, database, admin_name, admin_pass):
	url='http://admin:admin@localhost:3001/api/datasources'
	data={
		"name":name,
		"type":"influxdb",
		"url":"http://localhost:8086",
		"access":"direct", #vs proxy
		"password": admin_pass,
		"user": admin_name,
		"database": database,
		"httpMode": "GET"  #very important field!!!

	}
	headers={"Content-Type": 'application/json'}
	response = requests.post(url, json=data,headers=headers)
	print (response.text)


def _delete_datasource(datasource_name):
	url="http://admin:admin@localhost:3001/api/datasources/name/" + str(datasource_name)
	headers={"Content-Type": 'application/json'}
	response = requests.delete(url, headers=headers)
	print (response.text)

# DASHBOARDS

def _create_dashboard(name):
	url="http://admin:admin@localhost:3001/api/dashboards/db"
	headers={"Content-Type": 'application/json'}
	data = {
		"dashboard": {
			"id": None, #for new dashboard
			"uid": None,
			"title": name,
			"tags": [ "templated" ],
			"timezone": "browser",
			"schemaVersion": 16,
			"version": 0,
		},
		"folderId": 0,
		"overwrite": False #new dashboard
		}
	response = requests.post(url, json=data,headers=headers)
	print (response.text)

def _update_dashboard(dash_json,name, uid):
	#future versions: add time intervals too
	url="http://admin:admin@localhost:3001/api/dashboards/db"
	headers={"Content-Type": 'application/json'}

	dash_json['title'] = name
	dash_json['uid'] = uid
	dash_json["refresh"]= "30s" #default refresh rate
	data = {}
	data["dashboard"]= dash_json
	data["folderId"]= 0
	data["overwrite"]= True
	
	response = requests.post(url, json=data,headers=headers)
	print (response.text)

def _get_dashboard_uid(dash_title):
	url= "http://admin:admin@localhost:3001/api/search?folderIds=0&query=&starred=false"
	headers={"Content-Type": 'application/json'}
	response = requests.get(url, headers=headers)
	#print (response.text)
	dash_list = response.json()
	for i in range(len(dash_list)):
		if dash_list[i]['title'] == dash_title:
			return dash_list[i]['uid']
	return 0 #user not found

def _get_dashboard_json(dash_title, org):
	_change_current_organization_to(org)
	dash_uid = _get_dashboard_uid(dash_title)
	if dash_uid != 0:
		url= "http://admin:admin@localhost:3001/api/dashboards/uid/" + str(dash_uid)
		headers={"Content-Type": 'application/json'}
		response = requests.get(url, headers=headers)

		data = response.json()
		print("************************************")
		print (data['dashboard']['panels'])
	else:
		print("get dash json not working")

def _delete_dashboard(dash_title):
	dash_uid=_get_dashboard_uid(dash_title)
	if dash_uid != 0:
		print ("deleting dashboard ...", dash_title)
		url= "http://admin:admin@localhost:3001/api/dashboards/uid/" + str(dash_uid)
		headers={"Content-Type": 'application/json'}
		response = requests.delete(url, headers=headers)
		print (response.text)
	else:
		print("dashboard does not exist")
