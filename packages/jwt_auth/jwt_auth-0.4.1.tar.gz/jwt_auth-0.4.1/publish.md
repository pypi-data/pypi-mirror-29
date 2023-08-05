帮助页面参考

    https://packaging.python.org/tutorials/distributing-packages
注册你的账号：

    https://pypi.python.org/pypi?%3Aaction=register_form
构建目录结构，类似于

    https://github.com/pypa/sampleproject
编辑本地shell的配置文件

      [pypi]
        username： <username>
        password：<password>

编译
对wheel的配置
简单的情况，表达python2&3统统兼容。

        python setup.py bdist_wheel --universal
上传你的发布

        python setup.py register sdist upload