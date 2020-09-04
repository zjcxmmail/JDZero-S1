/**
 
【宠汪汪聚宝盆辅助脚本】
1、进入聚宝盆,显示 本轮 狗粮池 新增 投入总数,方便估算自己要投的数目
2、可能有两位数误差,影响不大

[MITM]
hostname = jdjoy.jd.com

surge
[Script]
聚宝盆投狗粮辅助 = type=http-response,pattern=^https://jdjoy\.jd\.com/pet/getPetTreasureBox,requires-body=1,max-size=0,script-path=https://raw.githubusercontent.com/Zero-S1/JD_tools/master/jbp.js

Qx
[rewrite_local]
^https://jdjoy\.jd\.com/pet/getPetTreasureBox url script-response-body https://raw.githubusercontent.com/Zero-S1/JD_tools/master/jbp.js

LOON：
[Script]
http-response ^https://jdjoy\.jd\.com/pet/getPetTreasureBox script-path=https://raw.githubusercontent.com/Zero-S1/JD_tools/master/jbp.js, requires-body=true, tag=聚宝盆投狗粮辅助

**/
let body = $response.body
body = JSON.parse(body)
food = body['data']['food']
var sum = 0
lastHourWinInfos = body["data"]["lastHourWinInfos"]
for (var i in lastHourWinInfos) {
    sum += lastHourWinInfos[i]["petCoin"]
}
lastTurnFood = parseInt(sum / 0.09 * 0.91)
body['data']['food'] = `${food} (${food - lastTurnFood})`
body = JSON.stringify(body)
$done({ body })
