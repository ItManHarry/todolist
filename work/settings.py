'''
    系统配置
'''
import os
#开发数据库
dev_db = os.getenv('DEVELOP_DB')
#生产数据库
pro_db = os.getenv('PRODUCT_DB')
#系统路径
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
#全局配置
class GlobalSetting():
    SECRET_KEY = os.getenv('SECRET_KEY', '123456789qwertyuio!@#$')  #秘钥(session使用)
    BOOTSTRAP_SERVE_LOCAL = True                                    # Bootstrap本地化
#开发配置
class DevelopSetting(GlobalSetting):
    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DEVELOP_DATABASE_URL', dev_db)
#生产配置
class ProductSetting(GlobalSetting):
    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('PRODUCT_DATABASE_URL', pro_db)
#映射配置
config = {
    'dev_config': DevelopSetting,
    'pro_config': ProductSetting
}