# CSCI4970-MC-GamePlayingBot

# Building MineRL

* I have been running/testing this with:
* Windows 11
* Python 3.10.6
* Temurin Java8 JDK


1. Install Java8 JDK if not already (https://adoptium.net/temurin/releases/?version=8)



* I used Git-Bash here just because I know it works. 
* It very well may build/install just fine if run from command prompt/powershell if you have the necessary executables in your path.
* I just can't guarantee the build will succeed.
1. In the Utils/MineRL directory, run `pip install -e . -vvv`
   1. `-e` flag will install in edit mode, allowing us edit the MineRL source files without needing to reinstall the package with pip.
   2. `-vvv` flag just enables the verbose outputs. I've found that not all build errors will be shown without this.



3. Wait. (Seriously, this has taken up to 2 hours on my windows machine. Even with `-vvv`, there are periods where you will have no indication of progress).