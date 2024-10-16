"""入口文件"""
import sys

import brew


def get_app_rb_url(app_name):
    """获取 brew 软件 rb文件的url"""
    print(f"从 brew 查询 {app_name} 的信息")

    apps = brew.brew_info(app_name)
    if len(apps) == 0:
        raise Exception(f"没有找到软件：{app_name}")

    for app_type, url in apps:
        print(f"查到 {app_type}: {app_name}")

    # 大于1时，需要选择1个
    tip = f"请选择一个类型：{[t for t, _ in apps]}(首字母): "
    while len(apps) > 1:
        input_ = input(tip)
        for app_type, url in apps:
            if app_type.startswith(input_):
                return app_type, url
        tip = "请输入正确的首字母: "

    return apps[0]


def main():
    """入口函数"""

    if len(sys.argv) <= 1:
        app_name = input("请输入需要搜索的软件: ")
    else:
        app_name = sys.argv[1]

    try:
        app_type, url = get_app_rb_url(app_name)
    except Exception as ex:
        print(ex)
        exit(1)

    # todo 使用 token形式访问github 或者 浏览器的形式访问

    print(app_type, url)


main()
