# top30

Automatically creates run downs of songs given certain parameters.

## Building

On any platform with Python 3, the following will build and install the latest
release of top30:

    pip install top30

Installing from source is done as follows

    python3 setup.py install


### Windows Executable

A Windows executable can be created using PyInstaller. This creates the
directory `dist/top30`, which then can be distributed run. It requires the
ffmpeg static build to be downloaded into `../ffmpeg`

    pip install pyinstaller
    pyinstaller top30.spec

## Running

top30 can be run as either a command-line application or a GUI. The CLI version
takes two arguments - the current chart file and the previous chart file. Both
are expected to be in the [format](#Chart Format) provided by UCT Radio

    rundown-creator -c some_chart.docx -p some_chart.docx

The GUI has no such restrictions and can be run as is:

    top30

## GUI Operation

The GUI allows files to be added in sequence to the list on the left. These
files are then parsed into a rundown. All files with a readable start time in
the description field of the metadata (can be changed in the configuration file
to be any metadata field) are assumed to be songs, while any others are assumed
to be voice tracks. Songs are clipped to the length specified under Song Length
and are overlapped with voice tracks using the timings specified. All times are
in seconds.

## Chart Format
All charts are expected to be in Microsoft Word 2007+ format (docx). The content
is expected to follow the following structure:

| Top30 | Top30 Hitlist: |            |            |         |
|-------|----------------|------------|------------|---------|
|       | **Artist**     | **Song**   | **L/Week** | **Reg** |
|1      | Artist Name    | Song Title | UP/DOWN X  | I/L     |
|...                                                         |
