# ES优化建议
## 调整indicies缓存
    indices.memory.index_buffer_size: 50%
## 更改新生代的大小（jvm.options）
    -XX:NewSize=8G
    -XX:MaxNewSize=8G #新老生代比例为1:1
## 设置模板更改分片数和更新频率    
