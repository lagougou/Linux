## mysql 二进制安装
 1. mysql-5.7.41(centos|redhat)  wget https://cdn.mysql.com//Downloads/MySQL-5.7/mysql-5.7.41-el7-x86_64.tar.gz
 2. tar xvf mysql-5.7.41-el7-x86_64.tar.gz -c /usr/local/mysql
 3. 准备mysql配置文件
  cat > mysql.cnf << EOF
    [client]

    #user=root
    #password=NthHTebo0c
    socket=/data/mysql/mysql.sock
    port=3306
    [mysql]
    prompt=(\\u@\\h) [\\d]>\\_
    [mysqld]
    datadir=/data/mysql
    socket=/data/mysql/mysql.sock
    port=3306
    #Disabling symbolic-links is recommended to prevent assorted security risks
    symbolic-links=0
    #Settings user and group are ignored when systemd is used.
    #If you need to run mysqld under a different user or group,
    #customize your systemd unit file for mariadb according to the
    #instructions in http://fedoraproject.org/wiki/Systemd
    innodb_buffer_pool_size=2G
    innodb_log_file_size=4G
    innodb_flush_log_at_trx_commit=1
    innodb_flush_method=O_DIRECT
    explicit_defaults_for_timestamp=1
    character_set_server=utf8
    slow_query_log=1
    long_query_time=5
    query_cache_type=1
    query_cache_size=32M
    max_allowed_packet=50M
    max_connections=10240
    max_connect_errors=100000
    open_files_limit=102400
    server-id=1
    log-bin=/data/mysql/mysql-bin
    [mysqld_safe]
    log-error=/data/mysql/log/mysql.log
    pid-file=/data/mysql/mysql.pid 
    EOF
 4. 创建mysql 用户 
     useradd -s /sbin/nologin mysql
 5. 更改base目录权限 
    chown -R mysql:mysql /usr/local/mysql
 6. 创建数据目录
    mkdir -p /data/mysql（必须为空）
 7. 初始化数据库
    /usr/loacal/mysql/bin/mysqld --initialize --user=root --basedir=/usr/local/mysql --datadir=/data/msyql
 8. 创建log目录及文件
    mkdir -p /data/mysql/log && touch /data/mysql/log/mysql.log
 9. 更改数据目录权限
     chown -R mysql:mysql /data/mysql
 10. 启动mysql服务 
    /usr/local/mysql/support-files/mysql.server start
 11. 登录数据库并修改初始密码
      mysql -uroot -p
      alter user root@'localhost' identified by 'password';
 
    

   
  
