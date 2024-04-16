# Dịch ngược file apk sử dụng androguard
#
from androguard.misc import AnalyzeAPK
import os
from pathlib import Path
import pandas as pd
from androguard.core.analysis.analysis import dex
from androguard.misc import dex

df = pd.DataFrame(columns=["API call","permissions","intent"])

def apk_info_csv(apk):
    # apk_path = os.path.join(os.getcwd(), 'apk_test.apk')
    # phân tích APK
    # apk_path = os.path.join(os.getcwd(), apk)
    a, d, dx = AnalyzeAPK(apk)
    
    ListPermission = set()
    # print("Danh sách quyền:")
    for permission in a.get_permissions():
        print(permission)
        ListPermission.add(permission)

    #lấy các API call
    api_calls = set()
    dx.get_external_classes()
    for x in dx.get_external_classes():
        for j in x.get_methods():
            if len(j.name) > 4 :
                api_calls.add(j.name)

    ## in các intent filter
    activities = a.get_activities()
    receivers = a.get_receivers()
    services = a.get_services()
    filter_list = set()

    for i in activities:
        filters = a.get_intent_filters("activity", i)
        if filters:
            for action in filters.values():
                for filter_item in action:
                    if isinstance(filter_item, (str, int)):  # Check if hashable (string or integer)
                        filter_list.add(filter_item)

    for i in receivers:
        filters = a.get_intent_filters("receiver", i)
        if filters:
            for action in filters.values():
                for filter_item in action:
                    if isinstance(filter_item, (str, int)):
                        filter_list.add(filter_item)

    for i in services:
        filters = a.get_intent_filters("service", i)
        if filters:
            for action in filters.values():
                for filter_item in action:
                    if isinstance(filter_item, (str, int)):
                        filter_list.add(filter_item)

    
    global df
    # df = df.append({"API call": [api_calls], "permissions": [ListPermission], "intent": [filter_list]})
    # df.update({"API call": [api_calls], "permissions": [ListPermission] ,"intent": [filter_list]})
    # df.loc[i] = [f"{api_calls}", f"{ListPermission}", f"{filter_list}"]
    df.loc[i] = [api_calls,ListPermission,filter_list]

    
if __name__ == '__main__':
 cnt = 0
 filenames = os.listdir('D:\KI 2 NAM 3\Python\BTL\Demo\Script\Fileapk')
 for filename in filenames :
    apk_info_csv(os.path.join('D:\KI 2 NAM 3\Python\BTL\Demo\Script\Fileapk',filename))
 df.to_csv("Begin_infor.csv", index=False)  # Lưu thành tệp CSV