struct News {
	string url,
	string title,
	double related,
	string content
}

struct Price {
	string time,
	double price,
	double predict
}

service FutureService {
	list<News> futureRelatedNews(string future),
	list<Price> predictPrice(string future, i16 type)
}
