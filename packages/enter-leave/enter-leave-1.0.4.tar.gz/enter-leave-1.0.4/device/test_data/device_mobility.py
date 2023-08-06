# -*- coding: utf-8 -*-
from __future__ import unicode_literals


device_url = '/devices/api/device/'
device_operate_url = '/devices/api/device/{pk}/'
device_mobility_url = '/devices/api/device-mobility/'
device_mobility_operate_url = '/devices/api/device-mobility/{pk}/'
device_mobility_search_url = '/devices/api/device-mobility/?project_pk={pro_pk}'

post_method = 'post'
patch_method = 'patch'
delete_method = 'delete'
put_method = 'put'

delete_status_code = 204
created_status_code = 201

device_test_data = {"name": 'test', "code": 'test'}
device_post_data = {"name": 'test2', "code": 'test2'}
device_operate_data = {"name": 'test', "code": 'test'}
device_mobility_post_data = {
    "project": {'name': 'test', 'pk': '123456', 'code': 'TS-123', 'obj_type': 'T_TS'},
    "project_unit": {},
    "is_ground": True,                       # 进场为True 离场为False
    "images": 'test',                        # 设备照片
    "created_on":None,                       # 进场时间，自动获取当前时间
    "end_on" :None  
}

device_mobility_test_data = {
    "project": {                             # 项目
        'name': 'test',
        'pk': '123456',
        'code': 'TS-123',
        'obj_type': 'T_TS'
    },
    "project_unit": {                        # 单位工程
        "pk": "4836126201382",
        "code": "QH-V-01-01",
        "name": "test",
        "obj_type": "C_WP_UNIT"        
    },
    "construction_org": {                    # 施工单位
        "pk": "4835940668966",
        "code": "QH-V-01",
        "name": "test1",
        "obj_type": "C_PJ"
    },
    "construction_per": {                    # 施工单位负责人
        "pk": "4836126201382",
        "code": "QH-V-01-01",
        "name": "test1",
        "obj_type": "C_WP_UNIT"        
    },
    "supervising_org": {                     # 监理单位
        "pk": "4835940668966",
        "code": "QH-V-01",
        "name": "test1",
        "obj_type": "C_PJ"
    },
    "supervising_per": {                     # 监理单位负责人
        "pk": "4836126201382",
        "code": "QH-V-01-01",
        "name": "单位工程名称",
        "obj_type": "C_WP_UNIT"        
    },
    # "device_name": 1,                      # 设备名称
    "code": "设备code",                      # 设备code
    "number": 100,                           # 进场数量
    "original_value": 100000000,             # 原值
    "device_type": "设备类型",
    "device_spec": "规格型号", 
    "source": 1,                             # 设备来源  1自有 2租赁 3自带            
    "manufacturer": {                        # 厂商
        "pk": "4835940668966",
        "code": "QH-V-01",
        "name": "项目名称",
        "obj_type": "C_PJ"
    },
    "licence": {
        "number": "许可证号"
    },
    "certificate": {
        "number": "合格证号"
    },
    "attachments": 'test',                    # 附件 
    "remark": 'test',                         # 备注, 预留
    "is_ground": True,                        # 进场为True 离场为False
    "images": 'test',                         # 设备照片
    "created_on":None,                        # 进场时间，自动获取当前时间
    "end_on" :None                            # 离场时间，自动获取当前时间  
}