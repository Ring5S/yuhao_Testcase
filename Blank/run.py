from run_benchmark import FullTest

if __name__ == "__main__":
    Test_Framework = "TFLITE"
    device_types = "P50"
    if_official = True
    full_test = FullTest(Test_Framework, device_types, if_official)
    # full_test.try_run(device_types)
    full_test.benchmark_run_all()
