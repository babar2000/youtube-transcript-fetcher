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

def get_transcript(video_id):
    # Try to get English transcript
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except Exception as e:
        return None, None, f"Error fetching transcript: {e}"

    text = ""
    srt = ""
    for index, t in enumerate(transcript):
        text += t['text'] + ' '
        start = int(t['start'])
        duration = int(t['duration'])
        hours, minutes, seconds = start // 3600, (start % 3600) // 60, start % 60
        end_hours, end_minutes, end_seconds = (start + duration) // 3600, ((start + duration) % 3600) // 60, (start + duration) % 60
        srt += f"{index + 1}\n{hours:02}:{minutes:02}:{seconds:02},000 --> {end_hours:02}:{end_minutes:02}:{end_seconds:02},000\n{t['text']}\n\n"
    return text, srt, None

def save_to_file(text, srt, filename):
    with open(f"{filename}.txt", "w", encoding="utf-8") as txt_file:
        txt_file.write(text)
    with open(f"{filename}.srt", "w", encoding="utf-8") as srt_file:
        srt_file.write(srt)

# Video ID is the code at the end of your video
video_id = "--JP-UorUgs"  
transcripts = list_available_transcripts(video_id)

# Check if English transcript is available
english_transcript = None
for transcript in transcripts:
    if transcript['language_code'] == 'en':
        english_transcript = transcript
        break

if english_transcript:
    transcript_text, transcript_srt, error = get_transcript(video_id)
    
    if error:
        print(error)
    else:
        print(f"\nTranscript in English ({english_transcript['type']}):")
        print(transcript_text)

        # Save transcript to files
        save_to_file(transcript_text, transcript_srt, f"transcript_{video_id}")
        print(f"\nTranscript saved to transcript_{video_id}.txt and transcript_{video_id}.srt")
else:
    print("No English transcript available for this video.")
