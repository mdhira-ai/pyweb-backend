from socket_pro import socketio
import asyncio
from asyncio import CancelledError
import subprocess
import sys
import re

class MTask:
    def __init__(self):
        self.__task1 = None
       

    def _clean_output(self, line: str) -> str:
        """Clean and format the output line by normalizing whitespace and removing extra indentation."""
        # Remove leading/trailing whitespace and normalize multiple spaces/tabs to a single space
        cleaned = re.sub(r'\s+', ' ', line.strip())
        return cleaned

    async def task(self,mysocket:socketio):
        try:
            # Run nmap with output streaming
            process = await asyncio.create_subprocess_shell(
                "sudo nmap -v -A scanme.nmap.org",
                # "ping google.com",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Create tasks to read stdout and stderr concurrently
            async def read_stream(stream:asyncio.StreamReader, name):
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    decoded_line = line.decode()
                    cleaned_line = self._clean_output(decoded_line)
                    if cleaned_line:
                        print(f"{cleaned_line}")


                        await mysocket.broadcast('nmap',data={
                            'message': cleaned_line
                        })
                        sys.stdout.flush()

            # Run stdout and stderr reading concurrently
            await asyncio.gather(
                read_stream(process.stdout, "Output"),
                read_stream(process.stderr, "Error")
            )

            # Wait for the process to complete
            await process.wait()

        except CancelledError:
            print("Task was cancelled")
            if 'process' in locals():
                process.terminate()  # Gracefully terminate the process
                await process.wait()  # Wait for the process to fully exit
            raise
        except Exception as e:
            print(f"Error: {e}")
            raise

    async def taskrun(self,mysocket:socketio):
        self.__task1 = asyncio.create_task(self.task(mysocket))
        print(f"Task running: {self.__task1.get_name()}")

    async def stop(self):
        if self.__task1 is not None and not self.__task1.done():
            self.__task1.cancel()
            try:
                await self.__task1
            except CancelledError:
                print(f"{self.__task1.get_name()} is cancelled")