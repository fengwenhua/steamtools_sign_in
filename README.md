# steamtools_sign_in
steamtools - 青龙自动签到脚本（cookie)

## 使用
```shell
ql repo https://github.com/fengwenhua/steamtools_sign_in.git "steamtools.py" "" "sendNotify"
```

国内机器如下：

```shell
ql repo https://ghproxy.com/https://github.com/fengwenhua/steamtools_sign_in.git "steamtools.py" "" "sendNotify"
```

青龙面板新增环境变量: `STEAMTOOLS_COOKIE` 和 `STEAMTOOLS_USER`

cookie用于签到，username用于验证cookie是否失效

![image](https://github.com/fengwenhua/steamtools_sign_in/assets/26518808/8e679d8a-e57e-41ba-b809-5966190098c3)



值应该类似如下:

```
__51cke__=; ET8X_2132_saltkey=xxxx; ET8X_2132_lastvisit=1xxxxxxx; ET8X_2132_sid=axxxxx; ET8X_2132_sendmail=1; ET8X_2132_ulastactivity=1xxxxx; ET8X_2132_auth=2xxxxx; ET8X_2132_lastcheckfeed=7xxxx; ET8X_2132_lip=2xxxx; ET8X_2132_seccodecSUnh7oS=1xxx.xxx; ET8X_2132_st_p=1xxxxx; ET8X_2132_visitedfid=xxx; ET8X_2132_viewid=tid_xxxx; ET8X_2132_smile=1xxx; __tins__21247227=xxx; __51laig__=xx; ET8X_2132_lastact=xxxx%09misc.php%09patch
```
