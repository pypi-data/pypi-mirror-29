# SonicParanoid: very fast, accurate, and easy orthology #

SonicParanoid is a stand-alone software tool for the identification of orthologous relationships among multiple species.

It was developed at [Iwasaki-lab](http://iwasakilab.bs.s.u-tokyo.ac.jp) at [The University of Tokyo](http://www.u-tokyo.ac.jp/en/index.html).

A more user friendly description of the method and its use can be found at the [`sonicparanoid web-page`](http://iwasakilab.bs.s.u-tokyo.ac.jp/sonicparanoid)

## Fast ##

SonicParanoid is the fastest method for orthology inference. It can infer orthologous relationships for 40 Eukaryotic proteomes in less than 7 hours, or for dozens of prokaryotes in about few minutes, using only 8 CPUs.

## Accurate ##

SonicParanoid was tested using a benchmark proteome dataset from [the Quest for Orthologs consortium](http://questfororthologs.org), and the correctness of its predictions was assessed using a public benchmark service. When compared to other 14 orthology prediction tools, SonicParanoid showed a [balanced trade-off between precision and recall](http://orthology.benchmarkservice.org/cgi-bin/gateway.pl?f=CheckResults&p1=72d29d4aebb02e0d396fcad2), with an accuracy comparable to that of well-established inference methods.

## Easy to use ##

SonicParanoid only requires the Python programming language and the MMseqs2.0 aligner to be installed in the laptop/server in order to work. Moreover, the very low hardware requirements make it possible to run on modern laptop computers. The 'update' feature allows users to easily maintain collections of orthologs that can be updated by adding or removing species.

## License ##
Copyright © 2017, Salvatore Cosentino, [The University of Tokyo](http://www.u-tokyo.ac.jp/en/index.html) All rights reserved. 

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at 
[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an __"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND__, either express or implied. See the License for the specific language governing permissions and limitations under the License.

## Contact ##
`Salvatore Cosentino`

* salvocos@bs.s.u-tokyo.ac.jp 
* salvo981@gmail.com

`Wataru Iwasaki`

* email: iwasaki@bs.s.u-tokyo.ac.jp
* web-page: [Iwasaki-lab](http://iwasakilab.bs.s.u-tokyo.ac.jp/eindex.html)