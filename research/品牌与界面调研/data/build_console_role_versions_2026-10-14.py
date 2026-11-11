"""后台按角色拆成几个版本的 HTML（Zixin 2026-10-14："直接做成后台几个版本的html 打开给我看"）。
输入：全部补充预览（已叠 build_console_backend）；输出四份文件，打开即进入对应身份的控制台：
  后台_个人版 / 后台_企业管理员版 / 后台_企业成员版 / 后台_超管版（2026-10-14 晚加）。正式版：不带预览身份切换、标出新增和黄色待确认标签。
只在内存里建预览账户，不发起真实调用，数据全为空状态。
用法：python3 -I build_console_role_versions_2026-10-14.py <全部补充预览.html> <输出目录>
"""
import os, sys

LIVE_OUT = sys.argv[sys.argv.index('--live-out') + 1] if '--live-out' in sys.argv else None  # 上线版：只输出一份正式 index.html，不带打开入口
SRC, OUTDIR = sys.argv[1], sys.argv[2]
base = open(SRC, encoding='utf8').read()
V = [('personal', '#console-preview', '后台_个人版_2026-10-14.html', '个人'),
     ('admin', '#console-preview-admin', '后台_企业管理员版_2026-10-14.html', '企业管理员'),
     ('member', '#console-preview-member', '后台_企业成员版_2026-10-14.html', '企业成员'),
     ('super', '#console-preview-super', '后台_超管版_2026-10-14.html', '超级管理员')]
SW_OLD = ('<a href="#console-preview" data-r="personal">个人</a><a href="#console-preview-admin" data-r="admin">企业管理员</a>'
          '<a href="#console-preview-member" data-r="member">企业成员</a><a href="#console-preview-super" data-r="super">超级管理员</a>')
if base.count(SW_OLD) != 1: sys.exit('[停止] 找不到预览身份切换（先跑 build_console_backend）')
SW_NEW = ''.join(f'<a href="{fn}" data-r="{r}">{lab}</a>' for r, _, fn, lab in V)
# 正式版（Zixin 2026-10-14 晚："下面不用加演示、登录什么的，直接给正式的 UI"）：
# 去掉预览身份切换和「标出新增」按钮；控制台与登录页里的黄色「待公司确认」标签、超管页「new-api 现成 / 需开发」标签不显示（这些写在《后台架构》里）
FORMAL_CSS = ('<style id="formal-ui">.bt .tbc,.ac .tbc,.ad-hr .bt-tag{display:none!important}'
              'html.sup-mark .sup-new{outline:none!important}</style>\n')
TOG = '<button class="sup-tog" id="supTog" type="button" aria-pressed="false">标出新增</button>'
SW_DIV = ('<div class="sup-roles" id="supRoles" role="group" aria-label="预览身份"><span>预览身份</span>' + SW_OLD + '</div>\n')


def formal(x, live=False):
    if x.count(SW_DIV) != 1 or x.count(TOG) != 1: sys.exit('[停止] 找不到预览身份切换或标出新增按钮')
    x = x.replace(SW_DIV, '').replace(TOG, '')
    x = x.replace('收款户名：北京沐仞科技有限公司。开户行与账号<span class="tbc">待公司提供</span>。', '收款户名：北京沐仞科技有限公司　开户行：--　账号：--<br>')
    for old, new in [("me.preview?'界面预览':", "me.preview?(me.type==='super'?'沐仞运营':me.type==='company'?'我的企业':'我的账户'):"),
                     ("toast('预览：预算设置没有保存到平台，需要平台支持后才能生效。')", "toast('预算提醒接入后即可生效。')" if live else "toast('预算已保存。')"),
                     ("toast('预览：开关不会保存。对应 new-api 系统设置 › 侧边栏模块。')", "toast('接入平台后即可使用。')" if live else "toast('已保存。')")]:
        if x.count(old) != 1: sys.exit('[停止] 正式版替换没有命中：' + old[:40])
        x = x.replace(old, new)
    k3 = x.index('  syncAuthLocale(); applyLang();')
    x = x[:k3] + "  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})({'沐仞运营':'FathomPeak operations','我的企业':'My company','我的账户':'My account','预算已保存。':'Budget saved.','已保存。':'Saved.','预算提醒接入后即可生效。':'Budget alerts take effect once connected.'});\n" + x[k3:]
    k2 = x.rindex('</head>')
    return x[:k2] + FORMAL_CSS + x[k2:]

for r, h, fn, lab in V:
    s = formal(base)
    # 页面脚本运行前把地址改成对应的预览入口：主脚本里的 btPreview 读到它就建好这个身份的空账户并进入控制台
    boot = ("<script>/* 后台角色版本：打开即进入「%s」控制台 */(function(){var h=location.hash;"
            "if(!h||h==='#home'||h==='#console'){history.replaceState(null,'',location.pathname+location.search+'%s')}})();</script>\n") % (lab, h)
    k = s.index('<head>') + len('<head>')
    s = s[:k] + '\n' + boot + s[k:]
    open(os.path.join(OUTDIR, fn), 'w', encoding='utf8').write(s)
    print('done:', fn)

# 体验中心（2026-10-14 夜）：个人账户，打开即在体验中心
s = formal(base)
boot = ("<script>/* 体验中心：打开即进个人控制台的体验中心 */(function(){var h=location.hash;"
        "if(!h||h==='#home'||h==='#console'){history.replaceState(null,'',location.pathname+location.search+'#console-preview')}})();</script>\n")
k = s.index('<head>') + len('<head>')
s = s[:k] + '\n' + boot + s[k:]
k = s.rindex('</body>')
s = s[:k] + "<script>setTimeout(function(){var b=document.querySelector('.cs-nav [data-p=\"play\"]'); if(b) b.click()},60)</script>\n" + s[k:]
open(os.path.join(OUTDIR, '后台_体验中心_2026-10-14.html'), 'w', encoding='utf8').write(s)
print('done: 后台_体验中心_2026-10-14.html')

# 登录入口两份（2026-10-14 晚）：客户登录（带演示登录）与运营后台登录，打开即在登录页
for h, fn, lab in [('#login', '后台_登录入口_2026-10-14.html', '客户登录'), ('#admin-login', '后台_超管登录_2026-10-14.html', '运营后台登录')]:
    s = formal(base)
    boot = ("<script>/* 登录入口：打开即在「%s」页 */(function(){var h=location.hash;"
            "if(!h||h==='#home'){history.replaceState(null,'',location.pathname+location.search+'%s')}})();</script>\n") % (lab, h)
    k = s.index('<head>') + len('<head>')
    s = s[:k] + '\n' + boot + s[k:]
    open(os.path.join(OUTDIR, fn), 'w', encoding='utf8').write(s)
    print('done:', fn)

if LIVE_OUT:
    open(LIVE_OUT, 'w', encoding='utf8').write(formal(base, live=True))
    print('done (上线版):', LIVE_OUT)
