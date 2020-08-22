# ia_movie_rec

## Designing a recommendation engine

There are 3 approach to design any recommendation algorithm. A best practise is to use a combination of these to create a recommendation engine.
1. Popularity indexing
2. Collaborative Filtering
3. Content based ranking

Approach (1) takes into account current trends and checks what data is frequently retrieved in a narrow time frame. E.g. YouTube videos in trending section. Since popularity varies with time and is a realtime metric, we wont be able to use this approach in our case.

Approach (2) is useful when we have a social network within the system and there is substantial user profiling done on recommendation data. E.g. say user A has watched movies X,Y,Z and user B has watched only X. But user A and B are friends. So we can recommend movies Y,Z to B. But in our case, we dont have a social network API to leverage so we wont be able to use this approach.

Approach (3) takes into account vector based similarity of data points based on various dimensions. Your data may have a lot of features and 2 data points may be similar in some or all features. We can rank similarity of target data with all data points in DB and find out recommendations. This is the approach we are going to take. Because this method relies on persistent static documents with lot of features.