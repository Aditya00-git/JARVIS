import asyncio
from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager


class SpotifyWatcher:
    def get_song(self):
        try:
            async def run():
                sessions = await MediaManager.request_async()
                current = sessions.get_current_session()
                if not current:
                    return "Nothing Playing", ""

                props = await current.try_get_media_properties_async()
                return props.title, props.artist

            return asyncio.run(run())
        except:
            return "Nothing Playing", ""
