namespace java com.didapinche.thrift.api

// 短信通道
struct Channel {
    1:i64 productId
    2:string name
    3:string app
    4:string category
}

// 发送历史
struct SendHistory {
    1:string phone
    2:string content
    3:string sendTime
}

// 通道余额
struct ChannelBalance {
    1:i64 productId
    2:double balance
}

// 变量短信item
// phone 单个手机号
// args 一条短信的变量值，按顺序排列
struct TplItem {
    1:string phone
    2:list<string> params
}

service SMSService {
    // 批量发送短信
    // productId: 短信通道 eg：1,点点客拼车行业通道，9，梦网拼车营销通道
    // phone: 接收手机号 单个
    // content: 短信内容
    void singleSend(1:i64 productId, 2:string phone, 3:string content)

    // 批量发送短信
    // productId: 短信通道 eg：1,点点客拼车行业通道，9，梦网拼车营销通道
    // phone: 接收手机号 支持多个，用英文逗号分开
    // content: 短信内容
    void batchSend(1:i64 productId, 2:string phone, 3:string content)

    // 模板短信/变量短信发送
    void tplSend(1:i64 productId, 2:list<TplItem> params, 3:string content)

    // 获取渠道账户余额
    ChannelBalance getChannelBalance(1:i64 productId)

    // 渠道列表
    list<Channel> getChannelList(1:string app, 2:string category)

    // 查询发送历史
    list<SendHistory> getSendHistory(1:string phone, 2:string beginTime, 3:string endTime, 4:i32 pageNo, 5:i32 pageSize)
}
