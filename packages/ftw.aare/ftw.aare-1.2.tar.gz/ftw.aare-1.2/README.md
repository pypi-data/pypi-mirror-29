# ftw.aare
A shell command which displays the current temperature of the Aare in Bern, Switzerland

## Installation Instructions

### Requirements
The command can be installed using `pipsi`. If you do not know what pipsi is and how to use, please install it first by visiting the [corresponding Github page](https://github.com/mitsuhiko/pipsi). The tool was implemented using `Python 3.6`.  

`ftw.aare` will work using Python 3.6 or 3.5, but keep in mind that it was not tested using `Python 3.5`

### Install the Tool
To install the tool with `pipsi` installed, you can run the following command:  
`pipsi install ftw.aare --python PATH_TO_PYTHON3.6`  

## Usage Instructions
You can see the current temperature of the `Aare` by typing:  
`aare`  
You also can use the tool to get the highest and the lowest temperature each day for the last seven days, by calling the tool as follows:
`aare --statistics`  

example:  
![aare_tool_demo.gif](https://github.com/4teamwork/ftw.aare/blob/master/docs/Aare_tool_demo.gif?raw=true)

 
