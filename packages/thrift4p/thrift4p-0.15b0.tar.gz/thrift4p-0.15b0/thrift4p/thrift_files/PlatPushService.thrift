namespace java com.didapinche.push

enum PackageType{
    CAR = 1;
    TAXI = 2;
}

struct PushMessage {
    1: i16 pushType;
    2: PackageType packageType;
    3: map<string,string> params;
    4: optional string templateKey; // 同一个pushType对应不同模板时需要使用
}

struct UnRegisterUser{
    1:string pushSDK;
    2:string regId;
}

exception PushException {
    1: i32 code;
    2: string message;
}

service PlatPushService {
    void send(1:PushMessage msg,2:set<string> cids) throws (1:PushException e);
    void send2UnRegister(1:PushMessage msg,2:set<UnRegisterUser> regIds) throws (1:PushException e);
    // delay为延迟毫秒数
    void sendDelayMil(1:PushMessage msg,2:set<string> cids,3:i64 delay) throws (1:PushException e);
    // 延迟推送 delay的时间格式 yyyyMMddHHmmss
    void sendDelayDate(1:PushMessage msg,2:set<string> cids,3:string delay) throws (1:PushException e);
}