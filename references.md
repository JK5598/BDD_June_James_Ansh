Reference 1: Kuhn, H.W. (1955), The Hungarian method for the assignment problem†. Naval Research Logistics, 2: 83-97. https://doi.org/10.1002/nav.3800020109

Summary: 
Given an n x n table of scores rating how well each person performs each job, find the one-to-one assignment of persons to jobs that maximizes the total score. Solution method. He shows that results from two Hungarian mathematicians (Konig and Egervary) can be adapted into an efficient algorithm, "the Hungarian method.

Reference 2 : Paluch, Katarzyna. (2013). Capacitated Rank-Maximal Matchings. 10.1007/978-3-642-38233-8_27. 

Summary: Instead of minimizing total rank, this maximizes how many people get their 1st choice first, then 2nd choice among what's left, and so on. A stricter, lexicographic version of fairness. Same doctors/hospitals setup as yours, just a different (and harder) objective than the one you're implementing.

Reference 3: Bertsekas, D. P. (1981). "A new algorithm for the assignment problem." Mathematical Programming, 21(1), 152–171.

Summary: Auction alternative: unassigned doctors bid up prices on hospitals instead of searching augmenting paths. Claims ~10x faster than Hungarian at scale.
