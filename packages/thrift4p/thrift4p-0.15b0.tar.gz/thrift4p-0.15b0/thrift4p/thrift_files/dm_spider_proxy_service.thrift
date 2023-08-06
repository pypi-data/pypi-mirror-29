namespace java com.didapinche.thrift.dm.proxy.dm_spider_proxy_service

service DMSpiderProxyService{

	# 把request写入到队列t_dm_spider_address_request
	bool sendAddressRequestToMq(1:string requestId, 2:double lon, 3:double lat)
	
	# (python)把结果发送到队列t_dm_spider_address_result
	bool sendAddressResultToMq(1:string key, 2:string tag, 3: string messageBody)
}