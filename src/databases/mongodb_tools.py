"""
    Created by howie.hu at 2021-12-23.
    Description: 数据库基本操作函数合集
    Changelog: all notable changes to this file will be documented
"""


def mongodb_delete_many_data(coll_conn, filter_dict: dict) -> dict:
    """删除对应条件数据

    Args:
        coll_conn ([type]): 集合连接对象
        filter_dict (dict): 条件字典

    Returns:
        dict: 结果字典
    """
    db_result = {"status": True, "info": ""}
    try:
        coll_conn.delete_many(filter=filter_dict)
    except Exception as e:
        db_result["status"] = False
        db_result["info"] = e
    return db_result


def mongodb_find(
    coll_conn,
    filter_dict: dict,
    return_dict: dict = None,
    sorted_key: str = "",
    sorted_index: int = 1,
    limit: int = None,
) -> dict:
    """找到满足条件的所有记录

    Args:
        coll_conn ([type]): 集合连接对象
        filter_dict (dict): 条件字典
        return_dict (dict, optional): 返回条件字典
        sorted_key (str, optional): 排序的key
        sorted_index (int, optional): 1 正序，逐渐变大 -1 倒序 逐渐变小
        limit (int, optional): 返回查询数量

    Returns:
        dict: 结果字典
    """
    db_result = {"status": True, "info": ""}
    try:
        res = []
        if return_dict:
            cursor = coll_conn.find(filter_dict, return_dict)
        else:
            cursor = coll_conn.find(filter_dict)
        cursor = cursor.sort(sorted_key, sorted_index) if sorted_key else cursor
        cursor = cursor.limit(limit) if limit else cursor
        for document in cursor:
            res.append(document)
        db_result["info"] = res
    except Exception as e:
        db_result["status"] = False
        db_result["info"] = str(e)
    return db_result


def mongodb_update_data(
    coll_conn, filter_dict: dict, update_data: dict, upsert: bool = True
) -> dict:
    """更新数据到 mongodb

    Args:
        coll_conn ([type]): 集合连接对象
        filter_dict (dict): 条件字典
        update_data (dict): 更新数据 {"$set": {}}
        upsert (bool, optional): True 存在更新，不存在插入，False 只更新 Defaults to True.

    Returns:
        dict: 结果字典
    """
    db_result = {"status": True, "info": ""}
    try:
        coll_conn.update_one(filter=filter_dict, update=update_data, upsert=upsert)
    except Exception as e:
        db_result["status"] = False
        db_result["info"] = e
    return db_result


def mongodb_batch_operate(coll_conn, target_list: list) -> dict:
    """批量操作数据

    Args:
        coll_conn ([type]): 集合连接对象
        target_list (list): 目标操作对象列表

    Returns:
        dict: [description]
    """
    db_result = {"status": True, "info": ""}
    try:
        coll_conn.bulk_write(requests=target_list)
    except Exception as e:
        db_result["status"] = False
        db_result["info"] = e
    return db_result
