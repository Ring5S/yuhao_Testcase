import pymongo
from config import runtime_json

cloud_password = "E8XWXNHj8U_cfxlh"
# MongoDB 集群信息
MONGODB_CLUSTER = {
    "NODE1": {
        "IP": "10.67.187.123",
        "PORT": 27017,
        "ip_username": "root",
        "ip_password": "huawei",
        "mongodb_sh": "/usr/local/mongodb/mongodb.sh"
    },
    "NODE2": {
        "IP": "10.67.187.55",
        "PORT": 27017,
        "ip_username": "root",
        "ip_password": "huawei",
        "mongodb_sh": "/usr/local/mongodb/mongodb.sh"
    },
    "NODE3": {
        "IP": "10.67.187.16",
        "PORT": 27017,
        "ip_username": "root",
        "ip_password": "huawei",
        "mongodb_sh": "/usr/local/mongodb/mongodb.sh"
    },
    "NODE4": {
        "IP": "10.67.187.17",
        "PORT": 27017,
        "ip_username": "root",
        "ip_password": "huawei",
        "mongodb_sh": "/usr/local/mongodb/mongodb.sh"
    },
    "NODE86": {
        "IP": "10.244.146.30",
        "PORT": 8635,
        "ip_username": "rwuser",
        "ip_password": cloud_password,
        "mongodb_sh": "/usr/local/mongodb/mongodb.sh"
    },
    "NODE86_2": {
        "IP": "10.244.146.182",
        "PORT": 8635,
        "ip_username": "rwuser",
        "ip_password": cloud_password,
        "mongodb_sh": "/usr/local/mongodb/mongodb.sh"
    },
    "NODE_CLOUD": {
        "IP": "10.244.146.88",
        "PORT": 8635,
        "ip_username": "rwuser",
        "ip_password": cloud_password,
        "mongodb_sh": "/usr/local/mongodb/mongodb.sh"
    }
}


class DBOperation:
    def __init__(self, Test_Framework, collection_name, mongo_env="cloud"):
        """
         init collection handle for mongodb
        :param db_name:name of db for initing
        :param collection_name:collection name of db for initing
        :param  mongo_env: mongodb env, local_base = 10.67.187.123; local_86 = 10.90.54.86; cloud = Cloud mongodb
        """
        self.collection_name = collection_name
        self.mongo_env = mongo_env
        self.Test_Framework = Test_Framework

    def collection_handle(self):
        """
        :param collection_name:collection name of db for initing
        :param  env: mongodb env, local_base = 10.67.187.123; local_86 = 10.90.54.86; cloud = Cloud mongodb
        """
        env = self.mongo_env
        collection_name = self.collection_name
        if env == "local_86":
            server_ip = MONGODB_CLUSTER["NODE86"]["IP"]
            password = MONGODB_CLUSTER["NODE86"]["ip_password"]
            username = MONGODB_CLUSTER["NODE86"]["ip_username"]
            port = MONGODB_CLUSTER["NODE86"]["PORT"]
        elif env == "cloud":
            server_ip = MONGODB_CLUSTER["NODE_CLOUD"]["IP"]
            password = MONGODB_CLUSTER["NODE_CLOUD"]["ip_password"]
            username = MONGODB_CLUSTER["NODE_CLOUD"]["ip_username"]
            port = MONGODB_CLUSTER["NODE_CLOUD"]["PORT"]
        else:
            server_ip = MONGODB_CLUSTER["NODE2"]["IP"]
            password = MONGODB_CLUSTER["NODE2"]["ip_password"]
            username = MONGODB_CLUSTER["NODE2"]["ip_username"]
            port = MONGODB_CLUSTER["NODE2"]["PORT"]
        client = pymongo.MongoClient(server_ip, port)
        client.admin.authenticate(username, password, mechanism="SCRAM-SHA-1")
        # 读取MNN，MindSpore，BOLT，Tensorflow
        if self.Test_Framework == "MNN":
            db = client["MNN"]
        elif self.Test_Framework == "TFLITE":
            db = client["Tensorflow"]
        elif self.Test_Framework == "BOLT":
            db = client["BOLT"]
        elif self.Test_Framework == "TNN":
            db = client["TNN"]
        else:
            db = client["MindSpore"]
        collection_handle = db[collection_name]
        return collection_handle

    def get_original_json(self, _id):
        # 连交付模型仓
        collection_handle_cloud = self.collection_handle()
        exit_json = collection_handle_cloud.find_one({"_id": _id})
        return exit_json

    def update_db_official(self, ori_list, net, _id):
        original_json = self.get_original_json(_id)
        # print(f"original_json:{original_json}")
        try:
            RunTime = {
                "Thread_1": {
                    # 0，4，5
                    "Init": ori_list[0][0],
                    "Init_range": {"Avg": ori_list[0][0],
                                   "Max": ori_list[0][4],
                                   "Min": ori_list[0][5]
                                   },
                    "Run": {
                        "Min": ori_list[0][2],
                        "Max": ori_list[0][1],
                        "Avg": ori_list[0][3]
                    }
                },
                "Thread_2": {
                    "Init": ori_list[1][0],
                    "Init_range": {"Avg": ori_list[1][0],
                                   "Max": ori_list[1][4],
                                   "Min": ori_list[1][5]
                                   },
                    "Run": {
                        "Min": ori_list[1][2],
                        "Max": ori_list[1][1],
                        "Avg": ori_list[1][3]
                    }
                },
                "Thread_4": {
                    "Init": ori_list[2][0],
                    "Init_range": {"Avg": ori_list[2][0],
                                   "Max": ori_list[2][4],
                                   "Min": ori_list[2][5]
                                   },
                    "Run": {
                        "Min": ori_list[2][2],
                        "Max": ori_list[2][1],
                        "Avg": ori_list[2][3]
                    }
                }
            }
            # print(original_json['NetTestResult'][f'{net}'])
            original_json['NetTestResult'][net]["RunTime"] = RunTime
            # print(original_json['NetTestResult'][net])
            collection_handle_cloud = self.collection_handle()
            res = collection_handle_cloud.update_one(
                {"_id": _id},
                {"$set": {"NetTestResult": original_json['NetTestResult']}})
            return res.modified_count
        except Exception as e:
            print(f"update db Fail!,resList is {ori_list}")
            print(e)

    def update_db_openlite(self, ori_list, net, _id, net_type):
        original_json = self.get_original_json(_id)
        try:
            RunTime = {
                "Thread_1": {
                    # 0，4，5
                    "Init": ori_list[0][0],
                    "Init_range": {"Avg": ori_list[0][0],
                                   "Max": ori_list[0][4],
                                   "Min": ori_list[0][5]
                                   },
                    "Run": {
                        "Min": ori_list[0][2],
                        "Max": ori_list[0][1],
                        "Avg": ori_list[0][3]
                    }
                },
                "Thread_2": {
                    "Init": ori_list[1][0],
                    "Init_range": {"Avg": ori_list[1][0],
                                   "Max": ori_list[1][4],
                                   "Min": ori_list[1][5]
                                   },
                    "Run": {
                        "Min": ori_list[1][2],
                        "Max": ori_list[1][1],
                        "Avg": ori_list[1][3]
                    }
                },
                "Thread_4": {
                    "Init": ori_list[2][0],
                    "Init_range": {"Avg": ori_list[2][0],
                                   "Max": ori_list[2][4],
                                   "Min": ori_list[2][5]
                                   },
                    "Run": {
                        "Min": ori_list[2][2],
                        "Max": ori_list[2][1],
                        "Avg": ori_list[2][3]
                    }
                }
            }
            # print(original_json['NetTestResult'][net_type][net])
            original_json['NetTestResult'][net_type][net]["RunTime"] = RunTime
            collection_handle_cloud = self.collection_handle()
            res = collection_handle_cloud.update_one(
                {"_id": _id},
                {"$set": {"NetTestResult": original_json['NetTestResult']}})
            return res.modified_count
        except Exception as e:
            print(f"update db Fail!,resList is {ori_list}")
            print(e)

    def update_NewModel_official(self, net_info, _id):
        try:
            # _id = "MNN_Do_TD_V100R002CMASTER_1.1.1.6_Mate40"
            model_name, model_size = net_info[0], net_info[1]
            original_json = self.get_original_json(_id)
            original_json['NetTestResult'][model_name] = runtime_json
            original_json['NetTestResult'][model_name]["ModelSize"] = model_size
            # print(original_json['NetTestResult'][model_name])
            collection_handle_cloud = self.collection_handle()
            res = collection_handle_cloud.update_one(
                {"_id": _id},
                {"$set": {"NetTestResult": original_json['NetTestResult']}})
            return res.modified_count
        except Exception as e:
            print(f"update db Fail!,resList is {net_info}")
            print(e)
