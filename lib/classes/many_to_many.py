from collections import Counter

class Article:
    all = []

    def __init__(self, author, magazine, title):
    # author, magazine instances and title string validation
    #Checks types and title length to enforce data integrity.
    #Raises exceptions if invalid data is provided.
        if not isinstance(author, Author):
            raise Exception("Author must be an Author instance")
        if not isinstance(magazine, Magazine):
            raise Exception("Magazine must be a Magazine instance")
        if not isinstance(title, str):
            raise Exception("Article title must be a string")
        if not 5 <= len(title) <= 50:
            raise Exception("Article title must be between 5 and 50 characters")
        self._author = author
        self._magazine = magazine
        self._title = title
     # Adds the article to the global Article.all.
        Article.all.append(self)
    #it calls line 24 to link the article to the magazine's article list.
        magazine.add_article(self)
        if self not in author._articles:
            author._articles.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if hasattr(self, '_title'):
            raise Exception("Cannot change article title after instantiation")
        if not isinstance(value, str):
            raise Exception("Article title must be a string")
        if not 5 <= len(value) <= 50:
            raise Exception("Article title must be between 5 and 50 characters")
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise Exception("Author must be an Author instance")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise Exception("Magazine must be a Magazine instance")
        self._magazine = value

class Author:
    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception("Author name must be a string")
        if len(name) == 0:
            raise Exception("Author name must be longer than 0 characters")
        self._name = name
        self._articles = []  # List to hold articles authored by this author

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if hasattr(self, '_name'):
            raise Exception("Cannot change author's name after instantiation")
        if not isinstance(value, str):
            raise Exception("Author name must be a string")
        if len(value) == 0:
            raise Exception("Author name must be longer than 0 characters")
        self._name = value

   # Property to access articles authored by this author

    def articles(self):
        return self._articles

    def magazines(self):
        return list(set(article.magazine for article in self._articles if isinstance(article.magazine, Magazine)))

    # Method to add an article to this author's list of articles
    # Validates that the magazine is an instance of Magazine and the title is a valid string
    # Raises exceptions if invalid data is provided.

    def add_article(self, magazine, title):
        if not isinstance(magazine, Magazine):
            raise Exception("Magazine must be a Magazine instance")
        if not isinstance(title, str) or not 5 <= len(title) <= 50:
            raise Exception("Article title must be a string between 5 and 50 characters")
        article = Article(self, magazine, title)
        return article
    
    # Derives unique categories (topics) from the author's magazines.
    # Returns None if no magazines.
    def topic_areas(self):
        magazines = self.magazines()
        if not magazines:
            return None
        return list(set(magazine.category for magazine in magazines))

class Magazine:
    _all = []

    def __init__(self, name, category):
        if not isinstance(name, str):
            raise Exception("Magazine name must be a string")
        if not 2 <= len(name) <= 16:
            raise Exception("Magazine name must be between 2 and 16 characters")
        if not isinstance(category, str):
            raise Exception("Magazine category must be a string")
        if len(category) == 0:
            raise Exception("Magazine category must be longer than 0 characters")
        self._name = name
        self._category = category
        self._articles = []
        Magazine._all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise Exception("Magazine name must be a string")
        if not 2 <= len(value) <= 16:
            raise Exception("Magazine name must be between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise Exception("Magazine category must be a string")
        if len(value) == 0:
            raise Exception("Magazine category must be longer than 0 characters")
        self._category = value

    def articles(self):
        return self._articles

    def add_article(self, article):
        if isinstance(article, Article) and article not in self._articles:
            self._articles.append(article)

    def contributors(self):
        return list(set(article.author for article in self._articles if isinstance(article.author, Author)))

    def article_titles(self):
        if not self._articles:
            return None
        return [article.title for article in self._articles]
    
    # Authors with >2 articles, using Counter.
    # Returns None if none qualify.

    def contributing_authors(self):
        author_counts = Counter(article.author for article in self._articles if isinstance(article.author, Author))
        authors = [author for author, count in author_counts.items() if count > 2]
        return authors if authors else None
    
    
    @classmethod
    # Finds magazine with most articles globally.
    def top_publisher(cls):
        if not Article.all:
            return None
        magazine_counts = Counter(article.magazine for article in Article.all if isinstance(article.magazine, Magazine))
        return max(magazine_counts, key=magazine_counts.get, default=None) if magazine_counts else None
    

    # Usage Example
if __name__ == "__main__":
        author = Author("Jane Doe")
        magazine = Magazine("Tech Weekly", "Technology")
        article = author.add_article(magazine, "AI Trends")
        print(author.articles())  
        print(magazine.contributing_authors())
        print(magazine.article_titles())
        print(magazine.top_publisher())
        print(magazine.contributors())
        print(magazine.category)  # Should return "Technology"
        print(magazine.name)  # Should return "Tech Weekly"
        print(author.name)  # Should return "Jane Doe"
        print(article.title)  # Should return "AI Trends"
        print(magazine.articles())  # Should return the list of articles in the magazine
        print(author.topic_areas())  # Should return the unique categories of magazines authored by Jane