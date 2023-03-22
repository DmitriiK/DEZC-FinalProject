from enum import Enum
class JsonSchema:
    rootNode = 'realtyList'
    hepsiemlak_source_fields = ['id', 'age', 'price', 'createDate', 'updatedDate', 'mapLocation/lon', 'mapLocation/lat',
                            'city/id', 'city/name', 'county/id', 'county/name', 'district/id', 'district/name',
                            'sqm/netSqm',   'room/0', 'livingRoom/0', 'floor/count', 'floor/name', 'detailDescription'] # 'sqm/grossSqm/0',

    def flat_name(hierarchy_name):
        return hierarchy_name.replace('/', '_')


class GetParams:
    IsFurnished = 'furnishStatus=FURNISHED'
    NotIsFurnished = 'furnishStatus=UNFURNISHED'
    IsGazHeating = 'p10=101304-101305'
    NotIsGazHeating = 'p10=101303-101306'

    key_values = [
        {"paramName": 'furnishStatus', "columnName": 'IsFurnished', "paramValues"
        : [{"paramValue": 'UNFURNISHED', "storageValue": False}, {"paramValue": 'FURNISHED', "storageValue": True}]}
        ,
        {"paramName": 'p10', "columnName": 'IsGazHeating', "paramValues"
        : [{"paramValue": '101303-101306', "storageValue": False},
           {"paramValue": '101304-101305', "storageValue": True}]}
    ]


