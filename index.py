""" 
腾讯云函数专用

由于云函数的入口一般都是 index.main_handler(),不同的云函数可能略微差异
如果在index文件中import多个模块,则这些模块都会执行;如果希望执行时间不同,那就需要新建不同的云函数,无法使用同一份jdCookie.py
采用timer触发器的附加信息Message进行传参,动态导入不同的模块,执行各自的run()方法
目的:
共用一份仓库文件,无需复制多份jdCookie.py
方便云函数调试
"""


def main_handler(event, context):
    for i in event['Message'].split("\r\n"):  # 定时器timer传参
        print(f"开始执行  {i}.py")
        tmp = __import__(i)
        tmp.run()  #该模块必须有run()接口;由于热启动的存在,重复import无效
        print("\n\n")
        print("###"*20)
        print("\n\n")

    return(event['Message'])


if __name__ == "__main__":  # 本地测试,模拟云函数定时触发器事件模板
    Message = ["test1","test2"]    # 此处修改,对应的模块名称
    """ 
    以下分割符("\r\n")与main_handler中的split("\r\n")保持一致;
    且创建定时触发器时多个需要换行,形如:
    1  test1
    2  test2
    ####################################
    * 如不换行,请将所有的 "\r\n" 改成 " " 
    """
    Message = ("\r\n").join(Message)
    # print(Message)

    # 以下无需修改
    event = {'Message': Message, 'Time': '2019-02-21T11:49:00Z',
             'TriggerName': 'EveryDay', 'Type': 'Timer'}
    context = {'memory_limit_in_mb': 128, 'time_limit_in_ms': 500000, 'request_id': 'abcdefg', 'environment': '{"SCF_NAMESPACE":"default"}', 'environ': 'xxxxxxxxxx',
               'function_version': '$LATEST', 'function_name': 'jd', 'namespace': 'default', 'tencentcloud_region': 'ap-beijing', 'tencentcloud_appid': '1111111111', 'tencentcloud_uin': '111111111'}

    main_handler(event, context)