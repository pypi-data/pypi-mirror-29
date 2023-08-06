namespace java com.didapinche.thrift.bigdata.tags


struct User{
			1:i32 id, //user id
			2:string tagName, //标签名
			3:i16 weight //用户标签的权重
}

service UserTagsManageService {    	 
	
	 //添加数据
	 bool add(i32 id, string tagName, i16 weight)
	 //添加临时标签数据,ttl单位毫秒
	 bool addWithTTL(i32 id, string tagName, i16 weight, i64 ttl)
     //添加数据
	 bool addData(1:User data)
	 //批量插入
	 bool bulkData(1:list<User> data)
	 //批量插入临时标签数据,ttl单位毫秒
	 bool bulkDataWithTTL(1:list<User> data, i64 ttl)
	 //更新数据，支持批量更新
	 bool updateData(1:list<User> data)
	 //根据标签删除数据，支持批量删除
	 bool deleteDataByTagName(1:list<string> tags)
	 //根据用户id删除数据，支持批量删除
	 bool deleteDataByUserId(1:list<i32> users)
	 
	 //根据标签查询数据，支持分页，每页大小、第几页，flag=true分页；
	 //当flag=false时，默认返回前100以内的数据；
	 list<User> queryDataByTagName(1:string tag,2:i32 size,3:i32 page,bool flag)
	 //同时含有这几个标签的用户
	 binary queryDataByTagNames(1:list<string> tags)
	 //根据用户id查询数据
	 list<User> queryDataByUserId(1:list<i32> data)
	 //查询某个用户是否贴有某些标签
	 bool isOwnTag(1:i32 user_id ,2:list<string> tagName)
	 
	 //注册的标签总数目
	 i32 getTagsTotalNum()	 
	 //查询注册标签中含有的user id数目
	 map<string,i32> getTagsNum(1:list<string> tagNames)
	 
	 //注册新标签，标签名，属性(系统标签s、用户画像标签p、临时标签t)，支持批量添加
	 bool registerTag(map<string,string> tags)
	 //删除标签，支持批量删除，同时删除含有该标签的数据，
	 bool deleteTag(list<string> tags)
	 map<string,string> queryAllTags()

}
