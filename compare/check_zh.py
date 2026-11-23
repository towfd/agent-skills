# 檢查一份中文對照的段數和原文對不對得上。用法：python3 -I compare/check_zh.py <原文檔> <中文檔>
# 中文檔第一行是「TOPIC: 主題」，空一行後才是譯文。
import sys, re
def blocks(t): return re.split(r'\n\s*\n', t.strip('\n'))
en = blocks(open(sys.argv[1], encoding='utf-8').read())
z = open(sys.argv[2], encoding='utf-8').read()
m = re.match(r'TOPIC: (.+)\n\s*\n', z)
if not m: sys.exit('第一行要是「TOPIC: 主題」，然後空一行')
zh = blocks(z[m.end():])
if len(en) != len(zh):
    print(f'段數不合：原文 {len(en)} 段，中文 {len(zh)} 段')
    for i in range(max(len(en), len(zh))):
        a = en[i][:50].replace('\n', ' ') if i < len(en) else '（沒有）'
        b = zh[i][:30].replace('\n', ' ') if i < len(zh) else '（沒有）'
        print(f'{i+1:3} | {a} | {b}')
    sys.exit(1)
print('OK', len(en), '段')
