# coding:utf8
"""

"""

MAKE_DIR_PART = """\
if [ ! -d  $Rpath ] ; then
     mkdir -p $Rpath
fi

"""

RSYNC_SCRIPT_PART = """\
if [ `ps -ef|grep "$yuming::$Rsync"|grep -v grep|wc -l` -eq 0 ];then
nohup rsync -avP --exclude=.[a-zA-Z0-9]* --chmod=ugo=rwx --password-file=/etc/rsyncd.down --port=19873  $yuming::$Rsync $Rpath &
fi

"""