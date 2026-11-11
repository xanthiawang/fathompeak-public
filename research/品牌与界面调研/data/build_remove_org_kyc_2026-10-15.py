"""企业后台去掉「企业认证」（Zixin 2026-10-15："感觉不太需要企业认证，因为他和我们签了合同才有这个界面"）。叠在线上 4e298b8 上。
企业账户只有签约后由沐仞开通，签约时已核对主体，后台里不再让企业管理员做认证：
 · 侧栏「企业认证」只留给个人（实名认证）和超管；企业管理员、成员都看不到。
 · 认证页里「企业认证」一条只超管能看到。
 · 钱包发票表单的说明「企业认证通过后抬头固定为认证主体」改成「抬头默认为合同签约主体」。
用法：python3 -I build_remove_org_kyc_2026-10-15.py <线上 index.html> <输出 html>
"""
import json, sys

SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding='utf8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)


rep('<button type="button" data-p="kyc" class="sup-new" data-roles="personal admin root">', '<button type="button" data-p="kyc" class="sup-new" data-roles="personal root">')
rep('<li data-roles="admin root"><div><b>企业认证</b>', '<li data-roles="root"><div><b>企业认证</b>')
T = '抬头默认为合同签约主体。'
rep('<p class="cs-help">企业认证通过后抬头固定为认证主体。</p>', f'<p class="cs-help">{T}</p>')
EN = {T: 'Defaults to the party named in your contract.'}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 企业不做认证 */\n  syncAuthLocale(); applyLang();')
open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT)
