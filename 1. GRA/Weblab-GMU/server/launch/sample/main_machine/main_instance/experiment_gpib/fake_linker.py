#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 onwards University of Deusto
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# This software consists of contributions made by many individuals, 
# listed below:
#
# Author: Pablo Orduña <pablo@ordunya.com>
# 

import os, sys

if __name__ == '__main__':
    assert len(sys.argv) == 11, "Linker example: ilink32 -Tpe -c whatever.obj c0x32, whatever.exe, , visa32 import32 cw32 bidsf \n\
Got %s arguments; \"%s\"" % ( len(sys.argv), ' '.join(sys.argv) )
    
    # assert sys.argv[0] == 'ilink32' #Not in the fake version
    assert sys.argv[1]  == '-Tpe' 
    assert sys.argv[2]  == '-c'
    assert sys.argv[3][-4:].lower() == '.obj'
    assert sys.argv[4]  == 'c0x32,'
    assert sys.argv[5][-5:].lower() == '.exe,'
    assert sys.argv[6]  == ','
    assert sys.argv[7]  == 'visa32'
    assert sys.argv[8]  == 'import32'
    assert sys.argv[9]  == 'cw32'
    assert sys.argv[10] =='bidsf'
    
    fname = sys.argv[5][:-1]
    try:
        f = open(fname,'w')
        source_lines = ""
        stdout_lines = ""
        for i in xrange(50):
        #   source_lines += "content sample line %i\\n" % i
            stdout_lines += "stdout sample line %i\\n" % i
        source_lines = """El nivel del marker -66.389 dBm
PTO :    FREC    : VALOR: dBm
============================================================

  1 :    1950000 :  642 : -66.387634 
  2 :    1950200 :  643 : -66.359848 
  3 :    1950400 :  644 : -66.332062 
  4 :    1950600 :  644 : -66.332062 
  5 :    1950800 :  644 : -66.332062 
  6 :    1951000 :  645 : -66.304276 
  7 :    1951200 :  645 : -66.304276 
  8 :    1951400 :  644 : -66.332062 
  9 :    1951600 :  644 : -66.332062 
 10 :    1951800 :  642 : -66.387634 
 11 :    1952000 :  642 : -66.387634 
 12 :    1952200 :  642 : -66.387634 
 13 :    1952400 :  641 : -66.415421 
 14 :    1952600 :  640 : -66.443207 
 15 :    1952800 :  642 : -66.387634 
 16 :    1953000 :  642 : -66.387634 
 17 :    1953200 :  643 : -66.359848 
 18 :    1953400 :  642 : -66.387634 
 19 :    1953600 :  643 : -66.359848 
 20 :    1953800 :  641 : -66.415421 
 21 :    1954000 :  641 : -66.415421 
 22 :    1954200 :  642 : -66.387634 
 23 :    1954400 :  644 : -66.332062 
 24 :    1954600 :  644 : -66.332062 
 25 :    1954800 :  642 : -66.387634 
 26 :    1955000 :  641 : -66.415421 
 27 :    1955200 :  642 : -66.387634 
 28 :    1955400 :  645 : -66.304276 
 29 :    1955600 :  643 : -66.359848 
 30 :    1955800 :  644 : -66.332062 
 31 :    1956000 :  645 : -66.304276 
 32 :    1956200 :  644 : -66.332062 
 33 :    1956400 :  640 : -66.443207 
 34 :    1956600 :  641 : -66.415421 
 35 :    1956800 :  640 : -66.443207 
 36 :    1957000 :  640 : -66.443207 
 37 :    1957200 :  640 : -66.443207 
 38 :    1957400 :  640 : -66.443207 
 39 :    1957600 :  642 : -66.387634 
 40 :    1957800 :  641 : -66.415421 
 41 :    1958000 :  641 : -66.415421 
 42 :    1958200 :  641 : -66.415421 
 43 :    1958400 :  644 : -66.332062 
 44 :    1958600 :  642 : -66.387634 
 45 :    1958800 :  644 : -66.332062 
 46 :    1959000 :  644 : -66.332062 
 47 :    1959200 :  642 : -66.387634 
 48 :    1959400 :  642 : -66.387634 
 49 :    1959600 :  640 : -66.443207 
 50 :    1959800 :  643 : -66.359848 
 51 :    1960000 :  645 : -66.304276 
 52 :    1960200 :  643 : -66.359848 
 53 :    1960400 :  642 : -66.387634 
 54 :    1960600 :  642 : -66.387634 
 55 :    1960800 :  644 : -66.332062 
 56 :    1961000 :  644 : -66.332062 
 57 :    1961200 :  642 : -66.387634 
 58 :    1961400 :  641 : -66.415421 
 59 :    1961600 :  640 : -66.443207 
 60 :    1961800 :  640 : -66.443207 
 61 :    1962000 :  640 : -66.443207 
 62 :    1962200 :  640 : -66.443207 
 63 :    1962400 :  640 : -66.443207 
 64 :    1962600 :  640 : -66.443207 
 65 :    1962800 :  644 : -66.332062 
 66 :    1963000 :  640 : -66.443207 
 67 :    1963200 :  640 : -66.443207 
 68 :    1963400 :  641 : -66.415421 
 69 :    1963600 :  642 : -66.387634 
 70 :    1963800 :  640 : -66.443207 
 71 :    1964000 :  641 : -66.415421 
 72 :    1964200 :  641 : -66.415421 
 73 :    1964400 :  641 : -66.415421 
 74 :    1964600 :  641 : -66.415421 
 75 :    1964800 :  640 : -66.443207 
 76 :    1965000 :  640 : -66.443207 
 77 :    1965200 :  641 : -66.415421 
 78 :    1965400 :  640 : -66.443207 
 79 :    1965600 :  641 : -66.415421 
 80 :    1965800 :  641 : -66.415421 
 81 :    1966000 :  641 : -66.415421 
 82 :    1966200 :  641 : -66.415421 
 83 :    1966400 :  640 : -66.443207 
 84 :    1966600 :  642 : -66.387634 
 85 :    1966800 :  642 : -66.387634 
 86 :    1967000 :  640 : -66.443207 
 87 :    1967200 :  640 : -66.443207 
 88 :    1967400 :  641 : -66.415421 
 89 :    1967600 :  641 : -66.415421 
 90 :    1967800 :  641 : -66.415421 
 91 :    1968000 :  641 : -66.415421 
 92 :    1968200 :  640 : -66.443207 
 93 :    1968400 :  641 : -66.415421 
 94 :    1968600 :  642 : -66.387634 
 95 :    1968800 :  642 : -66.387634 
 96 :    1969000 :  640 : -66.443207 
 97 :    1969200 :  640 : -66.443207 
 98 :    1969400 :  641 : -66.415421 
 99 :    1969600 :  644 : -66.332062 
100 :    1969800 :  644 : -66.332062 
101 :    1970000 :  644 : -66.332062 
102 :    1970200 :  644 : -66.332062 
103 :    1970400 :  641 : -66.415421 
104 :    1970600 :  640 : -66.443207 
105 :    1970800 :  643 : -66.359848 
106 :    1971000 :  643 : -66.359848 
107 :    1971200 :  641 : -66.415421 
108 :    1971400 :  640 : -66.443207 
109 :    1971600 :  641 : -66.415421 
110 :    1971800 :  641 : -66.415421 
111 :    1972000 :  640 : -66.443207 
112 :    1972200 :  641 : -66.415421 
113 :    1972400 :  640 : -66.443207 
114 :    1972600 :  642 : -66.387634 
115 :    1972800 :  641 : -66.415421 
116 :    1973000 :  640 : -66.443207 
117 :    1973200 :  640 : -66.443207 
118 :    1973400 :  642 : -66.387634 
119 :    1973600 :  641 : -66.415421 
120 :    1973800 :  640 : -66.443207 
121 :    1974000 :  640 : -66.443207 
122 :    1974200 :  642 : -66.387634 
123 :    1974400 :  642 : -66.387634 
124 :    1974600 :  640 : -66.443207 
125 :    1974800 :  641 : -66.415421 
126 :    1975000 :  640 : -66.443207 
127 :    1975200 :  640 : -66.443207 
128 :    1975400 :  641 : -66.415421 
129 :    1975600 :  642 : -66.387634 
130 :    1975800 :  641 : -66.415421 
131 :    1976000 :  640 : -66.443207 
132 :    1976200 :  643 : -66.359848 
133 :    1976400 :  641 : -66.415421 
134 :    1976600 :  641 : -66.415421 
135 :    1976800 :  641 : -66.415421 
136 :    1977000 :  642 : -66.387634 
137 :    1977200 :  643 : -66.359848 
138 :    1977400 :  642 : -66.387634 
139 :    1977600 :  642 : -66.387634 
140 :    1977800 :  640 : -66.443207 
141 :    1978000 :  640 : -66.443207 
142 :    1978200 :  640 : -66.443207 
143 :    1978400 :  640 : -66.443207 
144 :    1978600 :  641 : -66.415421 
145 :    1978800 :  643 : -66.359848 
146 :    1979000 :  642 : -66.387634 
147 :    1979200 :  642 : -66.387634 
148 :    1979400 :  642 : -66.387634 
149 :    1979600 :  641 : -66.415421 
150 :    1979800 :  642 : -66.387634 
151 :    1980000 :  642 : -66.387634 
152 :    1980200 :  644 : -66.332062 
153 :    1980400 :  642 : -66.387634 
154 :    1980600 :  641 : -66.415421 
155 :    1980800 :  640 : -66.443207 
156 :    1981000 :  640 : -66.443207 
157 :    1981200 :  643 : -66.359848 
158 :    1981400 :  643 : -66.359848 
159 :    1981600 :  642 : -66.387634 
160 :    1981800 :  640 : -66.443207 
161 :    1982000 :  640 : -66.443207 
162 :    1982200 :  640 : -66.443207 
163 :    1982400 :  641 : -66.415421 
164 :    1982600 :  642 : -66.387634 
165 :    1982800 :  640 : -66.443207 
166 :    1983000 :  642 : -66.387634 
167 :    1983200 :  642 : -66.387634 
168 :    1983400 :  640 : -66.443207 
169 :    1983600 :  640 : -66.443207 
170 :    1983800 :  640 : -66.443207 
171 :    1984000 :  640 : -66.443207 
172 :    1984200 :  640 : -66.443207 
173 :    1984400 :  640 : -66.443207 
174 :    1984600 :  640 : -66.443207 
175 :    1984800 :  642 : -66.387634 
176 :    1985000 :  640 : -66.443207 
177 :    1985200 :  640 : -66.443207 
178 :    1985400 :  641 : -66.415421 
179 :    1985600 :  644 : -66.332062 
180 :    1985800 :  645 : -66.304276 
181 :    1986000 :  642 : -66.387634 
182 :    1986200 :  644 : -66.332062 
183 :    1986400 :  644 : -66.332062 
184 :    1986600 :  645 : -66.304276 
185 :    1986800 :  641 : -66.415421 
186 :    1987000 :  642 : -66.387634 
187 :    1987200 :  642 : -66.387634 
188 :    1987400 :  641 : -66.415421 
189 :    1987600 :  640 : -66.443207 
190 :    1987800 :  640 : -66.443207 
191 :    1988000 :  640 : -66.443207 
192 :    1988200 :  640 : -66.443207 
193 :    1988400 :  642 : -66.387634 
194 :    1988600 :  642 : -66.387634 
195 :    1988800 :  640 : -66.443207 
196 :    1989000 :  641 : -66.415421 
197 :    1989200 :  640 : -66.443207 
198 :    1989400 :  640 : -66.443207 
199 :    1989600 :  641 : -66.415421 
200 :    1989800 :  643 : -66.359848 
201 :    1990000 :  645 : -66.304276 
202 :    1990200 :  645 : -66.304276 
203 :    1990400 :  641 : -66.415421 
204 :    1990600 :  641 : -66.415421 
205 :    1990800 :  642 : -66.387634 
206 :    1991000 :  641 : -66.415421 
207 :    1991200 :  640 : -66.443207 
208 :    1991400 :  642 : -66.387634 
209 :    1991600 :  641 : -66.415421 
210 :    1991800 :  641 : -66.415421 
211 :    1992000 :  641 : -66.415421 
212 :    1992200 :  642 : -66.387634 
213 :    1992400 :  645 : -66.304276 
214 :    1992600 :  644 : -66.332062 
215 :    1992800 :  643 : -66.359848 
216 :    1993000 :  642 : -66.387634 
217 :    1993200 :  642 : -66.387634 
218 :    1993400 :  640 : -66.443207 
219 :    1993600 :  640 : -66.443207 
220 :    1993800 :  641 : -66.415421 
221 :    1994000 :  645 : -66.304276 
222 :    1994200 :  644 : -66.332062 
223 :    1994400 :  641 : -66.415421 
224 :    1994600 :  641 : -66.415421 
225 :    1994800 :  643 : -66.359848 
226 :    1995000 :  642 : -66.387634 
227 :    1995200 :  641 : -66.415421 
228 :    1995400 :  640 : -66.443207 
229 :    1995600 :  640 : -66.443207 
230 :    1995800 :  641 : -66.415421 
231 :    1996000 :  644 : -66.332062 
232 :    1996200 :  641 : -66.415421 
233 :    1996400 :  640 : -66.443207 
234 :    1996600 :  641 : -66.415421 
235 :    1996800 :  642 : -66.387634 
236 :    1997000 :  641 : -66.415421 
237 :    1997200 :  642 : -66.387634 
238 :    1997400 :  640 : -66.443207 
239 :    1997600 :  641 : -66.415421 
240 :    1997800 :  642 : -66.387634 
241 :    1998000 :  642 : -66.387634 
242 :    1998200 :  644 : -66.332062 
243 :    1998400 :  644 : -66.332062 
244 :    1998600 :  642 : -66.387634 
245 :    1998800 :  644 : -66.332062 
246 :    1999000 :  645 : -66.304276 
247 :    1999200 :  642 : -66.387634 
248 :    1999400 :  641 : -66.415421 
249 :    1999600 :  640 : -66.443207 
250 :    1999800 :  642 : -66.387634 
251 :    2000000 :  641 : -66.415421 
252 :    2000200 :  644 : -66.332062 
253 :    2000400 :  640 : -66.443207 
254 :    2000600 :  641 : -66.415421 
255 :    2000800 :  640 : -66.443207 
256 :    2001000 :  644 : -66.332062 
257 :    2001200 :  642 : -66.387634 
258 :    2001400 :  642 : -66.387634 
259 :    2001600 :  642 : -66.387634 
260 :    2001800 :  642 : -66.387634 
261 :    2002000 :  642 : -66.387634 
262 :    2002200 :  643 : -66.359848 
263 :    2002400 :  641 : -66.415421 
264 :    2002600 :  641 : -66.415421 
265 :    2002800 :  643 : -66.359848 
266 :    2003000 :  643 : -66.359848 
267 :    2003200 :  642 : -66.387634 
268 :    2003400 :  642 : -66.387634 
269 :    2003600 :  643 : -66.359848 
270 :    2003800 :  644 : -66.332062 
271 :    2004000 :  641 : -66.415421 
272 :    2004200 :  641 : -66.415421 
273 :    2004400 :  640 : -66.443207 
274 :    2004600 :  638 : -66.498787 
275 :    2004800 :  648 : -66.220909 
276 :    2005000 :  640 : -66.443207 
277 :    2005200 :  638 : -66.498787 
278 :    2005400 :  649 : -66.193123 
279 :    2005600 :  641 : -66.415421 
280 :    2005800 :  644 : -66.332062 
281 :    2006000 :  642 : -66.387634 
282 :    2006200 :  640 : -66.443207 
283 :    2006400 :  642 : -66.387634 
284 :    2006600 :  641 : -66.415421 
285 :    2006800 :  643 : -66.359848 
286 :    2007000 :  641 : -66.415421 
287 :    2007200 :  640 : -66.443207 
288 :    2007400 :  640 : -66.443207 
289 :    2007600 :  641 : -66.415421 
290 :    2007800 :  640 : -66.443207 
291 :    2008000 :  642 : -66.387634 
292 :    2008200 :  644 : -66.332062 
293 :    2008400 :  643 : -66.359848 
294 :    2008600 :  643 : -66.359848 
295 :    2008800 :  641 : -66.415421 
296 :    2009000 :  640 : -66.443207 
297 :    2009200 :  643 : -66.359848 
298 :    2009400 :  643 : -66.359848 
299 :    2009600 :  642 : -66.387634 
300 :    2009800 :  642 : -66.387634 
301 :    2010000 :  642 : -66.387634 
302 :    2010200 :  640 : -66.443207 
303 :    2010400 :  641 : -66.415421 
304 :    2010600 :  641 : -66.415421 
305 :    2010800 :  641 : -66.415421 
306 :    2011000 :  641 : -66.415421 
307 :    2011200 :  641 : -66.415421 
308 :    2011400 :  641 : -66.415421 
309 :    2011600 :  641 : -66.415421 
310 :    2011800 :  643 : -66.359848 
311 :    2012000 :  641 : -66.415421 
312 :    2012200 :  640 : -66.443207 
313 :    2012400 :  640 : -66.443207 
314 :    2012600 :  640 : -66.443207 
315 :    2012800 :  641 : -66.415421 
316 :    2013000 :  641 : -66.415421 
317 :    2013200 :  641 : -66.415421 
318 :    2013400 :  640 : -66.443207 
319 :    2013600 :  642 : -66.387634 
320 :    2013800 :  643 : -66.359848 
321 :    2014000 :  642 : -66.387634 
322 :    2014200 :  641 : -66.415421 
323 :    2014400 :  642 : -66.387634 
324 :    2014600 :  644 : -66.332062 
325 :    2014800 :  641 : -66.415421 
326 :    2015000 :  641 : -66.415421 
327 :    2015200 :  644 : -66.332062 
328 :    2015400 :  643 : -66.359848 
329 :    2015600 :  640 : -66.443207 
330 :    2015800 :  640 : -66.443207 
331 :    2016000 :  642 : -66.387634 
332 :    2016200 :  640 : -66.443207 
333 :    2016400 :  643 : -66.359848 
334 :    2016600 :  642 : -66.387634 
335 :    2016800 :  641 : -66.415421 
336 :    2017000 :  642 : -66.387634 
337 :    2017200 :  641 : -66.415421 
338 :    2017400 :  641 : -66.415421 
339 :    2017600 :  640 : -66.443207 
340 :    2017800 :  642 : -66.387634 
341 :    2018000 :  641 : -66.415421 
342 :    2018200 :  641 : -66.415421 
343 :    2018400 :  642 : -66.387634 
344 :    2018600 :  640 : -66.443207 
345 :    2018800 :  640 : -66.443207 
346 :    2019000 :  641 : -66.415421 
347 :    2019200 :  641 : -66.415421 
348 :    2019400 :  641 : -66.415421 
349 :    2019600 :  641 : -66.415421 
350 :    2019800 :  640 : -66.443207 
351 :    2020000 :  640 : -66.443207 
352 :    2020200 :  640 : -66.443207 
353 :    2020400 :  641 : -66.415421 
354 :    2020600 :  640 : -66.443207 
355 :    2020800 :  641 : -66.415421 
356 :    2021000 :  644 : -66.332062 
357 :    2021200 :  641 : -66.415421 
358 :    2021400 :  640 : -66.443207 
359 :    2021600 :  640 : -66.443207 
360 :    2021800 :  640 : -66.443207 
361 :    2022000 :  640 : -66.443207 
362 :    2022200 :  640 : -66.443207 
363 :    2022400 :  640 : -66.443207 
364 :    2022600 :  641 : -66.415421 
365 :    2022800 :  642 : -66.387634 
366 :    2023000 :  641 : -66.415421 
367 :    2023200 :  641 : -66.415421 
368 :    2023400 :  640 : -66.443207 
369 :    2023600 :  640 : -66.443207 
370 :    2023800 :  640 : -66.443207 
371 :    2024000 :  641 : -66.415421 
372 :    2024200 :  641 : -66.415421 
373 :    2024400 :  640 : -66.443207 
374 :    2024600 :  640 : -66.443207 
375 :    2024800 :  638 : -66.498787 
376 :    2025000 :  650 : -66.165337 
377 :    2025200 :  642 : -66.387634 
378 :    2025400 :  643 : -66.359848 
379 :    2025600 :  641 : -66.415421 
380 :    2025800 :  640 : -66.443207 
381 :    2026000 :  643 : -66.359848 
382 :    2026200 :  642 : -66.387634 
383 :    2026400 :  640 : -66.443207 
384 :    2026600 :  640 : -66.443207 
385 :    2026800 :  641 : -66.415421 
386 :    2027000 :  641 : -66.415421 
387 :    2027200 :  641 : -66.415421 
388 :    2027400 :  641 : -66.415421 
389 :    2027600 :  641 : -66.415421 
390 :    2027800 :  641 : -66.415421 
391 :    2028000 :  640 : -66.443207 
392 :    2028200 :  644 : -66.332062 
393 :    2028400 :  643 : -66.359848 
394 :    2028600 :  642 : -66.387634 
395 :    2028800 :  642 : -66.387634 
396 :    2029000 :  642 : -66.387634 
397 :    2029200 :  641 : -66.415421 
398 :    2029400 :  640 : -66.443207 
399 :    2029600 :  640 : -66.443207 
400 :    2029800 :  640 : -66.443207 
401 :    2030000 :  640 : -66.443207 
402 :    2030200 :  641 : -66.415421 
403 :    2030400 :  641 : -66.415421 
404 :    2030600 :  640 : -66.443207 
405 :    2030800 :  641 : -66.415421 
406 :    2031000 :  642 : -66.387634 
407 :    2031200 :  641 : -66.415421 
408 :    2031400 :  641 : -66.415421 
409 :    2031600 :  641 : -66.415421 
410 :    2031800 :  642 : -66.387634 
411 :    2032000 :  644 : -66.332062 
412 :    2032200 :  640 : -66.443207 
413 :    2032400 :  640 : -66.443207 
414 :    2032600 :  641 : -66.415421 
415 :    2032800 :  640 : -66.443207 
416 :    2033000 :  641 : -66.415421 
417 :    2033200 :  640 : -66.443
207 
418 :    2033400 :  640 : -66.443207 
419 :    2033600 :  640 : -66.443207 
420 :    2033800 :  640 : -66.443207 
421 :    2034000 :  641 : -66.415421 
422 :    2034200 :  643 : -66.359848 
423 :    2034400 :  642 : -66.387634 
424 :    2034600 :  643 : -66.359848 
425 :    2034800 :  644 : -66.332062 
426 :    2035000 :  642 : -66.387634 
427 :    2035200 :  641 : -66.415421 
428 :    2035400 :  640 : -66.443207 
429 :    2035600 :  641 : -66.415421 
430 :    2035800 :  640 : -66.443207 
431 :    2036000 :  641 : -66.415421 
432 :    2036200 :  644 : -66.332062 
433 :    2036400 :  642 : -66.387634 
434 :    2036600 :  642 : -66.387634 
435 :    2036800 :  640 : -66.443207 
436 :    2037000 :  640 : -66.443207 
437 :    2037200 :  640 : -66.443207 
438 :    2037400 :  640 : -66.443207 
439 :    2037600 :  638 : -66.498787 
440 :    2037800 :  648 : -66.220909 
441 :    2038000 :  641 : -66.415421 
442 :    2038200 :  641 : -66.415421 
443 :    2038400 :  642 : -66.387634 
444 :    2038600 :  641 : -66.415421 
445 :    2038800 :  640 : -66.443207 
446 :    2039000 :  640 : -66.443207 
447 :    2039200 :  642 : -66.387634 
448 :    2039400 :  642 : -66.387634 
449 :    2039600 :  642 : -66.387634 
450 :    2039800 :  641 : -66.415421 
451 :    2040000 :  643 : -66.359848 
452 :    2040200 :  641 : -66.415421 
453 :    2040400 :  640 : -66.443207 
454 :    2040600 :  642 : -66.387634 
455 :    2040800 :  642 : -66.387634 
456 :    2041000 :  640 : -66.443207 
457 :    2041200 :  640 : -66.443207 
458 :    2041400 :  640 : -66.443207 
459 :    2041600 :  641 : -66.415421 
460 :    2041800 :  641 : -66.415421 
461 :    2042000 :  641 : -66.415421 
462 :    2042200 :  640 : -66.443207 
463 :    2042400 :  640 : -66.443207 
464 :    2042600 :  640 : -66.443207 
465 :    2042800 :  640 : -66.443207 
466 :    2043000 :  640 : -66.443207 
467 :    2043200 :  640 : -66.443207 
468 :    2043400 :  640 : -66.443207 
469 :    2043600 :  640 : -66.443207 
470 :    2043800 :  640 : -66.443207 
471 :    2044000 :  640 : -66.443207 
472 :    2044200 :  640 : -66.443207 
473 :    2044400 :  640 : -66.443207 
474 :    2044600 :  641 : -66.415421 
475 :    2044800 :  644 : -66.332062 
476 :    2045000 :  642 : -66.387634 
477 :    2045200 :  641 : -66.415421 
478 :    2045400 :  643 : -66.359848 
479 :    2045600 :  642 : -66.387634 
480 :    2045800 :  642 : -66.387634 
481 :    2046000 :  641 : -66.415421 
482 :    2046200 :  643 : -66.359848 
483 :    2046400 :  641 : -66.415421 
484 :    2046600 :  641 : -66.415421 
485 :    2046800 :  641 : -66.415421 
486 :    2047000 :  642 : -66.387634 
487 :    2047200 :  643 : -66.359848 
488 :    2047400 :  642 : -66.387634 
489 :    2047600 :  643 : -66.359848 
490 :    2047800 :  643 : -66.359848 
491 :    2048000 :  643 : -66.359848 
492 :    2048200 :  642 : -66.387634 
493 :    2048400 :  644 : -66.332062 
494 :    2048600 :  645 : -66.304276 
495 :    2048800 :  645 : -66.304276 
496 :    2049000 :  642 : -66.387634 
497 :    2049200 :  641 : -66.415421 
498 :    2049400 :  641 : -66.415421 
499 :    2049600 :  641 : -66.415421 
500 :    2049800 :  642 : -66.387634 
501 :    2050000 :  642 : -66.387634 
"""
        f.write("""#!/usr/bin/python

import time

print ""\"%s""\"
open("gpib.txt","w").write(""\"%s""\")

time.sleep(5)

""" %
                    (stdout_lines, source_lines))
        f.close()
    except Exception, e:
        import traceback
        print traceback.print_stack(e)

    if hasattr(os, 'chmod'):
        try:
            os.chmod(fname, 0755)
        except:
            pass
