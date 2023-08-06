本框架是一个service启动框架，适合一些分模块的定时任务

安装说明
  fdfs-client-py pip安装是2.X版本 无法正常在3.X运行 所以安装前需要先手工安装https://github.com/jefforeilly/fdfs_client-py.git

数据库默认支持PostgresSQL

使用说明
  启动方法
    import SDLCSService
    SDLCSService.ServiceManager.Main()

  各模块需要放在应用目录的ServiceMoudels目录 
     各模块单独文件夹以模块名命名 
     各模块的入口也是同样文件名.py
     入口文件里面的入口类也是同样的名字并继承于SDLCSService.Core.ServiceBase 

   
配置文件为应用目录Config.json

内容示例
{
    "ServiceModules":{
        "SDLCSUnit":{
            "loopTime":"5"
        }
    },
    "InterfaceModules": {
        "SDLCTester":{
        }
    },
    "options": {
        "fileSize": "2048",
        "filePath": "/data/",
        "port": "80",
        "debug":"True",
        "host":"0.0.0.0",
        "threadCount":"2",
        "IsPrintError":"True",
        "UnLimitedIP":["*"],
        "AsyncTheadCount":"4",
        "AsyncTimeOut":"20",
        "ExitPassword":"123456",
        "Database":{
            "serverip":"10.86.87.79",
            "port":"5432",
            "dbname":"postgres",
            "username":"postgres",
            "password":"postgres",
            "poolcount":"100",
            "isecho":"False"
        },
        "Logger":{
            "Level":"0",
            "IsPrint":"True",
            "SaveDay":"30"
        }
    }
}

