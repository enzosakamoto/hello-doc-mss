from pytube import YouTube
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://3.80.203.53",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the YouTube Downloader API!"}


@app.get("/download")
async def download_video(url: str):
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the highest resolution video stream
        stream = yt.streams.get_highest_resolution()

        file_path = f"{yt.title}.mp4"

        # Download the video to the current working directory
        stream.download(filename=file_path)

        def iterfile():
            with open(file_path, mode="rb") as file_like:
                yield from file_like
            os.remove(file_path)

        headers = {"Content-Disposition": f'attachment; filename="{yt.title}.mp4"'}

        return StreamingResponse(iterfile(), media_type="video/mp4", headers=headers)
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail="Error: Video is not available or cannot be downloaded",
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Error: Invalid URL")
    except Exception as e:
        raise HTTPException(
            status_code=400, detail="Error downloading video: " + str(e)
        )


@app.get("/videoInfo")
async def get_video_info(url: str):
    try:
        # Create a YouTube object
        yt = YouTube(url)

        title = yt.title
        author = yt.author
        embed = yt.embed_url
        thumbnail = yt.thumbnail_url

        return {
            "title": title,
            "author": author,
            "embed": embed,
            "thumbnail": thumbnail,
        }

    except KeyError:
        raise HTTPException(
            status_code=400,
            detail="Error: Video is not available or cannot be downloaded",
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Error: Invalid URL")
    except Exception as e:
        raise HTTPException(
            status_code=400, detail="Error downloading video: " + str(e)
        )
