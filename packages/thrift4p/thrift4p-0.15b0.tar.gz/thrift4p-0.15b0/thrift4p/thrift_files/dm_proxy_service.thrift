namespace java com.didapinche.thrift.dm.proxy.dm_proxy_service

struct CreditInfo{
    1: i16 score  // 信用得分，0~100
    2: i16 creditLevel // 信用评级,暂定0~10
}

struct DeviceCreditInfo{
    1: CreditInfo creditInfo;
    2: list<string> tags // 标签
}

struct PaymentCreditInfo{
    1: CreditInfo creditInfo;
    2: list<string> tags // 标签
}

struct UserCreditInfo{
    1: CreditInfo creditInfo;
    2: list<string> tags // 标签
}

struct DriverCreditInfo{
    1: CreditInfo creditInfo;
    2: list<string> tags // 标签
}

struct TaxiDriverCreditInfo{
    1: CreditInfo creditInfo;
    2: list<string> tags // 标签
}

struct OrderCreditInfo{
    1: CreditInfo creditInfo;
    2: list<string> tags // 标签
}

struct HexagonCreditInfo{
    1: CreditInfo creditInfo;
    2: list<string> tags // 标签
}

struct DeviceInfo{
	1: DeviceCreditInfo deviceCreditInfo 	//标签
	2: string deviceType       	//设备类型
	3: list<i32> relatedUsers  	//关联用户id列表
	4: i32 relatedUsersCount   	//关联用户的个数
	
}

service DMProxyService{
	
	//设备信用得分
	DeviceCreditInfo getDeviceCreditInfo(1:string imei, 2:string imsi, 3:string mac, 4:string idfa)
	
	//支付账号信用得分
	PaymentCreditInfo getPaymentAccountCreditInfo(1:optional string weixin, 2:optional string alipay)
	
	//提现信用得分
	PaymentCreditInfo getWithdrawRequestCreditInfo(1:i64 userId, 2:string withdrawRequestAccount, 3:string withdrawAccountType)
	
	//车牌号信用得分
	CreditInfo getCarnoCreditInfo(1:string carno)
	
	//手机号信用得分
	CreditInfo getPhoneCreditInfo(1:string accountId)
	
	//乘客信用得分
	UserCreditInfo getUserCreditInfo(1:i64 userId)
	
	//拼车车主信用得分
	DriverCreditInfo getDriverCreditInfo(1:i64 driverId)
	
	//出租车车主信用得分
	TaxiDriverCreditInfo getTaxiDriverCreditInfo(1:i64 driverId)
	
	//拼车订单信用得分
	OrderCreditInfo getRideCreditInfo(1:i64 rideId)
	
	//出租车订单信用得分
	OrderCreditInfo getTaxiRideCreditInfo(1:i64 rideId)
	
	//获取区域标签
	list<string> getLbsTags(1:string lbsType, 2:i32 cityId, 3:string lbsId)
	
	//设置区域标签
	bool setLbsTag(1:string lbsType, 2:i32 cityId, 3:string lbsId, 4:string tag)
	
	//删除区域标签
	bool unsetLbsTag(1:string lbsType, 2:i32 cityId, 3:string lbsId, 4:string tag)
	
	//获取设备信息
	DeviceInfo getSingleDeviceInfo(1:string deviceId)
	
	//设置设备标签
	bool setSingleDeviceTag(1:string deviceId, 2:string tag)
	
	//删除设备标签
	bool deleteSingleDeviceTag(1:string deviceId, 2:string tag)
	
}