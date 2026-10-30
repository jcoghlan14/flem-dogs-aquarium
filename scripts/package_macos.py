from pathlib import Path
import plistlib
import shutil
import subprocess

root = Path(__file__).resolve().parents[1]
out = root / 'dist/Flem-Dogs-Aquarium-Mac-Apple-Silicon'
shared = out / 'Resources'
shared.mkdir(parents=True, exist_ok=True)
shutil.copy2(root / 'target/release/aquarium', shared / 'aquarium')
shutil.copytree(root / 'assets', shared / 'assets', dirs_exist_ok=True)
subprocess.run(['codesign', '--force', '--sign', '-', str(shared / 'aquarium')], check=True)
launcher = r'''
#include <mach-o/dyld.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
int main(void) {
 char raw[PATH_MAX], root[PATH_MAX], path[PATH_MAX];
 uint32_t n=sizeof(raw);
 if (_NSGetExecutablePath(raw,&n) || !realpath(raw,root)) return 1;
 for(int i=0;i<4;i++){char *s=strrchr(root,'/');if(!s)return 2;*s=0;}
 snprintf(path,sizeof(path),"%s/Resources/assets",root);setenv("AQUARIUM_ASSETS",path,1);
 setenv("AQ_WALLPAPER_MAIN","1",1);
 const char *home=getenv("HOME");
 if(home){
  snprintf(path,sizeof(path),"%s/Library/Caches/FlemDogsAquarium",home);
  mkdir(path,0700);setenv("AQ_CACHE_DIR",path,1);
  size_t k=strlen(path);snprintf(path+k,sizeof(path)-k,"/%s.log",LOGNAME);
  freopen(path,"a",stdout);freopen(path,"a",stderr);
 }
 snprintf(path,sizeof(path),"%s/Resources",root);if(chdir(path))return 3;
 execl("./aquarium","aquarium",MODE,NULL);
 perror("Flem Dogs Aquarium launcher");return 4;
}
'''
cfile = root / 'dist/launcher.c'
cfile.write_text(launcher)
for name, mode, suffix in [('Flem Dogs Aquarium', '--windowed', 'interactive'), ('Flem Dogs Aquarium Desktop', '--wallpaper', 'desktop')]:
 contents = out / (name + '.app') / 'Contents'
 exe = contents / 'MacOS/launch'
 exe.parent.mkdir(parents=True, exist_ok=True)
 info = {'CFBundleName':name, 'CFBundleDisplayName':name, 'CFBundleIdentifier':'com.flemdogs.aquarium.'+suffix, 'CFBundleExecutable':'launch', 'CFBundlePackageType':'APPL', 'CFBundleVersion':'1', 'CFBundleShortVersionString':'0.1.0', 'NSHighResolutionCapable':True, 'LSMinimumSystemVersion':'15.0'}
 if suffix == 'desktop':info['LSUIElement']=True
 (contents/'Info.plist').write_bytes(plistlib.dumps(info))
 subprocess.run(['clang',str(cfile),'-O2','-mmacosx-version-min=15.0','-Wall','-Wextra','-Werror',f'-DMODE="{mode}"',f'-DLOGNAME="{suffix}"','-o',str(exe)],check=True)
 subprocess.run(['codesign','--force','--sign','-',str(contents.parent)],check=True)
for name in ['LICENSE-MIT','LICENSE-APACHE']:
 shutil.copy2(root/name,out/name)
(out/'START-HERE.txt').write_text('''Flem Dogs Aquarium — Mac Apple silicon preview\n\nRequires macOS 15 or newer and an Apple silicon Mac (M1 or newer). Intel Macs are not supported by this download.\nExtract the ZIP and keep this folder together; both apps need the Resources folder.\nOpen Flem Dogs Aquarium.app to feed and interact with fish. Left-click feeds, scroll zooms, right-drag rotates, Esc quits.\nOpen Flem Dogs Aquarium Desktop.app for desktop wallpaper on the main display. Wallpaper ignores clicks.\nTo stop desktop mode, use Activity Monitor to quit its aquarium process.\nNo login item or automatic restart service is installed. Desktop mode can stop when displays disconnect.\nThis is a locally signed community preview, not an Apple-notarized release. If macOS blocks it, do not disable security protections; contact the sender.\nLogs and texture caches are stored in ~/Library/Caches/FlemDogsAquarium.\nOriginal project: https://github.com/akaloic/aquarium (MIT OR Apache-2.0).\n''')
archive = root / 'dist/Flem-Dogs-Aquarium-Mac-Apple-Silicon.zip'
subprocess.run(['ditto','-c','-k','--sequesterRsrc','--keepParent',str(out),str(archive)],check=True)
print(archive)
