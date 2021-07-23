#110 Automatic Rebound Attacks on AES-like Hashing by Exploiting Related-key Differentials
===

A Quick Revision
---

A revised version of the paper is provided at (https://github.com/rebound-rk/rebound-rk/blob/main/paper-quick-revised.pdf). In this revision:


* To explore the classic attacks with our automatic model, we identify the new 5-round classic collision attack and a 6-round classic free-start collision attack on Saturnin in Supplementary Material B.

* To achieve better quantum attacks than CNS algorithm, we identify the new 7-round semi-free-start collision attack on Saturnin in Supplementary Material C. The time complexity of the new quantum attack is 2^{90.99} without qRAM or classcial memory, which is better than CNS algorithm whose time and memory is 2^{102.4} and 2^{51.2}, respectively.

* The new results are updated in Table 1



Source Codes
---

* The MILP model of related-key rebound attack on Saturnin is in saturnin_rebound.py.

* The code for detecting contradictions and generate tex file is in sol2tex.py.
