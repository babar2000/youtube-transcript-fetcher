!pip install youtube-transcript-api

from youtube_transcript_api import YouTubeTranscriptApi

def list_available_transcripts(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    available_transcripts = []

    for transcript in transcript_list:
        if transcript.is_generated:
            type_of_transcript = "auto-generated"
        else:
            type_of_transcript = "manual"

        available_transcripts.append({
            "language": transcript.language,
            "language_code": transcript.language_code,
            "is_generated": transcript.is_generated,
            "type": type_of_transcript
        })

    return available_transcripts

def get_transcript(video_id, language_code):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
    text = ""
    for t in transcript:
        text += t['text'] + ' '
    return text

video_id = "PUT_YOUR_VIDEO_ID_HERE"  # Video ID
transcripts = list_available_transcripts(video_id)

# Print available transcripts
print("Available transcripts:")
for transcript in transcripts:
    print(f"Language: {transcript['language']}, Language Code: {transcript['language_code']}, Type: {transcript['type']}")

# Download and display the first available transcript
if transcripts:
    selected_transcript = transcripts[0]
    try:
        transcript_text = get_transcript(video_id, selected_transcript['language_code'])
        print(f"\nTranscript in {selected_transcript['language']} ({selected_transcript['type']}):")
        print(transcript_text)
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No transcripts available for this video.")
