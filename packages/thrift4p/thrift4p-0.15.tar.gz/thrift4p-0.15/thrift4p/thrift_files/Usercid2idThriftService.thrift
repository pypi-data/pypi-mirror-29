namespace java com.didapinche.usercid2id.thrift

struct Result {
  1: i32 code
  2: string msg
}

service Usercid2idThriftService {
    Result getUserId(1:string user_cid);
    Result getBatchUserId(1:string user_cids);
    Result getUserCid(1:string user_id);
    Result getBatchUserCid(1:string user_ids);
}