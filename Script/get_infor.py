# Dịch ngược file apk sử dụng androguard
#
from androguard.misc import AnalyzeAPK
import os
from pathlib import Path
import pandas as pd
from androguard.core.analysis.analysis import dex


n = 0
df = pd.DataFrame(columns=["API call","permissions","intent"])

def apk_info_csv(apk):
  try:
    # apk_path = os.path.join(os.getcwd(), 'apk_test.apk')
    # phân tích APK
    # apk_path = os.path.join(os.getcwd(), apk)
    a, d, dx = AnalyzeAPK(apk)
    cg = dx.get_call_graph()

    ListPermission = set()
    # print("Danh sách quyền:")
    for permission in a.get_permissions():
        print(permission)
        ListPermission.add(permission)

    # method_dict = {}
    # for method in cg.nodes():
    #     cls_name = method.class_name[1:-1].lower()
    #     method_name = method.name.lower()
    #     if len(method_name) > 2 :
    #      if cls_name not in method_dict:
    #         method_dict[cls_name] = []
    #      method_dict[cls_name].append(method_name)
    # print(method_dict)

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
    # Tạo DataFrame từ danh sách này với tên cột là "key" và "value"
    # df1 = pd.DataFrame({"API call": [api_calls], "permissions": [ListPermission], "intent": [filter_list]})
    global df
    str_api = " ".join(x for x in list(api_calls))
    str_permiss = " ".join(x for x in list(ListPermission))
    str_filter = " ".join(x for x in list(filter_list))
    # df = df.append({"API call": [api_calls], "permissions": [ListPermission], "intent": [filter_list]})
    # df.update({"API call": [api_calls], "permissions": [ListPermission] ,"intent": [filter_list]})
    # df.loc[i] = [f"{api_calls}", f"{ListPermission}", f"{filter_list}"]
    global n
    df.loc[n] = [str_api, str_permiss, str_filter]
    # df.loc[n] = [api_calls,ListPermission,filter_list]
    n += 1
    # df["API call"] = [api_calls]
    # df["permissions"] = [ListPermission]
    # df["intent"] = [filter_list]
  except :
      return
if __name__ == '__main__':
 cnt = 0
 filenames = os.listdir('D:/KI 2 NAM 3/Python/BTL/Demo/Script/Filemalware')
 for filename in filenames :
    apk_info_csv(os.path.join('D:/KI 2 NAM 3/Python/BTL/Demo/Script/Filemalware',filename))
 df.to_csv("mal5_table.csv", index=False)  # Lưu thành tệp CSV