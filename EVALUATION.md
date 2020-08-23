# VALIDATING OUR ENGINE

### Precision
- Recall in our case can be defined as ratio of movies that user actually liked out of the recommended ones
- In practise, our engine would be backed by a downstream feedback loop that collects data related to user-clicks, history, video log etc that could help us understand what movies were actually watches after recommendation

### Recall
- Recall in our case can be defined as ratio of movies that we recommended the user and that also happened to be users' choice as next movie to watch
- We could collect this data from bookmarks and movie search history.

### Mean Reciprocal Rank
- Since we have developed a rank based engine, we need to understand if our ranking was correct
- We may have recommended user movies A1, A2 ... AN (in ranked order) but after rating is given by user, we find that AN was most liked movie (which was least suggested). This mean ranking was mostly inaccurate.
- The reciprocal rank for Ai movie can be calculated as 1/Aj (where j is actual rank given by user after rating and i is provided rank)
- The mean of all movies in A1 to AN will be our Mean reciprocal rank
- Higher the Reciprocal rank, better is our ranking system