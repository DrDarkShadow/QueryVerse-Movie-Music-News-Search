from crewai import Agent, LLM
from langchain.tools import Tool
from api_tools import TMDBMovieTools, ITunesMusicTools, NewsTools, GeneralSearchTools
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the LLM
llm = LLM(
    model=os.getenv("AZURE_MODEL"),
    api_version=os.getenv("AZURE_API_VERSION"),
    api_key=os.getenv("AZURE_API_KEY"),
    base_url=os.getenv("AZURE_BASE_URL")
)

class UnifiedSearchAgents:
    def __init__(self, tmdb_api_key, tmdb_token, serp_api_key):
        # Initialize API tools
        self.movie_tools = TMDBMovieTools(tmdb_api_key, tmdb_token)
        self.music_tools = ITunesMusicTools()
        self.news_tools = NewsTools(serp_api_key)
        self.search_tools = GeneralSearchTools(serp_api_key)
        
        # Create proper Tool objects
        self.movie_search_tool = Tool(
            name="Search Movies",
            description="Search for movies using TMDB API",
            func=self.movie_tools.search_movies
        )
        
        self.music_search_tool = Tool(
            name="Search Music",
            description="Search for music using iTunes API",
            func=self.music_tools.search_music
        )
        
        self.news_search_tool = Tool(
            name="Fetch News",
            description="Fetch news articles using SERP API",
            func=self.news_tools.fetch_news
        )
        
        self.web_search_tool = Tool(
            name="Web Search",
            description="Perform general web searches using SERP API",
            func=self.search_tools.web_search
        )

    def create_movie_agent(self):
        return Agent(
            role='Movie Search Specialist',
            goal='Find high-quality movie information based on user queries',
            backstory='''Expert in movie data analysis with vast knowledge of films, 
                       directors, and actors. Specializes in finding the best matches 
                       for user movie queries and presenting detailed information.''',
            llm=llm,
            tools=[self.movie_search_tool],
            verbose=True,
            allow_delegation=False
        )
        
    def create_music_agent(self):
        return Agent(
            role='Music Discovery Specialist',
            goal='Find and present music that matches user preferences',
            backstory='''Experienced music curator with deep knowledge of artists, 
                       genres, and trends. Skilled at matching user queries with 
                       the perfect songs and creating engaging music recommendations.''',
            llm=llm,
            tools=[self.music_search_tool],
            verbose=True,
            allow_delegation=False
        )
        
    def create_news_agent(self):
        return Agent(
            role='News Analyst',
            goal='Find and summarize relevant news stories',
            backstory='''Seasoned journalist with experience in quickly finding, 
                       analyzing, and summarizing news across various topics. 
                       Skilled at extracting key information and presenting it 
                       in a concise, informative manner.''',
            llm=llm,
            tools=[self.news_search_tool],
            verbose=True,
            allow_delegation=False
        )
        
    def create_search_agent(self):
        return Agent(
            role='Research Specialist',
            goal='Find accurate information for general queries',
            backstory='''Meticulous researcher with experience in finding reliable 
                       information across various domains. Skilled at evaluating 
                       sources, extracting key facts, and presenting comprehensive 
                       answers to user questions.''',
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
