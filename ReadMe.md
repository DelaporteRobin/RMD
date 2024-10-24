# RMD - RenderMan Denoiser - v0.2
### Writen by Quazar

RMD is an interface allowing you to use the latest Renderman Denoiser (available since Renderman 25)
with custom settings, keeping in your final renders AOV's and lightgroups you created.
It also include some features to remove unwanted channels from the final Denoised Renders, 
as well as compression methods, which in certain case can divide the file weight by 12.


You can read the documentation [HERE](https://www.notion.so/a13a63a10cde4ebda42246b9a3c6e408?pvs=4)

The TUI design was made using the Textual library, go check their [WEBSITE](https://textual.textualize.io/) if you feel interested.


### Tasklist for dev
- [ ] Include independant combine process (without using Denoise algorythm)
- [ ] Include independant compress process (without using Denoise algorythm)
- [ ] Return if wanted a full data set about the input sequence informations




