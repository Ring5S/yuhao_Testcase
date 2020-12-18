def search_app():
    import json, requests
    url = "http://jmp.joowing.com/rbj/api/wxopen/release"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    }
    release_version = input("要推送的小程序版本：")
    s_url = "http://jmp.joowing.com/rbj/api/wxopen/mini_programs.json?auth_status=1&page%5Bindex%5D=1&page%5Bsize%5D=1000&symbol=3"
    res = requests.get(s_url)
    # print(res.json())
    for info in res.json():
        org_code = info["org_code"]
        appid = info["authorization_appid"]
        plugins = info["plugins"]
        # print(plugins)
        data = {"release": {"authorization_appid": appid, "release_version": release_version}}
        if len(plugins) > 0:
            for plugins in plugins:
                if "nickname" in plugins.keys() and plugins["nickname"] == "小程序直播组件":
                    print(f"{org_code}该商户存在直播插件")
                    if_live = True
                    res1 = requests.post(url, data=data, headers=headers)
                    print(res1)
                else:
                    print(f"{org_code}该商户不存在直播插件")
                    if_live = False
                    data["release"]["release_version"] = f"{release_version}b"
                    res2 = requests.post(url, data=data, headers=headers)
                    print(res2)
        else:
            print(f"{org_code}该商户不存在直播插件")
            if_live = False
            data["release"]["release_version"] = f"{release_version}b"
            res2 = requests.post(url, data=data, headers=headers)
            print(res2)


search_app()
