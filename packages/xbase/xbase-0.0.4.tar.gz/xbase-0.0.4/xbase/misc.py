def xget_current_file_dir_path():
    import os
    return os.path.split(os.path.realpath(__file__))[0]


# 目前只支持两种浏览器类型chrome用于本地开发、phantomjs用于线上部署
def xget_selenium_driver_path(browser_type='chrome'):
    # 自动判断当前运行平台的操作系统类型进行自适应识别
    import platform
    import os
    os_type = platform.system().lower()
    driver_type = 'chromerdriver' if browser_type == 'chrome' else 'phantomjs'

    def get(list):
        if len(list) == 0:
            return None
        path = os.path.sep.join(list) + '/bin/%s/%s' % (os_type, driver_type)
        if os.path.exists(path):
            return path
        else:
            list.pop()
            return get(list)

    prefix_path = xget_current_file_dir_path()
    list = prefix_path.split(os.path.sep)
    return get(list)
