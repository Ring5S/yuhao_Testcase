from datetime import datetime, timedelta
def quick_schemas_data(static_phones, serial_no, id, serial_name):
    dateTime = datetime.now()
    utc_time = dateTime - timedelta(hours=8)  # UTC只是比北京时间提前了8个小时
    utc_time = utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")  # 转换成传参格式...
    Payload = {"quick_schema":
                   {"schema_name": "自动化营销回归{dateTime}".format(dateTime=dateTime),
                    "test_phones": "12345678987",
                    "periodic": 'false',
                    "deadline": utc_time,
                    "programs": [{"program_name": "节目1",
                                  "population": {"type": "mobile",
                                                 "referee_population": "normal",
                                                 "referee_template": 'null',
                                                 "sources": {"fixed": True,
                                                             "dynamic": False},
                                                 "static_member_nos": [],
                                                 "static_phones": [static_phones],
                                                 "labels": [],
                                                 "filters": {"limit": 0,
                                                             "order": 1,
                                                             "scopes": []}},
                                  "action": {"type": "coupon",
                                             "action_detail": {"type": "coupon",
                                                               "promotion": 'null',
                                                               "promotionItem": "",
                                                               "coupon": {
                                                                   "code": "{serialno}".format(serialno=serial_no),
                                                                   "label": "[{serialno}]{serial_name}".format(
                                                                       serialno=serial_no, serial_name=serial_name),
                                                                   "id": id},
                                                               "p_code": "",
                                                               "pi_code": "",
                                                               "serial_no": "{serialno}".format(serialno=serial_no),
                                                               "number": 1,
                                                               "no_repeat": False,
                                                               "no_repeat_type": "active",
                                                               "effective_days": 7}}}]}}
    print(dateTime)

