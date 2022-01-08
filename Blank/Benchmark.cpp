/*
 * Copyright (c) Huawei Technologies Co., Ltd. 2018-2019. All rights reserved.
 * Description: mslite
 * Author: mslite
 * Create: 2019-11-04
 */
#include <sys/time.h>
#include <string.h>
#include <unistd.h>

#include <include/api/cell.h>
#include <include/api/model.h>
#include <include/api/data_type.h>
#include <include/api/serialization.h>
#include <include/api/context.h>
#include <include/api/types.h>
#include <assert.h>

#include <utils.h>
#include <benchmark.h>

#include <string>
#include <iostream>
#include <vector>

MSLiteBenchmarkRuner::~MSLiteBenchmarkRuner() {
    printf("~MSLiteBenchmarkRuner running");
}


MSLiteBenchmarkRuner::MSLiteBenchmarkRuner() {
    model_name = nullptr;
    printf("MSLiteBenchmarkRuner running");
}

void MSLiteBenchmarkRuner::ShowUsage() {
    std::cout << "Usage : " << std::endl;
    std::cout << "Option : " << std::endl;
    std::cout << "-M=         model name,such as -M=./models/mnet.ms,must be given" << std::endl;
    std::cout << "-N=         model train run time ,such as -N=1000 default is 100" << std::endl;
    std::cout << "-D=         model dataset dir path type,such as -D=/dataset/MNNIST,must be given" << std::endl;
    std::cout << "-H=         model run hardware,such as -H=CPU or NPU GPU default is CPU" << std::endl;
    std::cout << "-T=         model run thread,number,such as -T=1 or 2 or 4,default is 4" << std::endl;
    std::cout << "-B=         model run bind mode ,such as -B=NOBIND -B=MID or -B=HIGH, default is HIGH " << std::endl;
    std::cout << "-I=         model run input date ,such as -I=224 or -I='44;;;'" << std::endl;
    std::cout << "-S=         model run train if save model,default is 0" << std::endl;
    std::cout << "-V=         model run input shape from outside and default is null" << std::endl;
    std::cout << "-h=         print help info" << std::endl;
}

bool MSLiteBenchmarkRuner::ReadArgs(int argc, char *argv[]) {
    if (argc < 2) {
        std::cout << "The input para is wrong, please check" << std::endl;
        ShowUsage();
        exit(-1);
    }
    int index = 1;
    while (index < argc) {
        if (strncmp(argv[index], "-M=", 3) == 0) {
            model_name = &argv[index][3];
        } else if (strncmp(argv[index], "-N=", 3) == 0) {
            runtimes = std::stoi(&argv[index][3]);
        } else if (strncmp(argv[index], "-D=", 3) == 0) {
            data_type = &argv[index][3];
        } else if (strncmp(argv[index], "-F=", 3) == 0) {
            run_frequency = std::stoi(&argv[index][3]);
        } else if (strncmp(argv[index], "-T=", 3) == 0) {
            thread_num = std::stoi(&argv[index][3]);
        } else if (strncmp(argv[index], "-W=", 3) == 0) {
            warmup = std::stoi(&argv[index][3]);
        } else if (strncmp(argv[index], "-I=", 3) == 0) {
            input_data = &argv[index][3];
            std::cout << "input_data " << input_data << std::endl;
        } else if (strncmp(argv[index], "-B=", 3) == 0) {
            bind_mode = &argv[index][3];
        } else if (strncmp(argv[index], "-S=", 3) == 0) {
            shape = &argv[index][3];
            if (!strcmp(shape, "NULL")) {
                std::cout << "shape is not NULL" << std::endl;
            }
        } else if (strncmp(argv[index], "-H=", 3) == 0) {
            device = &argv[index][3];
        } else if (strncmp(argv[index], "-h", 2) == 0) {
            ShowUsage();
            return 0;
        } else {
            std::cout << "Option " << argv[index] << " is not valid" << std::endl;
        }
        index++;
    }
    return true;
}


bool MSLiteBenchmarkRuner::GenerateRandData(size_t size, void *data, mindspore::DataType data_type) {
    assert(data != nullptr);
    switch (data_type) {
        case mindspore::DataType::kNumberTypeFloat32:
            FillInputData<float>(size, data, std::uniform_real_distribution<float>(0.1f, 1.0f));
            break;
        case mindspore::DataType::kNumberTypeInt64:
            FillInputData<int64_t>(size, data, std::uniform_int_distribution<int64_t>(0, 1));
            break;
        case mindspore::DataType::kNumberTypeInt32:
            FillInputData<int32_t>(size, data, std::uniform_int_distribution<int32_t>(0, 1));
            break;
        case mindspore::DataType::kNumberTypeInt8:
            FillInputData<int8_t>(size, data, std::uniform_int_distribution<int8_t>(-127, 127));
            break;
        case mindspore::DataType::kNumberTypeUInt8:
            FillInputData<uint8_t>(size, data, std::uniform_int_distribution<uint8_t>(0, 254));
            break;
        default:
            char *casted_data = static_cast<char *>(data);
            for (size_t i = 0; i < size; i++) {
                casted_data[i] = static_cast<char>(i);
            }
    }
    return 0;
}

void MSLiteBenchmarkRuner::ConfigRuntime(const std::shared_ptr <mindspore::Context> &context) {
    context->SetThreadNum(thread_num);
    auto gpu_context = std::make_shared<mindspore::GPUDeviceInfo>();
    auto npu_context = std::make_shared<mindspore::KirinNPUDeviceInfo>();
    auto cpu_context = std::make_shared<mindspore::CPUDeviceInfo>();
    if (!strcmp(bind_mode.c_str(), "MID")) {
        auto core_list = setBindCpuMode("MID", thread_num);
        context->SetThreadAffinity(core_list);
    } else if (!strcmp(bind_mode.c_str(), "HIGH")) {
        auto core_list = setBindCpuMode("HIGH", thread_num);
        context->SetThreadAffinity(core_list);
    } else {
        auto core_list = setBindCpuMode("NOBIND", thread_num);
        context->SetThreadAffinity(core_list);
    }
    if (!strcmp(device.c_str(), "GPU")) {
        std::cout << "Run the session on GPU" << std::endl;
        context->MutableDeviceInfo().push_back(gpu_context);
        if (!strcmp(data_type.c_str(), "float16")) {
            gpu_context->SetEnableFP16(true);
        } else {
            gpu_context->SetEnableFP16(false);
        }
    }
    if (!strcmp(device.c_str(), "NPU")) {
        context->MutableDeviceInfo().push_back(npu_context);
        std::cout << "Run the session on NPU" << std::endl;
        npu_context->SetFrequency(run_frequency);
    }
    if (!strcmp(data_type.c_str(), "float16")) {
        context->MutableDeviceInfo().push_back(cpu_context);
        cpu_context->SetEnableFP16(true);
    } else {
        context->MutableDeviceInfo().push_back(cpu_context);
        cpu_context->SetEnableFP16(false);
    }
}

void MSLiteBenchmarkRuner::PrepareInputs(mindspore::Model &model, std::vector <mindspore::MSTensor> &msInputsTensors) {
    if (shape == nullptr) {
        msInputsTensors = model.GetInputs();
        for (auto tensor : msInputsTensors) {
            GenerateRandData(tensor.DataSize(), tensor.MutableData(), tensor.DataType());
        }
    } else {
        std::cout << "start to resize input" << std::endl;
        std::vector <std::vector<int64_t>> inputTensorDims;
        inputTensorDims = getInputShapeFromStrNew(shape);
        auto inputs = model.GetInputs();
        auto resize_ret = model.Resize(inputs, inputTensorDims);
        if (resize_ret.StatusCode() != mindspore::kSuccess) {
            std::cout << "The model Resize failed at runing, error is " << resize_ret.StatusCode() << std::endl;
            exit(-1);
        }
        msInputsTensors = model.GetInputs();
        // input data
        std::vector <std::string> input_data_vec = {};
        if (input_data != nullptr) {
            std::string input_data_str = input_data;
            std::string inputFlag = ";";
            input_data_vec = splitInput(input_data_str, inputFlag);
        }
        int flag = 0;
        for (auto tensor : msInputsTensors) {
            auto shapeSize = tensor.DataSize();
            auto inputData = tensor.MutableData();
            if (input_data != nullptr && input_data_vec[flag].length() != 0) {
                char *casted_data = static_cast<char *>(inputData);
                size_t size = shapeSize / 4;
                for (size_t i = 0; i < size; i++) {
                    casted_data[i] = static_cast<char>(stoi(input_data_vec[flag]));
                }
                flag += 1;
                continue;
            }
            GenerateRandData(tensor.DataSize(), tensor.MutableData(), tensor.DataType());
            flag += 1;
        }
    }
    msInputsTensors = model.GetInputs();
    for (auto &tensor : msInputsTensors) {
        if (tensor.DataType() == mindspore::DataType::kObjectTypeString) {
            std::string string_net_name = "string class net";
            auto *strtensors = mindspore::MSTensor::StringsToTensor(string_net_name, {"hello"});
            tensor = (*strtensors);
            mindspore::MSTensor::DestroyTensorPtr(strtensors);
        } else {
            GenerateRandData(tensor.DataSize(), tensor.MutableData(), tensor.DataType());
        }
        auto Mshape = tensor.Shape();
        if (Mshape[0] == 1 && Mshape[1] == 1 && Mshape[2] == 1 && Mshape[3] == 4) {
            auto data = reinterpret_cast<float *>(tensor.MutableData());
            if (data[0] > data[2]) {
                auto tmp = data[2];
                data[2] = data[0];
                data[0] = tmp;
            }
            if (data[0]-data[2] < 1e-5) {
                data[0] /= 2;
            }
            if (data[1] > data[3]) {
                auto tmp = data[3];
                data[3] = data[1];
                data[1] = tmp;
            }
            if (data[1]-data[3] < 1e-5) {
                data[1] /= 2;
            }
            for (auto i=0; i< 4; ++i) {
                std::cout << data[i] << ", ";
            }
            std::cout << std::endl;
        }
    }
}


// run benchmark
int MSLiteBenchmarkRuner::RunWithNewAPI() {
    size_t model_size = 0;
    float init_session_time;
    int loop;
    float sum = 0.0;
    float init_session_time_avg;
    // config context
    float array[5];
    mindspore::Model model;
    char *graph_buf = ReadFile(model_name, model_size);
    if (graph_buf == nullptr) {
        printf("Read model file failed while running %s", model_name);
        exit(-1);
    }
    for ( int a = 0; a < 5; a = a + 1 ) {
        uint64_t timeStartPrepare = getTimeInUs();
        auto context = std::make_shared<mindspore::Context>();
        ConfigRuntime(context);
        auto build_ret = model.Build(graph_buf, model_size, mindspore::ModelType::kMindIR, context);
        if (build_ret.StatusCode() != mindspore::kSuccess) {
            std::cout << "The model build failed at runing, error is " << build_ret.StatusCode() << std::endl;
            exit(-1);
        }
        uint64_t timeEndPrepare = getTimeInUs();
        float init_session_time_once = (timeEndPrepare - timeStartPrepare) / 1000.0;
        array[a] = init_session_time_once;
    }
    delete[] graph_buf;
    float init_session_time_min = array[0];
    for (loop = 1; loop < 5; loop++) {
      if ( init_session_time_min > array[loop] )
         init_session_time_min = array[loop];
    }
    float init_session_time_max = array[0];
    for (loop = 1; loop < 5; loop++) {
      if ( init_session_time_max < array[loop] )
         init_session_time_max = array[loop];
    }
    for (loop = 0; loop < 5; loop++) {
    sum += array[loop];
    init_session_time_avg = sum/5;
    }
    init_session_time = init_session_time_avg;
    std::cout << "init_session_time_min is: " << init_session_time_min << std::endl;
    std::cout << "init_session_time_max is: " << init_session_time_max << std::endl;
    std::cout << "init_session_time_avg is: " << init_session_time_avg << std::endl;
    std::cout << "start to prepare input" << std::endl;
    std::vector <mindspore::MSTensor> msInputsTensors;
    // prepare input
    PrepareInputs(model, msInputsTensors);
    std::vector <mindspore::MSTensor> msOutputsTensors;
    // warm up
    for (int i = 0; i < warmup; i++) {
        mindspore::Status warm_ret = model.Predict(msInputsTensors, &msOutputsTensors);
        if (warm_ret.StatusCode() != mindspore::kSuccess) {
            std::cout << "The model Predict failed at warmup, error is " << warm_ret.StatusCode() << std::endl;
            exit(-1);
        }
    }
    // test run
    std::vector<float> costs;
    for (int i = 0; i < runtimes; i++) {
        auto timeBeginRun = getTimeInUs();
        mindspore::Status loop_ret = model.Predict(msInputsTensors, &msOutputsTensors);
        if (loop_ret.StatusCode() != mindspore::kSuccess) {
            std::cout << "The model Predict failed at runing, error is " << loop_ret.StatusCode() << std::endl;
            exit(-1);
        }
        auto timeEndRun = getTimeInUs();
        costs.push_back((timeEndRun - timeBeginRun) / 1000.0);
    }
    printf("The input = %s and datatype = %s and thread_num = %d and runtimes = %d\n", model_name,
           data_type.c_str(), thread_num, runtimes);
    displayStats(model_name, costs, thread_num, init_session_time);
    return 0;
}

int MSLiteBenchmarkRuner::Main() {
    if (RunWithNewAPI()) {
        return 1;
    }
    return 0;
}
