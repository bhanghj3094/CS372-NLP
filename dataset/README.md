## Dataset

### Data Scheme

> (   
> &nbsp;&nbsp;&nbsp;&nbsp;review_text,   
> &nbsp;&nbsp;&nbsp;&nbsp;ratings (1 ~ 5)   
> )


### References

1. [Amazon Product Data](https://nijianmo.github.io/amazon/index.html#samples)
2. [Mendeley Movie Reviews](https://data.mendeley.com/datasets/38j8b6s2mx/1)
3. [Illinois DAIS Lab (TripAdvisor)](http://sifaka.cs.uiuc.edu/~wang296/Data/index.html)
4. [Movie Reviews(scale-dataset v1.0)](http://www.cs.cornell.edu/people/pabo/movie-review-data/)
5. [Book Review (Multi-Domain Sentiment Dataset)](http://www.cs.jhu.edu/~mdredze/datasets/sentiment/index2.html)


### CSV Reader

#### Options
1. Place csvReader.py in the root directory of Dataset
2. Dataset folder number starts from 1 (1 ~ 5)
3. File number starts from 0

#### Usage
> reader = Reader()
> reader.open_csv(3,0)  # folder_#3 - file_#0

#### Return
List of tuples : [  
&nbsp;&nbsp;&nbsp;&nbsp;( review_text, rating ),  
&nbsp;&nbsp;&nbsp;&nbsp;...  
]
