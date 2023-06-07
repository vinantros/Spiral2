from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api import TranscriptsDisabled
from youtubesearchpython import VideosSearch
import os

AI = os.getenv('OPENAI_API_KEY')

def youtube_search(message):
    """
    Search for videos on YouTube based on the message and return a summary of the
    transcript from the first result video. 

    Args:
    - message (str): The search query for the video.

    Returns:
    - summary (str): A summarized version of the transcript from the video.
    """
    # Search for videos on YouTube based on the message
    videos_search = VideosSearch(f"{message}", limit=1)
    results = videos_search.result()

    # Get transcript from video and format it as text
    for video in results['result']:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video['id'])
        except TranscriptsDisabled:
            print("Transcripts Disabled")
            return ""

        formatter = TextFormatter()
        txt_formatted = formatter.format_transcript(transcript)

    # Split text into chunks and create Document objects for each chunk
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(txt_formatted)
    docs = [Document(page_content=chunk) for chunk in texts]

    # Use OpenAI to summarize the text and return the summary
    llm = OpenAI(temperature=0, openai_api_key=AI)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)
    return summary