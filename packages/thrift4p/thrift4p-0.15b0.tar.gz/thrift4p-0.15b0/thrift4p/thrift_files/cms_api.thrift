namespace java com.didapinche.cms.thrift

// meg：失败信息
struct Result{
    1:i32 code;
    2:string msg;
}

struct DeviceResult{
    1:i32 code;
    2:string user_ids;
}

struct BatchResult{
    1:i32 code;
    2:string msg;
    3:string batchId;
}

service CmsService {
   // 封禁用户，days：封禁天数
   Result forbiddenUser(1:i64 user_id, 2:string reason, 3:i64 sys_op_id, 4:string sys_op_ip, 5:i32 days);

   // 解封用户
   Result unforbiddenUser(1:i64 user_id, 2:string reason, 3:i64 sys_op_id, 4:string sys_op_ip);

   // 封禁车主（加入黑名单），days：封禁天数
   Result forbiddenDriver(1:i64 user_id, 2:string reason, 3:i64 sys_op_id, 4:string sys_op_ip, 5:i32 days);

   // 解封车主（移除黑名单），group_id：解封后的组别
   Result unforbiddenDriver(1:i64 user_id, 2:string reason, 3:i64 sys_op_id, 4:string sys_op_ip, 5:byte group_id);

   // 封禁设备，days：封禁天数
   DeviceResult forbiddenDevice(1:string device_id, 2:string reason, 3:i64 sys_op_id, 4:string sys_op_ip, 5:i32 days);

   // 解封设备
   DeviceResult unforbiddenDevice(1:string device_id, 2:string reason, 3:i64 sys_op_id, 4:string sys_op_ip);

   // 禁止发帖，days：封禁天数
   Result forbiddenPost(1:i64 user_id, 2:string reason, 3:i64 sys_op_id, 4:string sys_op_ip, 5:i32 days);

   // 解封发帖
   Result unforbiddenPost(1:i64 user_id, 2:string reason, 3:i64 sys_op_id, 4:string sys_op_ip);

   // 出租车订单挂起
   Result taxiOrderHold(1:i64 taxi_order_id, 2:string holdContent, 3:bool isSend, 4:i64 sys_op_id);

   // 出租车订单取消挂起
   Result taxiOrderCancelHold(1:i64 taxi_order_id, 2:string holdContent, 3:i64 sys_op_id);

   // 拼车订单挂起
   Result orderHold(1:i64 order_id, 2:string holdContent, 3:bool isSend, 4:i64 sys_op_id);

   // 拼车订单取消挂起
   Result orderCancelHold(1:i64 order_id, 2:string holdContent, 3:i64 sys_op_id);

   // 设置出租车订单标签
   Result taxiOrderSetTag(1:i64 order_id, 2:byte sys_order_group, 3:string reason, 4:i64 sys_op_id, 5:string sys_op_ip);

   // 删除单个回帖
   Result delReply(1:string replyId);

   // 批量删除回帖
   Result delReplyMulti(1:string replyIds);

   // 屏蔽单个回帖
   Result maskReply(1:string replyId, 2:byte mask);

   // 批量屏蔽回帖
   Result maskReplyMulti(1:string replyIds);

   // 封禁出租车车主（加入黑名单），days：封禁天数
   Result forbiddenTaxiDriver(1:i64 user_id, 2:string reason, 3:i64 sys_op_id, 4:string sys_op_ip, 5:i32 days);

   // 解封出租车车主（移除黑名单），group_id：解封后的组别
   Result unforbiddenTaxiDriver(1:i64 user_id, 2:string reason, 3:i64 sys_op_id, 4:string sys_op_ip, 5:byte group_id);

   // 封禁出租车用户，days：封禁天数
   Result forbiddenTaxiUser(1:i64 user_id, 2:string reason, 3:i64 sys_op_id, 4:string sys_op_ip, 5:i32 days);

   // 解封出租车用户
   Result unforbiddenTaxiUser(1:i64 user_id, 2:string reason, 3:i64 sys_op_id, 4:string sys_op_ip);

   // 设置拼车订单标签
   Result userOrderSetTag(1:i64 order_id, 2:byte sys_order_group, 3:string reason, 4:i64 sys_op_id, 5:string sys_op_ip);
   //生成批次号
   BatchResult createBatch(1:string source,2:string type,3:string awardTime);
   //插入打款详情
   BatchResult insertDetail(1:string batchId,2:string userId,3:string balance,4:string allOrderNum,5:string actualOrderNum,6:string cityId);
   //更新批次状态
   BatchResult closeBatch(1:string batchId);

   // 出租车设置标签加扣款类型
   Result taxiOrderSetTagAndDebit(1:i64 taxi_order_id, 2:string debitContent, 3:i64 sys_op_id, 4:i32 debitType, 5:string debitMoney);

}



