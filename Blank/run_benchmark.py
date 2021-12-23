import re
import subprocess
import os
import time
import json
import sys
from multiprocessing import Process
from numpy import mean
import mongo
from log import create_logger
from config import Terminal_Device, runtime_json, MnnOfficialModel, MnnOpenLiteModel, TfliteOfficialModel, \
    TfliteOpenLiteModel, BoltOfficialModel, BoltOpenLiteModel, NpuSupportModels, GpuSupportModels, OfficialTestModels

# 在脚本目录下直接生成标杆流水线日志
PRE_HOME = os.getcwd()
LOG_FILE = os.path.join(PRE_HOME, "benchmark.log")
print("Log Path:", LOG_FILE)
# log
logger = create_logger("benchmark.log", "info", LOG_FILE)


class SingleModelTest:
    """
    该类用于存放标杆单个模型跑测流程
    """

    def __init__(self, device_id, data_type, backend, if_official):
        self.device_id = device_id
        self.data_type = data_type
        self.backend = backend
        self.if_official = if_official

    def run_mnn_benchmark(self, net):
        loop_time = "10"
        phone_mnn_path = "/data/local/tmp/mnn"
        # 交付模型目录
        official_model_path = MnnOfficialModel
        # 开源模型目录
        openlite_model_path = MnnOpenLiteModel
        per_info_lists = []
        # 推送模型
        if self.if_official:
            push_cmd = f"adb -s {self.device_id} shell 'rm -rf /data/local/tmp/mnn/models';" \
                       f"adb -s {self.device_id} shell 'mkdir -p " \
                       f"/data/local/tmp/mnn/models';adb -s {self.device_id} push {official_model_path}/{net}.mnn " \
                       f"/data/local/tmp/mnn/models/ "
        else:
            push_cmd = f"adb -s {self.device_id} shell 'rm -rf /data/local/tmp/mnn/models';" \
                       f"adb -s {self.device_id} shell 'mkdir -p " \
                       f"/data/local/tmp/mnn/models';adb -s {self.device_id} push {openlite_model_path}/{net}.mnn " \
                       f"/data/local/tmp/mnn/models/ "
        push_res = subprocess.getstatusoutput(push_cmd)
        if push_res[0] == 0:
            logger.info("PUSH Model {} SUCCESS".format(net))
        # 推送后开始测试
        if self.backend == "GPU":
            self.backend = "OPENGL"
        for thread in [1, 2, 4]:
            benchmark_cmd = f"cd {phone_mnn_path};export LD_LIBRARY_PATH=./libs;chmod 777 benchmark;" \
                            f"./benchmark -M=./models/{net}.mnn " \
                            f"-N={loop_time} -T={thread} -D={self.data_type} -P={self.backend}"
            output = subprocess.getstatusoutput(f"adb -s {self.device_id} shell '{benchmark_cmd}'")[1]
            self.wait_device_found(output)
            logger.info(benchmark_cmd)
            logger.info(output)
            try:
                # 获取初始化最小值和最大值
                init_string_min = re.findall("init_min is:.*", output)
                init_string_max = re.findall("init_max is:.*", output)
                init_min = init_string_min[0].split(": ")[-1]
                init_max = init_string_max[0].split(": ")[-1]
                # logger.info(f"init_min: {init_min} init_max:{init_max}")
                # 获取runtime和初始化平均值
                per_num_info = output.split("mnn")[1].strip(" ").split("=")
                per_info_num_list = [re.findall(r"\d+\.?\d*", str.strip("")) for str in per_num_info]
                per_info_lists.append([per_info_num_list[1][0], per_info_num_list[2][0],
                                       per_info_num_list[3][0], per_info_num_list[4][0], init_max, init_min])
            except IndexError as e:  # pylint: disable=invalid-name
                logger.error(
                    "{} model run fail, result failed to obtain the value!!! fail output value: {}".format(
                        net,
                        e))
                per_info_lists.append([0, 0, 0, 0, 0, 0])
            logger.info(per_info_lists)
        return per_info_lists

    def run_mnn_x86(self, net):
        loop_time = "10"
        x86_mnn_path = "/home/xueyuhao/BenchmarkNew/MNN/X86_benchmark"
        # 交付模型目录
        official_model_path = MnnOfficialModel
        # 开源模型目录
        openlite_model_path = MnnOpenLiteModel
        # 推送模型
        if self.if_official:
            push_cmd = f"rm -rf {x86_mnn_path}/models;mkdir -p {x86_mnn_path}/models;" \
                       f"cp {official_model_path}/{net}.mnn {x86_mnn_path}/models"
        else:
            push_cmd = f"rm -rf {x86_mnn_path}/models;mkdir -p {x86_mnn_path}/models;" \
                       f"cp {openlite_model_path}/{net}.mnn {x86_mnn_path}/models"
        push_res = subprocess.getstatusoutput(push_cmd)
        if push_res[0] == 0:
            logger.info("PUSH Model {} SUCCESS".format(net))
        else:
            logger.info("PUSH Model {} Fail".format(net))
        per_info_lists = []
        for thread in [1, 2, 4]:
            benchmark_cmd = f"cd {x86_mnn_path};export LD_LIBRARY_PATH=./libx86;chmod 777 benchmark_x86;" \
                            f"./benchmark_x86 -M=./models/{net}.mnn -N={loop_time} -T={thread}"
            # logger.info(f"adb -s {device_id} shell {benchmark_cmd}")
            output = subprocess.getstatusoutput(benchmark_cmd)[1]
            logger.info(output)
            try:
                # 获取初始化最小值和最大值
                init_string_min = re.findall("init_min is:.*", output)
                init_string_max = re.findall("init_max is:.*", output)
                init_min = init_string_min[0].split(": ")[-1]
                init_max = init_string_max[0].split(": ")[-1]
                # logger.info(f"init_min: {init_min} init_max:{init_max}")
                # 获取runtime和初始化平均值
                per_num_info = output.split("mnn")[1].strip(" ").split("=")
                per_info_num_list = [re.findall(r"\d+\.?\d*", str.strip("")) for str in per_num_info]
                per_info_lists.append([per_info_num_list[1][0], per_info_num_list[2][0],
                                       per_info_num_list[3][0], per_info_num_list[4][0], init_max, init_min])
            except IndexError as e:  # pylint: disable=invalid-name
                logger.error(
                    "{} model run fail, result failed to obtain the value!!! fail output value: {}".format(
                        net,
                        e))
                per_info_lists.append([0, 0, 0, 0, 0, 0])
            logger.info(per_info_lists)
        return per_info_lists

    def run_tflite_benchmark(self, net):
        """
        TFLITE实际可执行后端参数很多，但是鉴于平台上只展现CPU，GPU_CL，GPU_CL_FP16，所以脚本只更新...
        :param net:
        :return per_info_lists
        """
        init_runtime = 5
        loop_time = "10"
        phone_tflite_path = "/data/local/tmp/tflite"
        # 交付模型目录
        official_model_path = TfliteOfficialModel
        # 开源模型目录
        openlite_model_path = TfliteOpenLiteModel
        per_info_lists = []
        # 推送模型
        if self.if_official:
            push_cmd = f"adb -s {self.device_id} shell 'rm -rf /data/local/tmp/tflite/models';" \
                       f"adb -s {self.device_id} shell 'mkdir -p " \
                       f"/data/local/tmp/tflite/models';adb -s {self.device_id} " \
                       f"push {official_model_path}/{net}.tflite data/local/tmp/tflite/models/ "
        else:
            push_cmd = f"adb -s {self.device_id} shell 'rm -rf /data/local/tmp/tflite/models';" \
                       f"adb -s {self.device_id} shell 'mkdir -p " \
                       f"/data/local/tmp/tflite/models';adb -s {self.device_id}  " \
                       f"push {openlite_model_path}/{net}.tflite /data/local/tmp/tflite/models/ "
        push_res = subprocess.getstatusoutput(push_cmd)
        if push_res[0] == 0:
            logger.info("PUSH Model {}.tflite SUCCESS".format(net))
        # 推送后开始测试
        for thread in [1, 2, 4]:
            benchmark_cmd = f"cd {phone_tflite_path};chmod 777 benchmark_model;" \
                            f"./benchmark_model --graph=./models/{net}.tflite --num_threads={thread} " \
                            f"--warmup_runs=3 --num_runs={loop_time}"
            if self.backend == "CPU" and self.data_type == "float32":
                benchmark_cmd += " --use_xnnpack=true"
            elif self.backend == "GPU" and self.data_type == "float32":
                benchmark_cmd += " --use_gpu=true --gpu_backend=cl --gpu_precision_loss_allowed=false"
            elif self.backend == "GPU" and self.data_type == "float16":
                benchmark_cmd += " --use_gpu=true --gpu_backend=cl --gpu_precision_loss_allowed=true"
            else:
                print("ERROR: TFLITE不支持CPU_FP16及NPU")
                sys.exit()
            logger.info(benchmark_cmd)
            output = subprocess.getstatusoutput(f"adb -s {self.device_id} shell '{benchmark_cmd}'")[1]
            logger.info(output)
            self.wait_device_found(output)
            init_list = []
            for runtime in range(init_runtime):
                # 获取初始化值
                logger.info("get init time {}".format(runtime))
                run_init_cmd = f"cd {phone_tflite_path};timeout 5 ./benchmark_model --graph=./models/{net}.tflite " \
                               f"--num_threads={thread} --num_runs=1"
                # print(f"adb -s {device_id} shell 'timeout 1 {run_init_cmd}'")
                res = subprocess.getstatusoutput(f"adb -s {self.device_id} shell '{run_init_cmd}'")[1]
                try:
                    per = re.findall("Initialized session in.*", res)
                    init_time = per[0].split("in ")[-1]
                    init_time = init_time.split("ms")[0]
                    init_list.append(float(init_time))
                except Exception as e:
                    logger.error(e)
                    init_list = [0, 0, 0]
            try:
                # 截取结果数据
                init_time_max, init_time_min = max(init_list), min(init_list)
                init_avg = mean(init_list)
                logger.info(
                    "init time max:{};init time min:{},init time avg:{}".format(init_time_max, init_time_min, init_avg))
                pers = re.findall("count.*", output)
                run_per = pers[-1].split("=")
                run_min, run_max, run_avg = run_per[4].split(" ")[0], run_per[5].split(" ")[0], run_per[6].split(" ")[0]
                per_info_time = [init_avg, float(run_max) / 1000,
                                 float(run_min) / 1000, float(run_avg) / 1000, init_time_max, init_time_min]
                per_info_lists.append(per_info_time)
            except IndexError as e:  # pylint: disable=invalid-name
                logger.error(
                    "{} model run fail, result failed to obtain the value!!! fail output value: {}".format(
                        net,
                        e))
                per_info_lists.append([0, 0, 0, 0, 0, 0])
            logger.info(per_info_lists)
        return per_info_lists

    def run_bolt_benchmark(self, net):
        """
        bolt框架只支持跑armCPU和x86，且只支持1线程
        :return:
        """
        loop_time = "10"
        phone_bolt_path = "/data/local/tmp/bolt"
        # 交付模型目录
        official_model_path = BoltOfficialModel
        # 开源模型目录
        openlite_model_path = BoltOpenLiteModel
        per_info_lists = []
        # 推送模型
        if self.if_official and self.data_type == "float16":
            push_cmd = f"adb -s {self.device_id} shell 'rm -rf {phone_bolt_path}/models';" \
                       f"adb -s {self.device_id} shell 'mkdir -p " \
                       f"{phone_bolt_path}/models';adb -s {self.device_id} push " \
                       f"{official_model_path}/bolt_64_fp16/{net}_f16.bolt {phone_bolt_path}/models/ "
        elif self.if_official is False and self.data_type == "float16":
            push_cmd = f"adb -s {self.device_id} shell 'rm -rf {phone_bolt_path}/models';" \
                       f"adb -s {self.device_id} shell 'mkdir -p " \
                       f"{phone_bolt_path}/models';adb -s {self.device_id} push " \
                       f"{openlite_model_path}/bolt_64_fp16/{net}_f16.bolt {phone_bolt_path}/models/ "
        elif self.if_official and self.data_type == "float32":
            push_cmd = f"adb -s {self.device_id} shell 'rm -rf {phone_bolt_path}/models';" \
                       f"adb -s {self.device_id} shell 'mkdir -p " \
                       f"{phone_bolt_path}/models';adb -s {self.device_id} push " \
                       f"{official_model_path}/bolt_64_fp32/{net}_f32.bolt {phone_bolt_path}/models/ "
        elif self.if_official is False and self.data_type == "float32":
            push_cmd = f"adb -s {self.device_id} shell 'rm -rf {phone_bolt_path}/models';" \
                       f"adb -s {self.device_id} shell 'mkdir -p " \
                       f"{phone_bolt_path}/models';adb -s {self.device_id} push " \
                       f"{openlite_model_path}/bolt_64_fp32/{net}_f32.bolt {phone_bolt_path}/models/ "
        else:
            push_cmd = None
            print("Error:invalid models type")
        push_res = subprocess.getstatusoutput(push_cmd)
        if push_res[0] == 0:
            logger.info("PUSH Model {} SUCCESS".format(net))
        # 推送后开始测试
        # BOLT仅支持线程1，只跑线程1的数据
        bolt_model = net + "_f32" if self.data_type == "float32" else net + "_f16"
        benchmark_cmd = f"cd {phone_bolt_path};export LD_LIBRARY_PATH=./libs;chmod 777 benchmark;" \
                        f"./benchmark -M=./models/{bolt_model}.bolt -N={loop_time}"
        output = subprocess.getstatusoutput(f"adb -s {self.device_id} shell '{benchmark_cmd}'")[1]
        self.wait_device_found(output)
        logger.info(output)
        try:
            init_list = []
            # 先获取runtime，如果runtime获取成功再获取Init，否则直接判定用例失败
            p = re.findall("run_time_max.*", output)[0]
            aa = p.split("=")
            per_info_num_list = [re.findall(r"\d+\.?\d*", str_.strip("")) for str_ in aa]
            run_time_max, run_time_min, run_time_avg = per_info_num_list[1], per_info_num_list[2], per_info_num_list[3]
            init_runtime = 5
            for runtime in range(init_runtime):
                # 获取初始化值
                run_init_cmd = f"cd {phone_bolt_path};export LD_LIBRARY_PATH=./libs;timeout 5 " \
                               f"./benchmark -M=./models/{bolt_model}.bolt -N=1"
                res = subprocess.getstatusoutput(f"adb -s {self.device_id} shell '{run_init_cmd}'")[1]
                try:
                    per = re.findall("init_session_time is.*", res)
                    init_time = per[0].split("is ")[-1]
                    init_list.append(float(init_time))
                except Exception as e:
                    logger.error("Error while runtime is {}".format(runtime))
                    logger.error(e)
                    init_list = [0, 0, 0, 0, 0]
            # 将runtime和初始化平均值放入结果列表
            init_time_max, init_time_min = max(init_list), min(init_list)
            init_avg = mean(init_list)
            logger.info(
                "init time max:{};init time min:{},init time avg:{}".format(init_time_max, init_time_min, init_avg))
            per_info_lists.append([init_avg, run_time_max,
                                   run_time_min, run_time_avg, init_time_max, init_time_min])
        except IndexError as e:  # pylint: disable=invalid-name
            logger.error(
                "{} model run fail, result failed to obtain the value!!! fail output value: {}".format(
                    net,
                    e))
            per_info_lists.append([0, 0, 0, 0, 0, 0])
        logger.info("model-{}:{}".format(net, per_info_lists))
        for i in range(2):
            unused_thread = 2 * (i + 1)
            logger.info("bolt Thread {}".format(unused_thread))
            per_info_lists.append([0, 0, 0, 0, 0, 0])
        return per_info_lists

    @staticmethod
    def wait_device_found(output):
        if "device" in output and "not found" in output:
            sleep_time = 60
            logger.error("手机被跑shutdown，等待手机重新开机。")
            while sleep_time >= 0:
                logger.info("启动手机倒计时:{}".format(sleep_time))
                time.sleep(1)
                sleep_time -= 1
        else:
            pass


# pylint: disable=too-many-locals
def run_test(Test_Framework, backend_, data_types, if_official_=True, device_type="", model_list=None):
    """
    该方法用于执行批量模型更新
    :param Test_Framework:更新框架【MNN/TFLITE...】
    :param backend_:跑测后端【CPU/GPU/NPU】
    :param data_types:【FP16/32】
    :param if_official_:跑测商用or开源
    :param device_type:跑测设备
    :param model_list:跑测模型范围，该参数用于更新新增模型
    :return:
    """
    if model_list is None:
        model_list = []
    start_time = time.time()
    collection_name = "AI_Predict_Master" if if_official_ else "AI_Predict_Official"
    db_operation = mongo.DBOperation(Test_Framework, collection_name, mongo_env="cloud")
    if Test_Framework == "MNN":
        _id = "MNN_Do_TD_V100R002CMASTER" if if_official_ else "MNN_OpenLite_CMASTER"
    elif Test_Framework == "TFLITE":
        _id = "TensorFlow_Do_TD_V100R002CMASTER" if if_official_ else "TensorFlow_OpenLite_CMASTER"
    elif Test_Framework == "BOLT":
        _id = "BOLT_Do_TD_V100R002CMASTER" if if_official_ else "BOLT_OpenLite_CMASTER"
    else:
        print("not support Test Framework")
        sys.exit()
    if device_type == "X86":
        _id = _id + f"_{device_type}"
    elif data_types == "float32" and backend_ == "CPU":
        _id = _id + f"_{device_type}"
    elif data_types == "float32" and backend_ != "CPU":
        if backend_ == "GPU":
            _id = _id + f"_{device_type}_GPU_CL"
        else:
            _id = _id + f"_{device_type}_{backend_}"
    elif data_types == "float16":
        if backend_ == "GPU":
            _id = _id + f"_{device_type}_GPU_CL_FP16"
        else:
            _id = _id + f"_{device_type}_{backend_}_FP16"
    original_json = db_operation.get_original_json(_id)
    # 对更新前版本的数据做备份
    local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    if not os.path.exists(f"../history_json/{_id}_{local_date}"):
        os.makedirs("history_json")
        fp = open(f"./history_json/{_id}_{local_date}", "w")
        fp.write(json.dumps(original_json))
    device_id = Terminal_Device[device_type][0]
    print("update id:", _id)
    print("test device:", device_type)
    SingleTest = SingleModelTest(device_id, data_types, backend_, if_official_)
    # 商用交付模型流程
    # pylint: disable=len-as-condition
    run_model_list = original_json["NetTestResult"].keys() if len(model_list) == 0 else model_list
    if if_official_:
        for model in run_model_list:
            if backend_ == "GPU":
                if model not in GpuSupportModels:
                    logger.info("GPU Not support models{}".format(model))
                    continue
            elif backend_ == "NPU":
                if model not in NpuSupportModels:
                    continue
            logger.info("test model:{}".format(model))
            if Test_Framework == "MNN":
                if device_type == "X86":
                    res_list = SingleTest.run_mnn_x86(net=model)
                else:
                    res_list = SingleTest.run_mnn_benchmark(net=model)
            elif Test_Framework == "TFLITE":
                res_list = SingleTest.run_tflite_benchmark(net=model)
            elif Test_Framework == "BOLT":
                res_list = SingleTest.run_bolt_benchmark(net=model)
            else:
                print("not support Test Framework")
                sys.exit()
            db_operation.update_db_official(ori_list=res_list, net=model, _id=_id)
    # 开源模型流程
    else:
        for type_ in ["tflite", "caffe", "onnx"]:
            for model in original_json["NetTestResult"][type_].keys():
                logger.info("test model:{}".format(model))
                if Test_Framework == "MNN":
                    if device_type == "X86":
                        res_list = SingleTest.run_mnn_x86(net=model)
                    else:
                        res_list = SingleTest.run_mnn_benchmark(net=model)
                elif Test_Framework == "TFLITE":
                    res_list = SingleTest.run_tflite_benchmark(net=model)
                elif Test_Framework == "BOLT":
                    res_list = SingleTest.run_bolt_benchmark(net=model)
                else:
                    print("not support Test Framework")
                    sys.exit()
                db_operation.update_db_openlite(ori_list=res_list, net=model, _id=_id, net_type=type_)
    end_time = time.time()
    test_time = end_time - start_time
    print(f"test info:{_id},test Time is {test_time}")


def add_new_model(Test_Framework, backend_, data_types, device_type, current_id="MindSpore_OpenLite_20211216",
                  if_official_=True):
    """
    模型仓新增模型时，筛选出新增模型更新数据库
    Test_Framework:更新的框架[MNN.TFLITE.TNN.BOLT]
    data_types:float16/float32
    current_id:每日构建网络的id
    """
    # 交付模型目录
    ori_json = runtime_json
    collection_name = "AI_Predict_Master" if if_official_ else "AI_Predict_Official"
    db_operation = mongo.DBOperation(Test_Framework, collection_name, mongo_env="cloud")
    if Test_Framework == "MNN":
        _id = "MNN_Do_TD_V100R002CMASTER" if if_official_ else "MNN_OpenLite_CMASTER"
        net_type = "mnn"
        official_model_path = MnnOfficialModel
    elif Test_Framework == "TFLITE":
        _id = "TensorFlow_Do_TD_V100R002CMASTER" if if_official_ else "TensorFlow_OpenLite_CMASTER"
        net_type = "tflite"
        official_model_path = TfliteOpenLiteModel
    elif Test_Framework == "BOLT":
        _id = "BOLT_Do_TD_V100R002CMASTER" if if_official_ else "BOLT_OpenLite_CMASTER"
        net_type = "bolt"
        official_model_path = BoltOpenLiteModel
    else:
        print("not support Test Framework")
        sys.exit()
    official_models = os.listdir(official_model_path)
    if device_type == "X86":
        _id = _id + f"_{device_type}"
    elif data_types == "float32" and backend_ == "CPU":
        _id = _id + f"_{device_type}"
    elif data_types == "float32" and backend_ != "CPU":
        if backend_ == "GPU":
            _id = _id + f"_{device_type}_GPU_CL"
        else:
            _id = _id + f"_{device_type}_{backend_}"
    elif data_types == "float16":
        if backend_ == "GPU":
            _id = _id + f"_{device_type}_GPU_CL_FP16"
        else:
            _id = _id + f"_{device_type}_{backend_}_FP16"
    print("update id:", _id)
    print("test device:", device_type)
    original_json = db_operation.get_original_json(_id)
    json_models = []
    add_models = []
    for net in original_json["NetTestResult"].keys():
        json_models.append(f"{net}.{net_type}")
    # print(json_models)
    for model in official_models:
        if model not in json_models:
            model_size = os.stat(f"{official_model_path}/{model}").st_size
            print(f"Model:{model} Size:{model_size}")
            add_models.append([model.split(".")[0], model_size])
            print("新增模型列表：", add_models)
            ori_json["ModelSize"] = model_size
    # 更新新增模型的字段至数据库，方便连跑
    for model_info in add_models:
        db_operation.update_NewModel_official(model_info, _id)
    MScollection = mongo.DBOperation("MindSpore", "AI_Predict_OpenLite", mongo_env="cloud")
    Current_Json = MScollection.get_original_json(current_id)
    # 更新每日构建的支持网络json，否则前端无法展示数据
    for net in add_models:
        net_name = net[0]
        if net_name not in Current_Json[Test_Framework]["support_net"]:
            Current_Json[Test_Framework]["support_net"].append(net_name)
    # print(Current_Json["MNN"]["support_net"])
    res = MScollection.collection_handle().update_one(
        {"_id": current_id},
        {"$set": {Test_Framework: Current_Json[Test_Framework]}})
    print("Success:新增模型数据库Json初始化完成", res)
    # 开始跑测新增模型，更新时延数据
    model_lists = [info[0] for info in add_models]
    run_test(Test_Framework, backend_, data_types, if_official_=True, device_type=device_type, model_list=model_lists)


def process_run(process_list):
    for single_process in process_list:
        process_start = [p.start() for p in single_process]
        process_end = [p.join() for p in single_process]
        # 每轮流水线跑完建议让手机歇会
        time.sleep(60)
        logger.info("process_start:{}process_end:{}".format(process_start, process_end))


class FullTest:
    def __init__(self, Test_Framework, device_types, if_official):
        self.Test_Framework = Test_Framework
        self.device_types = device_types
        self.if_official = if_official

    def benchmark_run_all(self):
        device_types = ["Mate40", "Mate40pro", "P40"] if self.device_types == "all" else [self.device_types]
        for device_type in device_types:
            self.try_run(device_type)
        if self.Test_Framework == "MNN":
            # """===============跑测MNN==============="""
            # 并行跑测商用模型
            Process_x86 = [Process(target=run_test, args=("MNN", "CPU", "float32", self.if_official, device)) for device
                           in
                           ["X86"]]
            Process_cpu16 = [Process(target=run_test, args=("MNN", "CPU", "float16", self.if_official, device)) for
                             device in
                             device_types]
            Process_cpu32 = [Process(target=run_test, args=("MNN", "CPU", "float32", self.if_official, device)) for
                             device in
                             device_types]
            Process_gpu16 = [Process(target=run_test, args=("MNN", "GPU", "float16", self.if_official, device)) for
                             device in
                             device_types]
            Process_gpu32 = [Process(target=run_test, args=("MNN", "GPU", "float32", self.if_official, device)) for
                             device in
                             device_types]
            Process_npu32 = [Process(target=run_test, args=("MNN", "NPU", "float32", self.if_official, device)) for
                             device in
                             device_types]
            # 将所有进程队列放入到任务队列中，按队列顺序多机型并行跑侧
            ARM_process = [Process_cpu16, Process_cpu32, Process_gpu16, Process_gpu32, Process_npu32]
            X86_process = [Process_x86]
            process_run(ARM_process)
            process_run(X86_process)
        elif self.Test_Framework == "TFLITE":
            # """===============跑测TFLITE==============="""
            TFLITE_Process_cpu32 = [
                Process(target=run_test, args=("TFLITE", "CPU", "float32", self.if_official, device)) for
                device in device_types]
            TFLITE_Process_gpu32 = [
                Process(target=run_test, args=("TFLITE", "GPU", "float32", self.if_official, device)) for
                device in device_types]
            TFLITE_Process_gpu16 = [
                Process(target=run_test, args=("TFLITE", "GPU", "float16", self.if_official, device)) for
                device in device_types]
            processS = [TFLITE_Process_cpu32, TFLITE_Process_gpu32, TFLITE_Process_gpu16]
            process_run(processS)
        elif self.Test_Framework == "BOLT":
            # """===============跑测BOLT==============="""
            BOLT_Process_cpu32 = [Process(target=run_test, args=("BOLT", "CPU", "float32", self.if_official, device))
                                  for
                                  device in device_types]
            BOLT_Process_cpu16 = [Process(target=run_test, args=("BOLT", "CPU", "float16", self.if_official, device))
                                  for
                                  device in device_types]
            processS = [BOLT_Process_cpu32, BOLT_Process_cpu16]
            process_run(processS)

    def update_add_models(self):
        device_types = ["Mate40", "Mate40pro", "P40"] if self.device_types == "all" else [self.device_types]
        Add_official_x86 = [Process(target=add_new_model, args=(self.Test_Framework, "CPU", "float32", device)) for
                            device in
                            ["X86"]]
        Add_official_cpu16 = [Process(target=add_new_model, args=(self.Test_Framework, "CPU", "float16", device)) for
                              device in
                              device_types]
        Add_official_cpu32 = [Process(target=add_new_model, args=(self.Test_Framework, "CPU", "float32", device)) for
                              device in
                              device_types]
        Add_official_gpu16 = [Process(target=add_new_model, args=(self.Test_Framework, "GPU", "float16", device)) for
                              device in
                              device_types]
        Add_official_gpu32 = [Process(target=add_new_model, args=(self.Test_Framework, "GPU", "float32", device)) for
                              device in
                              device_types]
        Add_official_npu32 = [Process(target=add_new_model, args=(self.Test_Framework, "NPU", "float32", device)) for
                              device in
                              device_types]
        processS = [Add_official_cpu16, Add_official_gpu16, Add_official_gpu32, Add_official_cpu32, Add_official_x86,
                    Add_official_npu32]
        process_run(processS)

    def try_run(self, device_type):
        """
        实际启动连跑会实时更新数据库，该方法用于测试连跑环境配置等是否正常，不更新数据库信息
        """
        device_id = Terminal_Device[device_type][0]
        SingleTest = SingleModelTest(device_id, data_type="float32", backend="CPU", if_official=self.if_official)
        # 商用交付模型流程
        run_model_list = GpuSupportModels
        if self.if_official:
            success_num = 0
            for model in run_model_list:
                logger.info("test model:{}".format(model))
                if self.Test_Framework == "MNN":
                    res_list = SingleTest.run_mnn_benchmark(net=model)
                elif self.Test_Framework == "TFLITE":
                    res_list = SingleTest.run_tflite_benchmark(net=model)
                elif self.Test_Framework == "BOLT":
                    res_list = SingleTest.run_bolt_benchmark(net=model)
                else:
                    print("not support Test Framework")
                    sys.exit()
                if res_list != [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]:
                    success_num += 1
                    print(success_num)
                if success_num >= 3:
                    print("--------测试正常------")
                    break
            if success_num == 0:
                print("----单模型测试异常 取消连跑")
                sys.exit()
        # 开源模型流程
        else:
            success_num = 0
            for model in OfficialTestModels:
                logger.info("test model:{}".format(model))
                if self.Test_Framework == "MNN":
                    res_list = SingleTest.run_mnn_benchmark(net=model)
                elif self.Test_Framework == "TFLITE":
                    res_list = SingleTest.run_tflite_benchmark(net=model)
                elif self.Test_Framework == "BOLT":
                    res_list = SingleTest.run_bolt_benchmark(net=model)
                else:
                    print("not support Test Framework")
                    sys.exit()
                print(res_list)
                if res_list != [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]:
                    success_num += 1
                if success_num >= 1:
                    print("--------测试正常------")
                    break
            if success_num == 0:
                print("----单模型测试异常 取消连跑")
                sys.exit()


if __name__ == '__main__':
    add_new_model(Test_Framework="MNN", backend_="CPU", data_types="float16", if_official_=True,
                  device_type="Mate40pro", current_id="MindSpore_OpenLite_20211213_newAPI")
