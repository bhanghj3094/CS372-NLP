## Dataset

### Data Scheme

> (   
> &nbsp;&nbsp;&nbsp;&nbsp;reviewText,   
> &nbsp;&nbsp;&nbsp;&nbsp;ratings (0 ~ 5)   
> )


### References

1. [Amazon Product Data](https://nijianmo.github.io/amazon/index.html#samples)
2. [Mendeley Movie Reviews](https://data.mendeley.com/datasets/38j8b6s2mx/1)
3. [Illinois DAIS Lab (TripAdvisor)](http://sifaka.cs.uiuc.edu/~wang296/Data/index.html)
4. [Movie Reviews(scale-dataset v1.0)](http://www.cs.cornell.edu/people/pabo/movie-review-data/)
5. [Book Review (Multi-Domain Sentiment Dataset)](http://www.cs.jhu.edu/~mdredze/datasets/sentiment/index2.html)


### CSVReader.py
#### Option for Using
1. Place csvReader.py in the root directory of Dataset
2. Dataset folder number starts from 1 (1~5)
3. File number starts from 0

#### Usage
> rdr = Reader()
> rdr.open_csv(3,0) #folder#_3 - file_0

#### Return
List of Tuples : [(reviewText,rating),]
