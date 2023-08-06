namespace java com.didapinche.thrift.dm.hub.holder

struct Result{
	1:i32 code,
	2:string msg
}

struct DeviceResult{
	1:i32 code,
	2:string userids
}

struct MultiPostResult{
	1:list<string> faildPostIds
}

service DmOperationHubService{
	void holdOrder(1:i64 OrderId,2:i32 sysOpId,3:string content)
	void cancelHoldOrder(1:i64 OrderId,2:i32 sysOpId,3:string content)
	Result holdTaxiOrder(1:i64 OrderId,2:i32 sysOpId,3:string content,4:bool isSend)
	Result cancelHoldTaxiOrder(1:i64 OrderId,2:i32 sysOpId,3:string content)
	Result forbiddenUser(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip,5:i32 days)
	Result unforbiddenUser(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip)
	Result forbiddenDriver(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip,5:i32 days)
	Result unforbiddenDriver(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip,5:byte group_id)
	DeviceResult forbiddenDevice(1:string deviceId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip,5:i32 days)
	DeviceResult unforbiddenDevice(1:string deviceId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip)
	Result forbiddenPost(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip,5:i32 days)
	Result unforbiddenPost(1:i64 userId,2:string reason,3:i64 sys_op_id,4:string sys_op_ip)
	Result taxiOrderSetTag(1:i64 taxi_order_id,2:byte group_id,3:string reason,4:i64 sys_op_id,5:string sys_op_ip)
	Result delPost(1:string postId)
	MultiPostResult delPostMulti(1:list<string> postIds)
	Result delUserAllPost(1:i64 userId)
	Result maskPost(1:string postId,2:byte mask,3:string comment,4:i64 sys_op_id,5:string sys_op_ip)
	MultiPostResult maskPostMulti(1:list<string> postId,2:byte mask,3:string comment,4:i64 sys_op_id,5:string sys_op_ip)
	Result maskUserAllPost(1:i64 userId,2:string comment,3:i64 sys_op_id,4:string sys_op_ip)
}
