| **版本** | **日期**     | **修改内容**                                 | **修改人** |
| ------ | ---------- | ---------------------------------------- | ------- |
| V1.0   | 12 月 23    |  初版定稿                                    | 杨倩&吉莉   |
| V2.0   | 2026/1/9   | 插入精简工作项                                  | 吉莉      |
| V2.1   | 2026/1/21  | 修改冷启动自检                                  | 吉莉      |
| V2.2   | 2026/02/04 | 若未配对，建图前会调用一次无感配对，RTK=1 时会正常退出，无未配对扫码兜底。 | 杨倩      |

# 需求背景



## 流程图

![](<images/【RTK 款】阴影出桩建图、工作（退两段）-diagram.png>)

## 建图时

### **建图自检**

[ 建图前自检](https://roborock.feishu.cn/wiki/ZxviwWau7iW4I4kXEFwcFkMenSh?from=from_copylink)

**<span style="color: rgb(216,57,49); background-color: rgba(255,246,122,0.8)">改动点说明：</span>**

<table><colgroup><col width="100"><col width="622"></colgroup>
<thead>
<tr>
<th>调整前</th>
<th><ul>
<li>仅有 RTK 为 4 时，才能自检通过</li>
</ul></th>
</tr>
</thead>
<tbody>
<tr>
<td>调整后</td>
<td><ul>
<li>冷启动、故障，不通过，让用户稍等后重试</li>
<li>RTK 为 <strong>0/1/2/4/5</strong> 时，自检通过，直接退</li>
</ul></td>
</tr>
</tbody>
</table>

<table><colgroup><col width="127"><col width="100"><col width="274"><col width="312"><col width="472"></colgroup>
<thead>
<tr>
<th><strong>阶段</strong></th>
<th><strong>条件</strong></th>
<th> RTK 信号情况</th>
<th>方案</th>
<th>备注</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="2"><strong>建图前自检</strong></td>
<td rowspan="2"><strong>首区</strong><br /><strong>非首区</strong><br /><strong>禁区</strong><br /><strong>通道</strong></td>
<td><ul>
<li>冷启动<strong>（开机后 120s/或进到 4结束）</strong></li>
<li>故障类</li>
</ul></td>
<td><strong>自检不通过，</strong>提示用户等待或检查后重试<br /></td>
<td>沿用原逻辑与App 弹窗提示<br /><a href="https://roborock.feishu.cn/wiki/ZxviwWau7iW4I4kXEFwcFkMenSh?from=from_copylink"> 建图前自检</a></td>
</tr>
<tr>
<td><ul>
<li><strong><span style="color: rgb(216,57,49); background-color: rgba(255,246,122,0.8)">RTK</span> <span style="color: rgb(216,57,49); background-color: rgba(255,246,122,0.8)">：0/1/2/4/5</span></strong></li>
</ul></td>
<td><strong>自检通过，进入下一步</strong></td>
<td>删除原自检中的「 RTK 不等于4」这一项</td>
</tr>
</tbody>
</table>

#### 工作项拆分：

* **【RTK状态机】**&#x81EA;检条件修改：`@刘正鹏`<span style="color: inherit; background-color: rgba(255,246,122,0.8)">——开发+联调 1天</span>

  * 冷启动状态计时：拉起RTK模块即开始计时，RTK=4或计时超过120s冷启动完成，退出冷启动状态。

  * RTK状态自检条件：0/1/2/4/5 均可自检通过，有串口失效Error或冷启动时自检不通过，上报对应错误码。

* **【状态机】**&#x81EA;检时RTK状态机上报F310，自检失败，向插件上报冷启动错误（非E38）

### 退桩

<table><colgroup><col width="100"><col width="622"></colgroup>
<thead>
<tr>
<th>调整前</th>
<th><ul>
<li>需要在退桩过程中，完成 SLAM 初始化。</li>
</ul></th>
</tr>
</thead>
<tbody>
<tr>
<td>调整后</td>
<td><ul>
<li>需要在退桩过程中，完成 SLAM 初始化，<strong><span style="color: rgb(216,57,49); background-color: rgba(255,246,122,0.8)">但未完成不报建图失败；</span></strong></li>
<li>如若在后退 1 米左右时（S0）未完成初始化，则继续后退（S1 ）。</li>
</ul></td>
</tr>
</tbody>
</table>

**交互策略**

<table><colgroup><col width="127"><col width="153"><col width="183"><col width="417"><col width="472"></colgroup>
<thead>
<tr>
<th><strong>阶段</strong></th>
<th><strong>条件</strong></th>
<th> 定位情况</th>
<th>方案</th>
<th>交互</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>退桩失败</strong></td>
<td colspan="2">除了信号外的其他异常退桩失败，提示不变</td>
<td> E42</td>
<td></td>
</tr>
<tr>
<td rowspan="5"><strong>退桩成功</strong><br /><br /></td>
<td><strong>S0 点</strong><br /><strong>SLAM 初始化成功</strong></td>
<td>/</td>
<td>引导用户去设置起点，开始建图（正常流程）</td>
<td>（正常流程）</td>
</tr>
<tr>
<td><strong>S0 点</strong><br /><strong>SLAM 初始化<span style="color: rgb(216,57,49); background-color: inherit">失败</span></strong></td>
<td>ALL </td>
<td><span style="color: rgb(216,57,49); background-color: rgba(255,246,122,0.8)">继续退桩至 S1 点</span><br /></td>
<td> App <strong>仍显示退桩界面，增加小机器人提示：</strong><blockquote>
<p><strong>提示：</strong>卫星信号弱，继续后退以获取定位，请注意避让。</p>
</blockquote></td>
</tr>
<tr>
<td><strong><span style="color: rgb(216,57,49); background-color: rgba(255,246,122,0.8)">S1 点</span></strong><br /><strong>SLAM 初始化成功</strong><br /></td>
<td>/<br /></td>
<td>引导用户去设置起点，但需要提醒用户该位置信号不好。<br />开始建图（正常流程）<br /></td>
<td><blockquote>
<p><del><strong>建图提醒</strong></del></p>
<p><del>该位置卫星信号不稳定，可能会影响机器人后续工作。</del></p>
<p><del>您可以选择继续建图，或结束建图、然后按说明书检查并调整 RTK 基站与充电站至合适位置后再重新建图。</del></p>
<p><del><strong>结束 / 继续建图</strong></del></p>
</blockquote></td>
</tr>
<tr>
<td rowspan="2"><strong><span style="color: rgb(216,57,49); background-color: rgba(255,246,122,0.8)">S1 点</span></strong><br /><strong>SLAM 初始化失败</strong><br /></td>
<td><ul>
<li>冷启动、故障</li>
</ul>（自检已检查过，不大可能有此状态）<br /></td>
<td><ul>
<li>建图失败</li>
</ul></td>
<td><strong>机器：</strong><ul>
<li><strong>「建图状态：故障暂停」</strong></li>
<li><strong>语音：</strong>定位异常，建图失败<strong>（<span style="color: rgb(216,57,49); background-color: rgba(255,246,122,0.8)">map_failed_position.wav</span>）</strong></li>
</ul><strong>App：</strong><ul>
<li>震动 + 小机器人弹窗<span style="color: rgb(216,57,49); background-color: inherit">（复用自检弹窗，自检已拦截，不大可能此时还有问题）</span>：</li>
</ul><blockquote>
<p><strong>定位系统启动中</strong></p>
<ol>
<li>如若您的机器人刚开机、或RTK 基站刚通电，定位系统正在恢复工作，<strong><span style="color: rgb(216,57,49); background-color: inherit">耐心等待约 3 分钟左右</span></strong>。</li>
<li>如果您已等待超过 3 分钟，可能是定位系统异常，请检查基站的信号灯是否正常（绿灯），如果不是，可以手动插拔电源后等待 3 分钟看信号是否可恢复。</li>
<li>如果问题仍然存在，请联系技术支持。</li>
</ol>
<p><span style="color: inherit; background-color: rgba(254,212,164,0.8)">Button：知道了</span></p>
</blockquote></td>
</tr>
<tr>
<td><ul>
<li>0/1/2/4/5</li>
</ul></td>
<td><ul>
<li>建图失败，如果退 2 次都没成功，也不支持。</li>
</ul></td>
<td><blockquote>
<p><strong>建图失败</strong></p>
<p>卫星信号弱，定位失败。</p>
<p><strong>请将机器人推回充电站后重试。</strong></p>
<p>若问题仍存在，请点击“仍未解决”按钮，按步骤排查。</p>
<p><strong><span style="color: inherit; background-color: rgba(254,212,164,0.8)">Button：仍未解决 / 退出</span></strong></p>
</blockquote><span style="color: inherit; background-color: rgb(251,191,188)">点击</span><strong><span style="color: inherit; background-color: rgb(251,191,188)">“仍未解决”</span></strong><br /><span style="color: rgb(216,57,49); background-color: rgba(255,246,122,0.8)">页面需增加返回上一步的逻辑</span><blockquote>
<p><strong>建图失败</strong></p>
<p>请按如下步骤排查：</p>
<ol>
<li>确保充电站附近无遮挡，避免靠墙或室内安装；</li>
<li>若机器人刚开机，定位系统可能正在恢复，请<strong>等待约 3 分钟</strong>后再重试；</li>
</ol>
<ol start="3">
<li>检查 RTK 基站指示灯是否为绿灯常亮：</li>
</ol>
<p>1）若不是，请插拔RTK基站电源并<strong>等待 3 分钟</strong>后再重试；</p>
<p>2）若仍未解决，且指示灯频繁异常，建议重新选址安装 RTK 基站，并重新建图。</p>
<p><strong><span style="color: inherit; background-color: rgba(254,212,164,0.8)">Button：仍未解决 / 退出</span></strong></p>
</blockquote><span style="color: inherit; background-color: rgb(251,191,188)">点击</span><strong><span style="color: inherit; background-color: rgb(251,191,188)">“下一步”</span></strong><blockquote>
<p><strong>建图失败</strong></p>
<p>请确认是否为首次使用机器人、或近期更换过 RTK 基站。如是，请重新扫码配对，并<strong><span style="color: rgb(216,57,49); background-color: inherit">等待约 3 分钟后</span></strong>再重试。</p>
<p><em>注意：重新配对后需重新建图。</em></p>
<p><strong><span style="color: inherit; background-color: rgba(254,212,164,0.8)">Button：扫码配对 / 退出</span></strong></p>
</blockquote></td>
</tr>
<tr>
<td rowspan="2"><strong>桩外启动建图</strong><br /><strong>非首个图</strong><br /><span style="color: rgb(46,161,33); background-color: inherit">（已完成）</span><br /></td>
<td>当前有定位</td>
<td>有定位，定位可用，不需要重定位</td>
<td>直接下一步建图</td>
<td>（正常流程）2 月已支持</td>
</tr>
<tr>
<td>当前没定位</td>
<td>定位不可用，信号 ALL</td>
<td>先重定位，若重定位失败，则提示放回充电桩重试。</td>
<td>2 月已支持</td>
</tr>
</tbody>
</table>

#### 工作项拆分：

![](<images/【RTK 款】阴影出桩建图、工作（退两段）-diagram-1.png>)

* **【状态机/APP\_PROXY】建图退桩** <span style="color: inherit; background-color: rgba(255,246,122,0.8)"> </span>`@梁彬欣`<span style="color: inherit; background-color: rgba(255,246,122,0.8)">1天开发+1-2天联调</span>

  输入：导航上报初始化成功/失败、二次退桩成功/失败

  插件下发结束/继续建图指令

  输出：上报给插件初始化成功/失败、二次退桩成功/失败

  根据指令切【建图状态：遥控前往起点】/【建图状态：故障暂停】/【无任务状态】



* **【导航】建图二次退桩`@李欢`<span style="color: inherit; background-color: rgba(255,246,122,0.8)">1周开发+3天联调</span>**

  S0点初始化失败后自动二次退桩（最大1m），期间收到初始化成功立即停止后退

  向状态机上报首次初始化结果、二次退桩结果

  二次退桩成功后做局部坐标系到世界坐标系的坐标转换



* **【定位】二次退桩局部定位`@李宝玉`&#x20;**

局部VSLAM定位

SLAM初始化成功后将VSLAM局部坐标发给导航



* **【插件】二次退桩过程中交互**（文案参照产品最新版）

  * 收到RTK器件相关错误码或冷启动F310后，退出启动页面，弹提示

  交互文案参考[ 建图前自检](https://roborock.feishu.cn/wiki/ZxviwWau7iW4I4kXEFwcFkMenSh#share-WCEYdvqdpoXb78xLZL7cr40RnRb)

  按钮OK，退回主页面

  * 收到退桩初始化失败F码后，页面显示退桩页面，与现有的退桩一致，弹提示

  > **提示：**&#x536B;星信号弱，继续后退以获取定位，请注意避让。    &#x20;

  * 定位成&#x529F;**：**&#x5F39;UI引导建图

坚持继续建图则进遥控建图，退出建图退回主页面；给APP\_PROXY发继续建图/退出建图。

* 定位失败： 震动 + 小机器人弹窗报建图失败&#x20;

退出后退回主页面。

## 工作时

### **任务启动自检**

**<span style="color: rgb(216,57,49); background-color: rgba(255,246,122,0.8)">RTK 信号部分-- 改动点：</span>**

<table><colgroup><col width="100"><col width="807"></colgroup>
<thead>
<tr>
<th>调整前</th>
<th><ul>
<li><strong>在桩/不在桩：</strong>仅有 RTK 为 4 时，才能自检通过，自检通过后会退桩</li>
</ul></th>
</tr>
</thead>
<tbody>
<tr>
<td>调整后</td>
<td><ul>
<li><strong>在桩 / 不在桩：自检发现冷启动、故障，先做恢复</strong></li>
</ul></td>
</tr>
</tbody>
</table>

### 启动前

**在启动时，如若 RTK 处于故障、冷启动中时，需要先恢复到正常情况后再启动。**

<table><colgroup><col width="132"><col width="175"><col width="361"><col width="372"></colgroup>
<thead>
<tr>
<th><strong>阶段</strong></th>
<th><strong>条件</strong></th>
<th> 说明</th>
<th>交互</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>启动时</strong></td>
<td><ul>
<li>RTK 故障、冷启动</li>
</ul></td>
<td><strong>机器：</strong><ul>
<li>在桩：恢复成功则<strong>退桩，同时 SLAM 初始化；</strong></li>
<li>不在桩：恢复成功则<strong>重定位</strong>；（没其他异常时）</li>
</ul>至多<span style="color: rgb(216,57,49); background-color: rgba(255,246,122,0.8)">3 分钟</span>，未恢复则需要上报 Error38<br /><strong>App：</strong><ul>
<li>提示用户正在启动</li>
</ul></td>
<td><strong>恢复前：</strong><ul>
<li>
<p>机器语音：定位中，请稍后（<strong><span style="color: rgb(216,57,49); background-color: rgba(255,246,122,0.8)">robot_location.wav）</span></strong></p>
</li>
<li>
<p>App 提示：</p>
<p>首页状态<strong>「启动中」</strong>，小机器人消息：</p>
<blockquote>
<p>定位系统正在启动，请稍后。</p>
</blockquote>
</li>
</ul>至多3 分钟，未恢复则需要上报 Error38</td>
</tr>
</tbody>
</table>

**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">如沟通，工作启动有变更：</span>**

**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">启动前冷启动改为自检不通过，提示稍后重试，同建图启动自检；</span>**

**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">计划启动按照可自恢复故障逻辑，冷启动时计划延迟，故障恢复后自动开始计划任务</span>**

#### 工作项拆分：

~~**【状态机】任务启动自检：`@刘正鹏`**~~

* ~~冷启动状态计时：拉起RTK模块即开始计时，RTK=4或计时超过120s冷启动完成，退出冷启动状态。~~

* ~~RTK状态自检条件：0/1/2/4/5 均可自检通过，有串口失效Error时自检不通过。~~

~~工作启动自检逻辑：~~

* ~~触发自检时冷启动未结束：~~

  * ~~先自检其他项，若自检通过则上报F310，延迟启动；~~

  * ~~语音【定位中，请稍后（**<span style="color: rgb(216,57,49); background-color: inherit">robot_location.wav）</span>**】；~~

  * ~~退出冷启动状态时解除F310，上报插件~~

* ~~触发自检时冷启动已结束：正常自检，上报自检通过/自检不通过(E38)。~~

修改后版本：

* **【RTK状态机】**&#x81EA;检条件修改：`@刘正鹏`<span style="color: inherit; background-color: rgba(255,246,122,0.8)">——开发+联调 1天</span>

  * 冷启动状态计时：拉起RTK模块即开始计时，RTK=4或计时超过120s冷启动完成，退出冷启动状态。

  * RTK状态自检条件：0/1/2/4/5 均可自检通过，有串口失效Error或冷启动时自检不通过。

  自检逻辑同建图启动：冷启动时自检失败返回F310，其他RTK故障保持一致自检失败返回对应错误码。

* **【状态机】区分手动启动和计划启动**

  * 手动启动：自检时若RTK状态机上报F310，自检失败，向插件上报冷启动错误（非E38）

  * 计划启动：自检时若RTK状态机上报F310，自检失败，向插件上报冷启动错误（非E38）。

    * 语音【定位中，请稍后（**<span style="color: rgb(216,57,49); background-color: inherit">robot_location.wav）</span>**】；

    * 作为可恢复故障，计划延迟，自检到F310清除后重新自检开始计划任务

* **【插件】**&#x6839;据状态机上报自检结果显示启动中文案

  * 同建图启动，收到RTK器件相关错误码或冷启动F310后，退出启动页面，弹提示

  交互文案参考[ 建图前自检](https://roborock.feishu.cn/wiki/ZxviwWau7iW4I4kXEFwcFkMenSh#share-WCEYdvqdpoXb78xLZL7cr40RnRb)  按钮OK，退回主页面



### **工作定位**

<table><colgroup><col width="165"><col width="246"><col width="433"><col width="407"></colgroup>
<thead>
<tr>
<th><strong>情况</strong></th>
<th>信号条件</th>
<th><strong>方案</strong></th>
<th>示意图</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>启动时，无论在桩还是不在桩</strong></td>
<td><ul>
<li>RTK 冷启动</li>
<li>RTK故障</li>
</ul></td>
<td><strong>在这种状态下，不自动退桩、或不重定位。</strong><br />等待至多 120s，上报 Error38</td>
<td>等待时，App 显示的是 “定位系统恢复中”<br />不显示机器人位置</td>
</tr>
<tr>
<td><strong>在桩启动</strong></td>
<td>RTK = 0/1/2/4/5</td>
<td><br />从S0开始直退至S1，期间若SLAM初始化成功原地掉头沿通道goto割草起点，若S1处仍未初始化成功，从S1处开始走一个口字型做重定位，重定位过程中：<ul>
<li>SLAM初始化成功：结束重定位，沿通道goto割草起点；</li>
<li>重定位失败：报Error38</li>
</ul></td>
<td><img src="images/%E3%80%90RTK%20%E6%AC%BE%E3%80%91%E9%98%B4%E5%BD%B1%E5%87%BA%E6%A1%A9%E5%BB%BA%E5%9B%BE%E3%80%81%E5%B7%A5%E4%BD%9C%EF%BC%88%E9%80%80%E4%B8%A4%E6%AE%B5%EF%BC%89-diagram-2.png" alt=""></td>
</tr>
<tr>
<td rowspan="5"><strong>桩外启动</strong><br />参见文档顶部流程图<img src="images/%E3%80%90RTK%20%E6%AC%BE%E3%80%91%E9%98%B4%E5%BD%B1%E5%87%BA%E6%A1%A9%E5%BB%BA%E5%9B%BE%E3%80%81%E5%B7%A5%E4%BD%9C%EF%BC%88%E9%80%80%E4%B8%A4%E6%AE%B5%EF%BC%89-image.png" alt=""></td>
<td><ul>
<li>RTK 冷启动</li>
<li>RTK故障</li>
</ul></td>
<td><strong>在这种状态下，不自动退桩、或不重定位。</strong><br />等待至多 3min，上报 Error38</td>
<td><ul>
<li>
<p>App 提示：</p>
<p>首页状态<strong>「启动中」</strong>，小机器人消息：</p>
<blockquote>
<p>定位系统正在启动，请稍后。</p>
</blockquote>
</li>
</ul>至多3 分钟，未恢复则需要上报 Error38</td>
</tr>
<tr>
<td><ul>
<li>启动前定位<strong>可用</strong></li>
</ul>（RTK =0/1/2/ 4/5 都可以）</td>
<td>使用之前可用的定位，开始工作<br /></td>
<td>正常流程（已实现）</td>
</tr>
<tr>
<td>同时满足：<ul>
<li>启动前定位<strong>不可用</strong>（启动前重定位失败、重启或搬运过）</li>
<li>非计划启动</li>
</ul>（RTK =0/1/2/ 4/5 都可以）</td>
<td>启动，口字重定位<br /></td>
<td>定位时，App 提示定位中</td>
</tr>
<tr>
<td>同时满足：<ul>
<li>启动前定位<strong>不可用</strong>（启动前重定位失败、重启或搬运过）</li>
<li>计划启动</li>
<li>RTK = 2/4/5</li>
</ul></td>
<td>启动，口字重定位<br /></td>
<td>定位时，App 提示定位中</td>
</tr>
<tr>
<td>同时满足：<ul>
<li>启动前定位<strong>不可用</strong>（启动前重定位失败、重启或搬运过）</li>
<li>计划启动</li>
<li>RTK =0/1</li>
</ul></td>
<td><strong><span style="color: rgb(216,57,49); background-color: rgba(255,246,122,0.8)">存在启动风险</span></strong>，不启动，报 Error 38<br /></td>
<td><strong>Error 38</strong></td>
</tr>
</tbody>
</table>

#### 工作项拆分：

![](<images/【RTK 款】阴影出桩建图、工作（退两段）-diagram-3.png>)

* **【导航】工作出桩重定位`@李欢`<span style="color: inherit; background-color: rgba(255,246,122,0.8)"> 同建图一起做，导航总计1周开发+3天联调</span>**

退桩到S0点后若未初始化完成继续退至S1点，初始化失败后执行重定位，重定位过程初始化成功后立即停止

重定位后做局部坐标系到世界坐标系的坐标转换

重定位失败上报E38

* **【状态机】桩外自启动项兜底<span style="color: rgb(100,37,208); background-color: inherit">：</span>`@梁彬欣`**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">开发+自测 1天</span>

  桩外计划启动，若无定位（上次任务结束时定位丢失），自检RTK= 0/1，不启动，取消该段割草计划，报Error38；

  其余情况正常启动，根据有定位/无定位分别直接启动/自检后启动。

## 总结更新后，报 Error 38  的条件：

<table><colgroup><col width="136"><col width="172"><col width="398"><col width="355"></colgroup>
<thead>
<tr>
<th><strong>阶段</strong></th>
<th> RTK 情况</th>
<th>方案</th>
<th>App交互补充</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>建图启动</strong></td>
<td>ALL</td>
<td>建图启动时，各类信号情况不报 Error 38</td>
<td> 参见上文</td>
</tr>
<tr>
<td rowspan="3"><strong>任务启动</strong><br />（机器人要 自己去做 GOTO，包括自动割草、回充等）<br /></td>
<td><ul>
<li>故障、冷启动</li>
</ul></td>
<td><strong>在这种状态下，不自动退桩、或不重定位。</strong><br />先上报 App “启动中”，先<strong>进行恢复、等待冷启动结束</strong>，超时<strong>未恢复上报 Error 38</strong></td>
<td><ul>
<li>在等待进到 0/1/2/4/5 时，上报App 显示的是 “启动中”</li>
</ul>--如果是手动启动，可能会直接报。</td>
</tr>
<tr>
<td rowspan="2"><ul>
<li>0/1/2/4/5</li>
</ul></td>
<td><ul>
<li>
<p><strong>在桩</strong></p>
<p>先退桩，根据上述情况退桩进行 SLAM 初始化、以及重定位，<strong>如果失败，报 Error 38</strong></p>
</li>
</ul></td>
<td><ul>
<li>在退出基站时，上报App 显示的是“退出基站中”</li>
<li>在定位时，上报App 显示的是“定位中”</li>
</ul></td>
</tr>
<tr>
<td><ul>
<li>
<p><strong>不在桩</strong></p>
<p>根据上述情况，如果有定位则直接开启任务；</p>
<p>如若无定位，则在触发任务后执行重定位，重定位成功则继续工作，重定位失败则原地报错。</p>
</li>
</ul></td>
<td><ul>
<li>在定位时，上报App 显示的是“定位中”</li>
</ul></td>
</tr>
<tr>
<td><strong>任务过程中</strong></td>
<td></td>
<td>RTK 信号不佳、且 VIO、重定位丢失后，<strong>报 E38</strong></td>
<td></td>
</tr>
</tbody>
</table>

# 工作项分解

一阶段工作项方案分解，待排期：

[ 阴影出桩建图、工作方案工作项拆解](https://roborock.feishu.cn/wiki/OIWwwD14viegf2kT5mFclS8Dnkd)



##



## 启动时，信号不好怎么报 Error 38

<table><colgroup><col width="136"><col width="172"><col width="398"><col width="355"></colgroup>
<thead>
<tr>
<th><strong>阶段</strong></th>
<th> RTK 情况</th>
<th>方案</th>
<th>App交互补充</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>建图启动</strong></td>
<td>ALL</td>
<td>建图启动时，各类信号情况不报 Error 38</td>
<td> 参见上文</td>
</tr>
<tr>
<td rowspan="3"><strong>任务启动</strong><br />（机器人要 自己去做 GOTO，包括自动割草、回充等）<br /></td>
<td><ul>
<li>故障、冷启动</li>
</ul></td>
<td><strong>在这种状态下，不自动退桩、或不重定位。</strong><br />先上报 App “启动中”/“定位系统恢复中”，先<strong>进行恢复、等待冷启动结束</strong>，超时未恢复上报 Error 38</td>
<td><ul>
<li>在等待进到 0/1/2/4/5 时，上报App 显示的是 “启动中”/“定位系统恢复中”</li>
</ul></td>
</tr>
<tr>
<td rowspan="2"><ul>
<li>0/1/2/4/5</li>
</ul></td>
<td><ul>
<li>
<p><strong>在桩</strong></p>
<p>先退桩，根据上述情况退桩进行 SLAM 初始化、以及重定位，如果失败，报 Error 38</p>
</li>
</ul></td>
<td><ul>
<li>在退出基站时，上报App 显示的是“退出基站中”</li>
<li>在定位时，上报App 显示的是“定位中”</li>
</ul></td>
</tr>
<tr>
<td><ul>
<li>
<p><strong>不在桩</strong></p>
<p>根据上述情况，进行重定位，如果失败，报 Error 38</p>
</li>
</ul></td>
<td><ul>
<li>在定位时，上报App 显示的是“定位中”</li>
</ul></td>
</tr>
</tbody>
</table>

## E38 弹窗交互调整：

<table><colgroup><col width="485"><col width="576"></colgroup>
<thead>
<tr>
<th>原弹窗</th>
<th>期望调整</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>解决方案</strong><ol>
<li>机器人信号不佳，将机器人移至无遮挡、开阔区域后重试；</li>
<li>若仍失败，请检查 RTK 基站指示灯是否为绿灯常亮：</li>
</ol>1）若不是，请插拔RTK基站电源并等待 3 分钟后再重试；<br />2）若仍未解决，且指示灯频繁异常，建议重新选址安装 RTK 基站。<ul>
<li>如已更换 RTK 基站，请扫码绑定新基站。</li>
</ul><em>*注意： 调整基站位置或更换 RTK 基站后需重新建图。</em><br /><strong>按钮：我已处理 / 扫码配对</strong></td>
<td><strong>解决方案</strong><blockquote>
<ol>
<li>机器人信号不佳，将机器人移至无遮挡、开阔区域后重试；</li>
<li>若仍失败，请检查 RTK 基站指示灯是否为绿灯常亮：</li>
</ol>
<p>1）若不是，请插拔RTK基站电源并等待 3 分钟后再重试；</p>
<p>2）若仍未解决，且指示灯频繁异常，建议重新选址安装 RTK 基站。</p>
<p><em>*注意： 调整基站位置或更换 RTK 基站后需重新建图。</em></p>
</blockquote><strong>按钮：我已处理 / 仍未解决</strong><br /><strong>解决方案</strong><blockquote>
<p>如若仍未解决，请确认已更换 RTK 基站，请扫码绑定新基站。</p>
</blockquote></td>
</tr>
</tbody>
</table>

# 关联需求：

http://192.168.111.52/index.php?m=bug\&f=view\&t=html&=\&bugID=446229

### 背景：

当用户刚开机时，从开机到 RTK 信号恢复到 4，或未恢复到 4 但已 120s ，认为机器处于冷启动状态。如若在这个阶段，当前自检会直接不通过，然后报 E38。

## 需求：

1、工作、回充启动（仅这两个），自检刨除 RTK 的冷启动状态，冷启动状态下自检通过；

2、冷启动状态下，进入工作启动状态，RTK 款启动状态至多 120s，或 RTK 进到 4，若启动状态结束没有进到 4，则报 E38，进到 4 则开始退桩或重定位割草。

<http://192.168.111.52/index.php?m=file&f=read&t=png&fileID=1314024>

![](<images/【RTK 款】阴影出桩建图、工作（退两段）-image-1.png>)

3、RTK 款启动中状态（100ms 的情况不用显示），如图中 RTK 款冷启动状态下、以及雷达款不在桩预热阶段，插件显示如下：

![](<images/【RTK 款】阴影出桩建图、工作（退两段）-image-2.png>)

<http://192.168.111.52/index.php?m=file&f=read&t=png&fileID=1306527>

文案：启动中…/定位中…/退出基站中…
