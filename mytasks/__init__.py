from socket_pro import socketio
import asyncio
from asyncio import CancelledError
import subprocess
import sys
import re


class MTask:
    def __init__(self, socket: socketio, messageport: str):
        self.__messageport = messageport
        self.__socket = socket
        self.__task1 = None
        self._process = None  # Track the process separately

    async def __read_stream(self, stream: asyncio.StreamReader):
        """Helper method to read and process a stream."""
        while True:
            line = await stream.readline()
            if not line:
                break
            try:
                decoded_line = line.decode("ascii").rstrip()

                if decoded_line:
                    try:
                        await self.__socket.broadcast(
                            self.__messageport, data={"message": decoded_line}
                        )
                    except Exception as e:
                        print(f"WebSocket broadcast error: {e}")
                    sys.stdout.flush()
            except Exception as e:
                print(f"Error processing line: {e}")

    async def __task(self, cmd: str):
        try:
            # Run nmap with output streaming
            self._process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                limit=1024 * 1024,  # Set buffer limit to prevent memory issues
            )

            # Run stdout and stderr reading concurrently
            await asyncio.gather(
                self.__read_stream(self._process.stdout),
                self.__read_stream(self._process.stderr),
            )

            # Wait for the process to complete
            await self._process.wait()

        except CancelledError:
            print("Task was cancelled")
            await self._terminate_process()
            raise
        except Exception as e:
            print(f"Error in task: {e}")
            await self._terminate_process()
            raise
        finally:
            self._process = None

    async def _terminate_process(self):
        """Helper method to terminate the process."""
        if self._process and self._process.returncode is None:
            try:
                self._process.terminate()
                await asyncio.wait_for(self._process.wait(), timeout=5)
            except (ProcessLookupError, asyncio.TimeoutError) as e:
                print(f"Error terminating process: {e}")
                try:
                    self._process.kill()
                except ProcessLookupError:
                    pass

    async def taskrun(self, cmd: str):
        if self.__task1 and not self.__task1.done():
            print("Task is already running")
            return

        self.__task1 = asyncio.create_task(self.__task(cmd))
        print(f"Task running: {self.__task1.get_name()}")

        await self.__socket.broadcast(
            self.__messageport,
            data={"message": f"Task running: {self.__task1.get_name()}"},
        )

    async def stop(self):
        if self.__task1 and not self.__task1.done():
            self.__task1.cancel()
            try:
                await self.__task1
            except CancelledError:
                await self.__socket.broadcast(
                    self.__messageport,
                    data={"message": f"{self.__task1.get_name()} is cancelled"},
                )
            except Exception as e:
                print(f"Error during cancellation: {e}")
            finally:
                self.__task1 = None
