from pathlib import Path
import json
from content import LESSONS,MODULES
from checks import CHECKS
from deep_core import DEEP
import deep_fp1_fs1
import deep_fp2_fm1
import deep_fs2_fm2
import deep_d1_d2
P=Path(__file__).resolve().parents[1]
for lesson in LESSONS:
 assert lesson['id'] in CHECKS,lesson['id']
 lesson['check']={'q':CHECKS[lesson['id']][0],'a':CHECKS[lesson['id']][1]}
 if lesson['id'] in DEEP:lesson['deep']=DEEP[lesson['id']]
index=(P/'index.html').read_text(encoding='utf-8')
if 'src="further-tools.js' not in index:index=index.replace('<script src="further-data.js', '<script src="further-tools.js?v=20261023"></script>\n<script src="further-data.js',1)
(P/'index.html').write_text(index,encoding='utf-8')
search=(P/'topic-search.js').read_text(encoding='utf-8').replace('learn-last-lesson-alevel-maths','learn-further-maths-last-lesson').replace('Try bounds, integration or hypothesis tests','Try complex numbers, matrices or induction');(P/'topic-search.js').write_text(search,encoding='utf-8')
# Select genuine authored questions for Core Pure revision papers. Both cover the
# whole Core Pure pool; there is no official syllabus split between Papers 1 and 2.
def subset(items,target):
 dp={0:[]}
 for item in items:
  m=len(item['practice']['steps'])
  for total,chosen in list(dp.items())[::-1]:
   if total+m<=target and total+m not in dp:dp[total+m]=chosen+[item]
 assert target in dp
 return dp[target]
core=[l for l in LESSONS if l['module']=='core']
papers=[]
# Revision papers draw on the multi-part exam questions written for each lesson. The two Core Pure
# papers use different questions (never the same question twice) and each totals exactly 75 marks.
qm=lambda q:sum(p['m'] for p in q['parts'])
def pick(lessons,target,allowed):
 """choose at most one allowed question per lesson, total exactly target, covering as many lessons as possible"""
 best={0:[]}
 for l in lessons:
  nxt=dict(best)
  for total,chosen in best.items():
   for k in allowed(l):
    t=total+qm(l['deep']['exam'][k])
    if t<=target and (t not in nxt or len(nxt[t])<len(chosen)+1):nxt[t]=chosen+[(l['id'],k)]
  best=nxt
 assert target in best,target
 return best[target]
core=[l for l in LESSONS if l['module']=='core']
p1=pick(core,75,lambda l:[1]);used=set(p1)
p2=pick(core,75,lambda l:[k for k in (2,0) if (l['id'],k) not in used])
assert not set(p1)&set(p2)
papers=[]
for i,items in enumerate([p1,p2],1):
 papers.append(dict(id='fm-core-paper-'+str(i),module='core',title='Core Pure revision paper '+str(i),minutes=90,marks=75,kind='core-paper',lessons=[a for a,_ in items],items=[dict(lesson=a,q=k)for a,k in items],reuse='Multi-part questions drawn from the Core Pure lesson question bank; Papers 1 and 2 share no questions. Use them for timed consolidation.'))
for key,title,code in MODULES[1:]:
 selected=[l for l in LESSONS if l['module']==key];items=[(l['id'],0) for l in selected];marks=sum(qm(l['deep']['exam'][0]) for l in selected)
 papers.append(dict(id='fm-'+key+'-assessment',module=key,title=title+' · module assessment',minutes=round(marks*1.2),marks=marks,kind='module-assessment',lessons=[a for a,_ in items],items=[dict(lesson=a,q=k)for a,k in items],reuse='Short original revision assessment using one multi-part question from each lesson. This is not a full 75-mark examination paper.'))
data=dict(board='Pearson Edexcel',qualification='9FM0',checked='2026-10-23',modules=[dict(id=k,title=t,code=c)for k,t,c in MODULES],lessons=LESSONS,papers=papers)
(P/'course.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');(P/'further-data.js').write_text('window.FURTHER_COURSE='+json.dumps(data,ensure_ascii=False)+';\n',encoding='utf-8')
print(len(LESSONS),'lessons built')
