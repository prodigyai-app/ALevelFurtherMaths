from pathlib import Path
import json
from content import LESSONS,MODULES
from checks import CHECKS
P=Path(__file__).resolve().parents[1]
for lesson in LESSONS:
 assert lesson['id'] in CHECKS,lesson['id']
 lesson['check']={'q':CHECKS[lesson['id']][0],'a':CHECKS[lesson['id']][1]}
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
for i,ordered in enumerate([core,list(reversed(core))],1):
 selected=subset(ordered,75);papers.append(dict(id='fm-core-paper-'+str(i),module='core',title='Core Pure revision paper '+str(i),minutes=90,marks=75,kind='core-paper',lessons=[l['id']for l in selected],reuse='Questions are drawn from the lesson practice bank; use them for consolidation, not an unseen mock.'))
for key,title,code in MODULES[1:]:
 selected=[l for l in LESSONS if l['module']==key];marks=sum(len(l['practice']['steps'])for l in selected)
 papers.append(dict(id='fm-'+key+'-assessment',module=key,title=title+' · module assessment',minutes=round(marks*1.2),marks=marks,kind='module-assessment',lessons=[l['id']for l in selected],reuse='Short original revision assessment using the module lesson practice bank. This is not a full 75-mark examination paper.'))
data=dict(board='Pearson Edexcel',qualification='9FM0',checked='2026-10-23',modules=[dict(id=k,title=t,code=c)for k,t,c in MODULES],lessons=LESSONS,papers=papers)
(P/'course.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');(P/'further-data.js').write_text('window.FURTHER_COURSE='+json.dumps(data,ensure_ascii=False)+';\n',encoding='utf-8')
print(len(LESSONS),'lessons built')
