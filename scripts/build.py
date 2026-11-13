from pathlib import Path
import json
from content import LESSONS,MODULES
from checks import CHECKS
from deep_core import DEEP
import deep_fp1_fs1
import deep_fp2_fm1
import deep_fs2_fm2
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
# The lesson cp-argand keeps the circle-locus question; each core paper replaces it with a different locus
# question (same number of steps, so the 75 marks are unchanged) instead of repeating the lesson's.
SWAPS=[{'cp-argand':dict(q='Describe the locus |z − (3 + i)| = |z + 1 − i| and find where it crosses the real axis.',answer=None,steps=['The points are equally far from 3 + i and −1 + i.','The two centres share y = 1, so the locus is a perpendicular bisector through their midpoint (1,1).','It is the vertical line x = 1.','It crosses the real axis at z = 1.'])},
 {'cp-argand':dict(q='Describe the locus |z + 3 − 2i| = 5 and find the real numbers z that lie on it.',answer=None,steps=['The centre is (−3,2) and the radius is 5.','On the real axis y = 0, so (x + 3)² + 4 = 25.','Then (x + 3)² = 21.','x = −3 ± √21, approximately 1.58 and −7.58.'])}]
for i,ordered in enumerate([core,list(reversed(core))],1):
 selected=subset(ordered,75);papers.append(dict(swap=SWAPS[i-1],id='fm-core-paper-'+str(i),module='core',title='Core Pure revision paper '+str(i),minutes=90,marks=75,kind='core-paper',lessons=[l['id']for l in selected],reuse='Questions are drawn from the lesson practice bank; use them for consolidation, not an unseen mock.'))
for key,title,code in MODULES[1:]:
 selected=[l for l in LESSONS if l['module']==key];marks=sum(len(l['practice']['steps'])for l in selected)
 papers.append(dict(id='fm-'+key+'-assessment',module=key,title=title+' · module assessment',minutes=round(marks*1.2),marks=marks,kind='module-assessment',lessons=[l['id']for l in selected],reuse='Short original revision assessment using the module lesson practice bank. This is not a full 75-mark examination paper.'))
data=dict(board='Pearson Edexcel',qualification='9FM0',checked='2026-10-23',modules=[dict(id=k,title=t,code=c)for k,t,c in MODULES],lessons=LESSONS,papers=papers)
(P/'course.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');(P/'further-data.js').write_text('window.FURTHER_COURSE='+json.dumps(data,ensure_ascii=False)+';\n',encoding='utf-8')
print(len(LESSONS),'lessons built')
