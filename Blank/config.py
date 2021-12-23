# 机型配置信息
Terminal_Device = {
    "P40": ["NAB0220804063824", "arm64"],
    "Enjoyz": ["JDFNW20525001900", "arm64"],
    "Iqooz1": ["EYOBWSZ9U8AUU8QK", "arm64"],
    "Galaxys9": ["5158514554583398", "arm64"],
    "Galaxynote20": ["RFCN70JB9YW", "arm64"],
    "Mate40": ["XWN0220C15020042", "arm64"],
    "Mate40pro": ["PQYGY21130000022", "arm64"],
    "X86": ["x86", "x86"],
    "P50": ["FPP0221914016460", "arm64"]
}
runtime_json = {
    "RunTime": {
        "Thread_1": {
            "Init": "0",
            "Run": {
                "Min": "0",
                "Max": "0",
                "Avg": "0"
            }
        },
        "Thread_2": {
            "Init": "0",
            "Run": {
                "Min": "0",
                "Max": "0",
                "Avg": "0"
            }
        },
        "Thread_4": {
            "Init": "0",
            "Run": {
                "Min": "0",
                "Max": "0",
                "Avg": "0"
            }
        }
    },
    "RAM": {
        "Thread_1": 0,
        "Thread_2": 0,
        "Thread_4": 0
    },
    "ModelSize": 0
}
# 归档标杆模型的路径
MnnOfficialModel = "/home/thor/deploy_file/models/BENCHMARK/mnn_network"
MnnOpenLiteModel = "/home/thor/deploy_file/models/OFFICIAL/BENCHMARK/mnn_network"
TfliteOfficialModel = "/home/thor/deploy_file/models/BENCHMARK/tflite_network"
TfliteOpenLiteModel = "/home/thor/deploy_file/models/OFFICIAL/BENCHMARK/tflite_network"
BoltOfficialModel = "/home/thor/deploy_file/models/BENCHMARK/bolt_network"
BoltOpenLiteModel = "/home/thor/deploy_file/models/OFFICIAL/BENCHMARK/bolt_network"
OfficialTestModels = ["melgan_dr_1", "melgan_float16_1", "midas_v2_1_small_1_lite_1", "mirnet-fixed_dr_1",
                      "mirnet-fixed_fp16_1", "mirnet-fixed_integer_1", "mnasnet_050_224", "mnasnet_05_224",
                      "mnasnet_075_224", "mnasnet_10_128", "mnasnet_10_160", "mnasnet_10_192", "mnasnet_10_224",
                      "mnasnet_10_96", "mnasnet_13_224", "mobielnetv3-large_224", "mobilebert_1_default_1",
                      "mobilenet_v1_025_128_quant_frozen", "mobilenet_v1_025_128", "mobilenet_v1_025_160_quant_frozen",
                      "mobilenet_v1_025_160", "mobilenet_v1_025_192_quant_frozen", "mobilenet_v1_025_192",
                      "mobilenet_v1_025_224_quant_frozen", "mobilenet_v1_025_224", "mobilenet_v1_05_128_quant_frozen",
                      "mobilenet_v1_05_128", "mobilenet_v1_05_160_quant_frozen", "mobilenet_v1_05_160",
                      "mobilenet_v1_05_192_quant_frozen", "mobilenet_v1_05_192", "mobilenet_v1_05_224_quant_frozen"]
# NPU支持模型列表
NpuSupportModels = ["ml_video_edit_art_generate_20210513", "ml_video_edit_art_generate",
                    "ml_video_edit_art_transfer_20210513", "ml_video_edit_art_transfer", "ml_video_edit_detect",
                    "ml_video_edit_enhance_update", "ml_video_edit_generate_filter",
                    "ml_video_edit_generate_filter_pb2tflite", "ml_video_edit_hair_dyeing_migrate_v2",
                    "ml_video_edit_hair_dyeing_segmodel_v3",
                    "ml_video_edit_hairSeg_have_imageProcessLayer_interpTo145_updated_20210121",
                    "ml_video_edit_have_imageProcessLayer_interpTo145_20201015", "ml_video_edit_img_segment_adaptise",
                    "ml_video_edit_img_segment_adaptise_pb2tflite", "ml_video_edit_img_segment",
                    "ml_video_edit_imitate_filter", "ml_video_edit_judge", "ml_video_edit_makeup_mobilenetv203",
                    "ml_video_edit_MnetN367_extract_1010_pay", "ml_video_edit_oneclick_adaptis",
                    "ml_video_edit_person_divison_pic", "ml_video_edit_person_divison_video", "ml_video_edit_reid",
                    "ml_video_edit_style_transfer_autoportrait", "ml_video_edit_style_transfer_candy",
                    "ml_video_edit_style_transfer_gongnongbing", "ml_video_edit_style_transferl_starry",
                    "ml_video_edit_v10_best_model_nomean_20200723", "ml_video_edit_video_segment_gauss_adaptis_part1",
                    "ml_video_edit_video_segment_gauss_adaptis_part2",
                    "ml_video_edit_video_segment_gauss_adaptis_part2_pb2tflite", "ml_video_edit_vignet",
                    "hdc_contour_pose_128", "hdc_efficientnet_b3_1w_class", "hdc_emotion",
                    "hdc_Face_Aesthetic_MTI_Aesthetic", "hdc_Face_Emotion_MTI_Aesthetic",
                    "hdc_Face_Landmark5_MTI_Aesthetic", "hdc_fivembnet", "hdc_Image_Aesthetic_MTI_Aesthetic",
                    "hdc_isface", "hdc_mobilenet_1w_class", "hdc_mobilenetface", "hdc_ocr_attention", "hdc_ocr_detect",
                    "hdc_ocr_recog_202106", "hdc_resnet_1w_class", "hdc_resnet", "hdc_retinaface", "hdc_tb_cn_neg",
                    "ml_Heatmap_depth_180240", "ml_Heatmap_depth_240180", "ml_bodymask", "ml_ARengine23_bodypose",
                    "ml_hand_3d_detection", "ml_hand_3d_regression", "ml_Hand_deploy"]
# GPU支持模型列表
GpuSupportModels = ["Q888_model_normalize_object_scene_ps_20200826_f32_no_softmax", "Q888_HADB_AADB_MBV2_model_fp32",
                    "Q888_CV_face_emo_dress_mv3_orderd", "Q888_CV_model_face_dress_mv3y", "Q888_CV_model_age_gender",
                    "Q888_CV_model_face_emo_dress_mv3", "Q888_CV_face_dress_mv3y", "Q888_CV_age_gender_orderd",
                    "Q888_CV_face_recognition_self", "Q888_CV_face_recognition", "Q888_CV_labeldetect_multitask",
                    "Q888_CV_mbv2-object84.48-place70.9-activity82.4-FG85.5-softmax-small-test",
                    "Q888_CV_landmark_tflite", "Q888_CV_iris_detect", "Q888_CV_isface_caffemodel", "Q888_CV_pose_pb",
                    "Q888_CV_landmark_caffemodel", "Q888_CV_new_detect_tflite", "Q888_CV_pose_tflite",
                    "Q888_CV_new_detect_pb", "Q888_CV_isface_tflite", "Q888_CV_face_recognition_self",
                    "Q888_CV_lapa158_unet_0924_pb", "Q888_CV_lapa158_unet_0924_tflite", "Q_pose", "Q_isface",
                    "Q_new_detect", "Q_landmark", "Q_AADB_HADB_MBV2_model", "Q_hand_0812_pb2tflite", "Q_hand_0812",
                    "Q_convert", "Q_crnn_ori_75w_slim_norm_pb2tflite", "Q_crnn_ori_75w_slim_norm",
                    "Q_language_model_hrmini_Q4_b4_17w", "Q_detect_fpn_add_inception-1448650", "Q_focusocr_cn_recog",
                    "Q_focusocr_jk_recog", "Q_dila-small-mix-full-fineturn-390000-nopixel-nosigmoid_pb2tflite",
                    "Q_crnn_screen_slim400w_more_20w_pb2tflite",
                    "Q_dila-small-mix-full-fineturn-390000-nopixel-nosigmoid_tflite", "Q_crnn_screen_slim400w_more_20w",
                    "Q_dila-small-mix-full-fineturn-390000-nopixel-nosigmoid", "Q_face_recognition", "Q_object_scene",
                    "Q_iMaxSR_RGB_385_p", "Q_iMaxDN_RGB_385_p_RGB_RGB", "Q_crnn_ori_v2_405001_notrans_nopre",
                    "Q_crnn_ori_v2_405001_notrans_nopre_pb2tflite", "Q_inception-249970-672-11-16_pb2tflite",
                    "Q_inception-249970-672-11-16", "ml_location_lane_counter", "bolt_deploy_color-server",
                    "bolt_segment", "bolt_segment_pb2tflite", "bloom_hongmo_detection", "bloom_isface",
                    "bloom_landmark", "bloom_model_age_gender", "bloom_new_detect"]
