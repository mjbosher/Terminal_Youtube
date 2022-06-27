import cmd
import os
import datetime
import subprocess
import threading
import sys
from termcolor import colored, cprint
import getpass
import requests
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver import Firefox,common
from selenium.webdriver.firefox import options
import time
options=options.Options()
options.add_argument("--headless")

playlist = []
playlist_ = []
autoplay=['no']
user= getpass.getuser()
user = user.rstrip()
home="/home/" + user + "/"
download_dir = f'{home}Downloads/bigfolder'
print(download_dir)
config = f'{home}Downloads/Files/MPV'
if os.path.exists(config):
	pass
elif not os.path.exists(config):
	os.mkdir(config)
ext=[x.lower() for x in 'mkv,mp4,m4a,m4v,f4v,f4a,m4b,m4r,f4b,mov,3gp,3gp2,3g2,3gpp,3gpp2,ogg,oga,ogv,ogx,wmv,wma,asf*,webm,flv,AVI*,OP1a,OP-Atom,ts,WAV,LXF,GXF* ,VOB*'.split(',')]
ext1=[x.lower() for x in 'MP3,AAC,HE-AAC,AC3,EAC3,Vorbis,WMA,PCM,WEBVTT,DFXP,SAMI,SCC,SRT,TTML,3GPP,flac,wav,opus'.split(',')]
ext.extend(ext1)
mode=['--on-all-workspaces --ontop  --fs=no --geometry=400x300-0+0 --no-terminal']
class DevNull:
	def write(self, msg):
		p1 = threading.Thread(target=event_loop().main_event_loop)
		p2 = threading.Thread(target=CmdParse().cmdloop)
		p1.start()
		p2.start()

sys.stderr = DevNull()

class event_loop:
	@staticmethod
	def check_pids():
		ps = [x for x in str(subprocess.check_output(['ps','-e'])).split('\\n')]
		ps.pop(0)
		ps.pop()
		ps = [x.split(' ')[-1] for x in ps]
		return(ps)
	@staticmethod
	def main_event_loop():
		while True:
			
			ps =event_loop.check_pids()
			if 'mpv' in ps:
				pass
			elif 'mpv' not in ps and not playlist:
				pass
			elif 'mpv' not in ps and len(playlist) != 0 and len(autoplay) != 0:
				pass
			elif 'mpv' not in ps and len(playlist) != 0 and len(autoplay) == 0:
				os.system(f'mpv {mode[0]}  {playlist[0]}')
				playlist.pop(0)
				playlist_.pop(0)
				#changed sudo mpv to mpv to fix headphone problem
					

class wildcard_nav():
	def __init__(self,comm,file,origpath):
		self.file = file
		comm=[x for x in comm.split('/') if x != '']
		self.temp=''
		for i in comm:
			self.main_loop(i,origpath)
	def main_loop(self,i,origpath):
		x =Search.wildcard(i,self.file)
		if len(x) == 1:
			try:
				self.found(x)
			except:
				self.error('No such path',origpath)
		elif len(x) > 1:
			Font.info(x)
			self.error('Too many arguments',origpath)
		else:
			self.error('No such path',origpath)
	def found(self,x):
		
		if self.temp == '':
			os.chdir(x[0])
			self.temp=x[0]
		else:
			os.chdir(x[0])
			self.temp = f'{self.temp}/{x[0]}'
		self.file = files.list_dir()
		self.res = self.temp
	def error(self,msg,origpath):
		Font().warning(msg)
		self.res = ''
		os.chdir(origpath)

class Search():
	@staticmethod
	def wildcard(comm,file):
		if comm.count('*') > 2 or not comm.startswith('*') and not comm.endswith('*'):
			res_=comm.split('*')
			res = []
			for part in res_:
				matches=[x for x in file if part in x]
				if len(res) == 0:
					res = matches
				else:
					res = [x for x in res if x in matches]
		elif comm.startswith('*') and comm.endswith('*'):
			res=[x for x in file if comm.split('*')[1] in x]
		elif comm.endswith('*') and not comm.startswith('*'):
			res=[x for x in file if comm.split('*')[0] in x]
		elif comm.startswith('*') and not comm.endswith('*'):
			res=[x for x in file if comm.split('*')[1] in x]
		else:
			res = ''
			Font().warning('No such path')
		return(res)
class Nav:
	@staticmethod
	def pwd():
		return(os.getcwd())
	@staticmethod
	def isdir(comm,file):
		os.chdir(comm)
		Font.path(os.getcwd())
		file = files.list_dir()
		return(file)
	@staticmethod
	def wildcard(comm,file):
		origpath = os.getcwd()	
		if '/' not in comm:
			res = Search().wildcard(comm,file)
		elif '/' in comm:
			res = wildcard_nav(comm,file,origpath)
			res = res.res
		if len(res) == 1:
			os.chdir(res[0])
			Font.path(os.getcwd())
		elif len(res) > 1:
			Font.path(res)
			
	@staticmethod
	def back():
		path = os.getcwd().rsplit('/',1)[0]
		os.chdir(path)
		Font().path(os.getcwd())
	@staticmethod
	def home(home):
		Font().path(home)
		os.chdir(home)
	@staticmethod
	def isfile():
		pass

class files:
	@staticmethod			
	def list_dir():
		x = [x for x in os.listdir(os.getcwd()) if not x.startswith('.')]
		return(x)
	@staticmethod			
	def list_abspath(dir):
		if os.path.exists(dir):
			if dir != os.getcwd():
				dir=os.path.join(os.getcwd(),dir)
			elif dir == os.getcwd():
				dir = os.getcwd()
			x = {os.path.join(dir,x) for x in os.listdir(dir) if not x.startswith('.')}
			sorted_f=files().sort_files(x)
			return(sorted_f)
		elif not os.path.exists(dir):
			Font.warning('Directory not found')
	@staticmethod
	def sort_files(files_):
		videoext = ('mp4','avi')
		audioext = ('mp3','flac')
		videoext=tuple([x.lower() for x in 'mkv,mp4,m4a,m4v,f4v,f4a,m4b,m4r,f4b,mov,3gp,3gp2,3g2,3gpp,3gpp2,ogg,oga,ogv,ogx,wmv,wma,asf*,webm,flv,AVI*,OP1a,OP-Atom,ts,WAV,LXF,GXF* ,VOB*,avi'.split(',')])
		audioext=tuple([x.lower() for x in 'MP3,AAC,HE-AAC,AC3,EAC3,Vorbis,WMA,PCM,WEBVTT,DFXP,SAMI,SCC,SRT,TTML,3GPP,flac,wav,opus'.split(',')])
		folders = {f"{file.rsplit('/',1)[1]}" for file in files_ if os.path.isdir(file)}
		audiofiles = {f"{file.rsplit('/',1)[1]}" for file in files_ if os.path.isfile(file) and 
		file.endswith(audioext)}
		videofiles = {f"{file.rsplit('/',1)[1]}" for file in files_ if os.path.isfile(file) and 
		 file.endswith(videoext)} 
		files_ = {f"{file.rsplit('/',1)[1]}" for file in files_} 
		contentfiles = videofiles|audiofiles
		otherfiles = folders|contentfiles
		otherfiles = files_-otherfiles
		return(list(audiofiles),list(folders),list(otherfiles),list(videofiles))
	@staticmethod
	def add_color(obj,color,path,bg='',content=None):
		string = ''
		obj = list(obj)
		if content is None:
			for i in obj:
				if len(f'{string},{i}') >= 108:
					end = ' '
					i = f'\n{i}'
					string=''
				else:
					end = ', '
				if bg != '':
					text = colored(i, color,bg)
				else:
					text=colored(i, color,)
				print(text,end=end)
				string = f'{string},{i}'
		elif content == 'audio':
			for n,i in enumerate(obj):
				text = colored(i, color,bg)
				print(f'A|{n}\t',text)
		elif content == 'video':
			for n,i in enumerate(obj):
				text = colored(i, color,bg)
				print(f'V|{n}\t',text)
		return([[x,os.path.join(path,x)] for x in obj])
class Font:
	@staticmethod
	def warning(text):
		print(colored(text,'red','on_white',attrs=['bold']))
	@staticmethod
	def info(text):
		print(colored(text,'yellow',attrs=['bold']))
	@staticmethod
	def path(text):
		print(colored(text,'red',attrs=['bold']))
	def playlist(n,text):
		print(colored(n,'red',attrs=['bold']),end=' ')
		print(colored(text,'red', 'on_cyan',attrs=['bold']))
	@staticmethod
	def dev(n,text):
		print(colored(n,'red',attrs=['bold']),end=' ')
		print(colored(text,'magenta', 'on_white',attrs=['bold']))

class Bluetooth:
	@staticmethod
	def disconnect():
		disconnect=subprocess.check_output(['bluetoothctl','disconnect']).decode('utf+8')
		if 'Connected: no' in disconnect:
			Font().warning(f'disonnected bluetooth device')
		elif 'Connected: no' not in disconnect:
			Font().warning(f'Could not disconnected bluetooth device')

		

class youtubeSearch():
	def __init__(self,line):
		query=f"https://www.youtube.com/results?search_query={line}"
		
		self.d = Firefox(options=options)
		self.d.get(query)
	def scroll(self):
		while(True):
			height = self.d.execute_script("return document.body.scrollHeight")
			time.sleep(1)
			self.d.find_element_by_tag_name('body').send_keys(common.keys.Keys.END)
			if int(height)==0:
				break
	def get_results(self):
		#need to pass it the page source again
		data={}		
		channels,songs=[],[]
		x=self.d.find_elements_by_tag_name('a')
		y=self.d.find_elements_by_id('channel-info')
		for i in y:
			channels.append(i.text)
		for i in x:
			if i.get_attribute('id') == 'video-title':
				text=i.text,
				song=i.get_attribute('href')
				songs.append([text,song])
		for i,j in zip(songs,channels):
			data[i[0][0]]=[i[1],j]		
		return(data)
	def next_res(self):
		self.scroll()
		return(self.get_results())
		
	def quit(self):
		self.d.quit()

class CmdParse(cmd.Cmd):
	prompt = 'COMMAND >> '
	ruler = '-'
	
	def __init__(self):
		super().__init__()		
		self.file = files.list_dir()
		if hasattr(self,'audio') == False:
			self.audio = []
		if hasattr(self,'video') == False:
			self.video = []
		self.folders = []
		global content
		
		
	def do_search(self,line=''):
		'''search {video}, searches a video from youtube and returns a list that can be added using / type more for more results'''
		self.video=[]
		self.youtube=youtubeSearch(line)
		res=self.youtube.get_results()
		for n,i in enumerate(res.items()):
			if int(n) % 2 == 0:
				color = 'blue'
			else:
				color = 'cyan'
			print(
			colored(n,'red',attrs=['bold']),
			colored(i[0],color,attrs=['bold']),
			colored(i[1][1],color,attrs=['bold']),sep='\t')
			self.video.append([i[0],i[1][0]])
	def do_more(self,line):
		'''loads more search results, takes no arguments, only works if search has been initiated'''
		try:
			self.video=[]
			res=self.youtube.next_res()
			for n,i in enumerate(res.items()):
				if int(n) % 2 == 0:
					color = 'blue'
				else:
					color = 'cyan'
				print(
				colored(n,'red',attrs=['bold']),
				colored(i[0],color,attrs=['bold']),
				colored(i[1][1],color,attrs=['bold']),sep='\t')
				self.video.append([i[0],i[1][0]])
		except:
			print("No search query given, please use the search function")	
	def emptyline(self):
		if self.lastcmd:
			self.lastcmd = ""
			return self.onecmd('\n')
	def do_cd(self,comm):
		'''CHANGE DIR'''
		if os.path.exists(comm) and os.path.isdir(comm):
			self.file=Nav().isdir(comm,self.file)
		elif '*' in comm:
			Nav.wildcard(comm,self.file)
		elif comm == '..':
			Nav().back()
		elif comm == '~':
			Nav.home(home)
	def do_ls(self,line):
		'''LIST DIR, -m: media,-v:videos,-a:audio,-d:dir'''
		if line == '':
			content=files().list_abspath(os.getcwd())
			self.folders=files().add_color(content[1],'green',os.getcwd())
			other=files().add_color(content[2],'yellow',os.getcwd())
			self.audio=files().add_color(content[0],'magenta',os.getcwd(),'on_white')
			self.video=files().add_color(content[3],'red',os.getcwd(),'on_white')
		elif len(line.split()) == 1:
			if line == '-m':
				content=files().list_abspath(os.getcwd())
				if len(content[0]) == 0 and len(content[3]) == 0:
					Font().warning('--empty directory/Type file not found--')
				else:
					self.audio=files().add_color(content[0],'magenta',
					os.getcwd(),'on_white','audio')
					self.video=files().add_color(content[3],'red',os.getcwd(),'on_white','video')
			elif line == '-v':
				content=files().list_abspath(os.getcwd())
				if len(content[3]) == 0:
					Font().warning('--empty directory/Type file not found--')
				else:
					self.video=files().add_color(content[3],'red',os.getcwd(),'on_white','video')
			elif line == '-a':
				content=files().list_abspath(os.getcwd())
				if len(content[0]) == 0:
					Font().warning('--empty directory/Type file not found--')
				else:
					self.audio=files().add_color(content[0],
					'magenta',os.getcwd(),'on_white','audio')
			elif line == '-d':
				content=files().list_abspath(os.getcwd())
				if len(content[1]) == 0:
					Font().warning('--empty directory/Type file not found--')
				else:
					self.folders=files().add_color(content[1],'green',os.getcwd())
			else:
				content=files().list_abspath(line)
				if line == os.getcwd():
					line = os.getcwd()
				elif line != os.getcwd():
					line=os.path.join(os.getcwd(),line)
				self.folders=files().add_color(content[1],'green',line)
				other=files().add_color(content[2],'yellow',line)
				self.audio=files().add_color(content[0],'magenta',line,'on_white')
				self.video=files().add_color(content[3],'red',line,'on_white')
		elif len(line.split()) == 2:
			comm = line.split()[0]
			line = line.split()[1]
			content=files().list_abspath(line)
			if line == os.getcwd():
					line = os.getcwd()
			elif line != os.getcwd():
					line=os.path.join(os.getcwd(),line)
			if comm == '-m':
				if len(content[0]) == 0 and len(content[3]) == 0:
					Font().warning('--empty directory/Type file not found--')
				else:
					self.audio=files().add_color(content[0],'magenta',line,'on_white','audio')
					self.video=files().add_color(content[3],'red',line,'on_white','video')
			elif comm == '-v':
				if len(content[3]) == 0:
					Font().warning('--empty directory/Type file not found--')
				else:
					self.video=files().add_color(content[3],'red',line,'on_white','video')
			elif comm == '-a':
				if len(content[0]) == 0:
					Font().warning('--empty directory/Type file not found--')
				else:
					self.audio=files().add_color(content[0],'magenta',line,'on_white','audio')
			elif comm == '-d':
				if len(content[1]) == 0:
					Font().warning('--empty directory/Type file not found--')
				else:
					self.folders=files().add_color(content[1],'green',line)	
		print('\n')
		'''
		if len(line.split(' ')) > 1:
			print(line)
			if line.split(' ')[1].startswith('-'):
				folders=files().add_color(folders,'green')
				audio=files().add_color(audiofiles,'green','on_white')
				video=files().add_color(videofiles,'green','on_cyan')
				files().add_color(otherfiles,'yellow') 
		'''
	def do_pwd(self,line):
		'''CURRENT WORKING DIRECTORY'''
		Font().path(Nav().pwd())
	def do_clear(self,line):
		'''Clear playlist'''
		try:
			if len(playlist) >= 1:
				while len(playlist) != 0:
					playlist.pop(0)
					playlist_.pop(0)
		except:
			pass
	def do_vp(self,line):
		'''view playlist, use "vp top" to view the playlist reversed, use link playlist_number(without vp) to view link of an item in the playlist, use playlist_number(without vp) to view playlist track name of that number'''
		if len(playlist_) >= 1 and not line:
			n=0
			for i in playlist_:
				print(colored(n,'red',attrs=['bold']),end=' ')
				print(colored(i,'red', 'on_cyan',attrs=['bold']))
				n=n+1
		elif len(playlist_) >=1 and line.lower().startswith('top'):
			n=len(playlist_)-1
			for i in reversed(playlist_):
				print(colored(n,'red',attrs=['bold']),end=' ')
				print(colored(i,'red', 'on_cyan',attrs=['bold']))
				n=n-1			
	def do_playlists(self,line):
		'''view playlists'''
		if not os.path.exists(config):
			os.mkdir(config)
		lists = [x.replace('.playlist','') for x in os.listdir(config) if x.endswith('playlist')]
		for i in lists:
			print(f'\t{i}')
		
	def do_delete(self,line):
		'''delete playlist || delete playlistname (name all deletes all playlists'''
		if os.path.exists(f'{config}/{line}.playlist') or line == 'all':
			delete = input(f'Are you sure that you want to delete {line}? ')
			if delete.lower() == 'yes' or delete.lower() == 'y' and line.lower() != 'all':
				os.remove(f'{config}/{line}.playlist')
				Font().warning(f'playlist {line} deleted')
			elif delete.lower() == 'yes' or delete.lower() == 'y' and line.lower() == 'all':
				for i in os.listdir(f'{config}'):
					if i.endswith('playlist'):
						i = f'{config}/{i}'
						os.remove(i)
						Font().warning(f'playlist {i} deleted')
			else:
				Font().warning(f'playlist {line} not deleted')
		else:
			Font().warning(f'playlist {line} doesnt exist')
	def do_load(self,line):
		'''load playlist || load playlistname, to shuffle on open use playlistname.shuffle'''
		if line.endswith('.shuffle'):
			random_=True
			line = line.rsplit('.',1)[0]
			file = f'{config}/{line}.playlist'
		else:
			random_=False
			file = f'{config}/{line}.playlist'
		
		if os.path.exists(file):
			data = [x for x in open(file)]
			if random_==True:
				random.shuffle(data)
			for i in data:
				if '||' in i:
					i = i.rstrip().split('||')
					playlist_.append(i[0])
					playlist.append(i[1])
			Font.warning(f'Playlist {line} loaded')
		elif not os.path.exists(file):
			Font.warning(f'Playlist {line} doesnt exist')
	def do_set(self,line):
		'''set mode, internal=on computer, external=on external display, leave empty to view settings, internal.new for new comp to get smaller display'''
		if line == 'internal':
			mode[0] = '--on-all-workspaces --ontop  --fs=no --geometry=400x300-0+0 --no-terminal'
		elif line == 'external':
			mode[0] = '--no-config --on-all-workspaces --ontop  --player-operation-mode=pseudo-gui --fs --screen=1 --fs-screen=1'
		elif line == 'internal.new':
			mode[0] = '--on-all-workspaces --ontop  --fs=no --geometry=300x200-0+0 --no-terminal'
		elif line == 'internal.yulia':
			mode[0] = '--on-all-workspaces --ontop  --fscd =no --geometry=500x400-0+0 --no-terminal'
		elif line == 'external':
			mode[0] = '--no-config --on-all-workspaces --ontop  --player-operation-mode=pseudo-gui --fs --screen=1 --fs-screen=1'
		elif line == '':
			Font().warning(mode[0])
	def do_shuffle(self,line):
		'''shuffles playlist, takes no arguments'''
		playlistTemp = [x for x in zip(playlist,playlist_)]
		random.shuffle(playlistTemp)
		self.do_clear('')
		for x,y in playlistTemp:
			playlist.append(x)
			playlist_.append(y)
		Font.warning(f'Playlist shuffled')	
	def do_save(self,line):
		'''save playlist || save playlistname, save name|new (replace existing playlist), save name|add (add to existing playlist)'''
		count =0
		
		overwrite='yes'
		if '|' in line:
			print(line.split('|'))
			overwrite=line.split('|')[1]
			line = line.split('|')[0]
		file = f'{config}/{line}.playlist'
		if os.path.exists(file):
			Font().warning('Playlist exists')
			
			if overwrite.lower() == 'new':
				os.remove(file)
				os.mknod(file)
				file = open(file,'a')
			elif overwrite.lower() == 'add':
				file = open(file,'a')
			else:
				Font().warning('File not saved')
		else:
			os.mknod(file)
			file = open(file,'a')
		while count < len(playlist) and overwrite.lower() == 'yes' or overwrite.lower() =='y' or overwrite.lower() == 'new' or overwrite.lower() =='add':
			if count >= len(playlist):
				break;
			file.write(f'{playlist_[count]}||{playlist[count]}\n')
			count+=1
		if overwrite.lower() == 'yes' or overwrite.lower() == 'y':
			file.close()
			Font().warning(f'playlist {line} created')		
	def do_play(self,line):
		'''play'''
		autoplay.pop(0)
	def do_mv(self,line):
		'''mv (track number) (up,down,top,last) to move track number or move by index number "mv 13 1'''
		if len(line.split(' ')) > 1:
			line = line.split(' ')
			order = line[1]
			line = line[0]
			if line.isdigit() and not order.isdigit():
				if int(line) <= len(playlist) and order.lower() == 'top':
					playlist_.insert(0,playlist_[int(line)])
					playlist.insert(0,playlist[int(line)])
					playlist.pop(int(line)+1)
					playlist_.pop(int(line)+1)
				if int(line) <= len(playlist) and order.lower() == 'last':
					playlist_.insert(len(playlist_),playlist_[int(line)])
					playlist.insert(len(playlist),playlist[int(line)])
					playlist.pop(int(line))
					playlist_.pop(int(line))
				if int(line)+2 <= len(playlist) and order.lower() == 'down':
					playlist_.insert(int(line)+2,playlist_[int(line)])
					playlist.insert(int(line)+2,playlist[int(line)])
					playlist.pop(int(line))
					playlist_.pop(int(line))
				if int(line)-1 <= len(playlist) and order.lower() == 'up':
					playlist_.insert(int(line)-1,playlist_[int(line)])
					playlist.insert(int(line)-1,playlist[int(line)])
					playlist.pop(int(line)+1)
					playlist_.pop(int(line)+1)
			elif order.isdigit():
				if int(order) > len(playlist) or int(line) > len(playlist):
					print('Move command out of range')
				else:
					playlist_.insert(int(order),playlist_[int(line)])
					playlist.insert(int(order),playlist[int(line)])
					playlist.pop(int(line)+1)
					playlist_.pop(int(line)+1)
	def do_download(self,line):
		'''download link|playlist_number|current_playlist (--video=True --path=/save/path/ & amperstand is for detach)optional arguments, current_playlist=downloads current playlist'''
		command=line
		line = line.split(" ")
		video=''
		detach=''
		if line[0].startswith('http'):
			link=line[0]
		elif line[0].isdigit():
			link=playlist[int(line[0])]
		elif line[0].lower() == 'current_playlist':
			link = [x for x in playlist]
		
		if line[0].lower() == 'current_playlist' and '--path' not in command:
			folder=datetime.datetime.now().strftime("%d%b%Y-%H%M%S")
			os.mkdir(f'{download_dir}/{folder}')
			path=f"'{download_dir}/{folder}/%(title)s.%(ext)s'"
		elif line[0].lower() == 'current_playlist' and '--path' in command:
			folder=datetime.datetime.now().strftime("%d%b%Y-%H%M%S")
			path=''
		else:
			path=f"'{download_dir}/%(title)s.%(ext)s'"
		for i in line:
			if i.startswith('--path') and 'current_playlist' not in command:
				path=i.replace('--path=','')
				if os.path.exists(path):
					path = f"'{path}/%(title)s.%(ext)s'"
				elif os.path.exists(download_dir):
					path=f"'{download_dir}/%(title)s.%(ext)s'"
				else:
					path = f"'{os.getcwd()}/%(title)s.%(ext)s'"
					
			elif i.startswith('--path') and 'current_playlist' in command:
				print('here')
				path=i.replace('--path=','')
				if os.path.exists(path):
					path = f"'{path}/%(title)s.%(ext)s'"
				elif os.path.exists(download_dir):
					print('here')
					os.mkdir(f'{download_dir}/{folder}')
					path=f"'{download_dir}/{folder}/%(title)s.%(ext)s'"
					print('here')
				else:
					os.mkdir(f'{download_dir}/{folder}')
					path = f"'{os.getcwd()}/{folder}/%(title)s.%(ext)s'"
				
		
			if i.startswith('--video'):
				video=i.replace('--video=','')
				if video=="True" or video=="true":
					video='-x'
				else:
					video=""
					
			if i.endswith('&') and not isinstance(link,list):
				detach='mate-terminal -e'
				comm=f'{detach} "youtube-dl {video} -o {path} {link}"'
			elif not i.endswith('&') and not isinstance(link,list):
				comm=f'{detach} youtube-dl {video} -o {path} {link}'
			elif i.endswith('&') and isinstance(link,list):
				detach='mate-terminal -e'
				comm=f'{detach} "youtube-dl {video} -o {path}"'
			elif not i.endswith('&') and  isinstance(link,list):
				comm=f'{detach} youtube-dl {video} -o {path}'
		
		if isinstance(link,list):
			for i in link:
				os.system(f'{comm} {i}')
		elif not isinstance(link,list):
			os.system(comm)
		
	def do_pause(self,line):
		'''pause'''
		autoplay.append('no')
	def do_stop(self,line):
		'''stops mpv and clears playlist'''
		while len(playlist) != 0:																						
			playlist.pop(0)
			playlist_.pop(0)
		os.system('killall mpv')
	def do_next(self,line):
		'''stops mpv and plays next item'''
		os.system('killall mpv')
	def do_connect(self,line):
		'''connect to bluetooth device, connect devicename or leave devicename blank for to specify from a list'''
		try:
			Bluetooth.disconnect()
		except:
			pass
		Font().warning('Scanning for specified device name')
		dev =  str(subprocess.check_output(['hcitool','scan']).decode('utf+8')).replace("Scanning ...\n\t","")
		dev =[x.split('\t') for x in dev.split('\n\t')]
		devices = {}
		dev_=[]
		if line == '':
			for n,i in enumerate(dev):
				name = i[1].rstrip()
				Font().dev(n,name)
				dev_.append(name)
			n = input('Connect to: ')
			if n.isdigit():
				print(int(n))
				if int(n)<len(dev_):
					line = dev_[int(n)]
		for i in dev:
			name = i[1].rstrip()
			mac = i[0].rstrip()
			devices[name] = mac
		dev_id=''
		for name,mac in devices.items():
			if line.lower() == name.lower():
				dev_id=mac
				Font().warning(f'Found {line}')
		if dev_id == '':
			Font().warning(f'{line} not a valid device')
		elif dev_id != '':
			try:
				connect=subprocess.check_output(['bluetoothctl','connect',dev_id]).decode('utf+8')
				if 'Connection successful\n' in connect:
					Font().warning(f'Connected to {line}')
				elif 'Connection successful\n' not in connect:
					Font().warning(f'Could not connected to {line}')
			except:
				Font().warning(f'Could not connected to {line}')
	def do_update(self,line):
		'''view updated info'''
		old =["Append old updates to this list"]
		old+=["Last updated on the 15th of October","Added function in default to view playlist_track name or playlist track", "Added functionality to vp to view the playlist in reverse","----------------------------------------------"]
		new=['Last updated 15th of October','Added do_favourite and do_later to add items to favourites and watch later','Added function do_add_to to create and append to playlists or append to existing playlists items from the currently load playlist',
		'----------------------------------------']
		
		for i in old:
			if not i.startswith('---'):
				Font().path(i)
			else:
				print('\n',i)
			
		for i in new:
			if not i.startswith('---'):
				Font().info(i)
			else:
				print('\n',i)
	def do_disconnect(self,line):
		'''disconnect bluetooth device'''
		try:
			Bluetooth.disconnect()
		except:
			Font().warning(f'Could not disconnected bluetooth device')
	def do_scan(self,line):
		'''scans for nearby bluetooth devices'''
		Font().warning('Scanning for bluetooth devices')
		dev =  str(subprocess.check_output(['hcitool','scan']).decode('utf+8')).replace("Scanning ...\n\t","")
		dev =[x.split('\t') for x in dev.split('\n\t')]
		
		for i in dev:
			name = i[1].rstrip()
			mac = i[0].rstrip()
			print(f'{name} || {mac}')
	def do_execute(self,line):
		'''execute terminal command'''
		line = line.split(' ')
		line = subprocess.check_output(line).decode('utf+8')
		print(line)
	def do_emptyline(self,line):
		pass
	def do_quit(self,line):
		'''quit program'''
		os.system('killall python3')
	def do_add(self,line):
		'''can add file with d:dir, A:audio file, V:videofile,path with *,A|Vstart-stop&|step for range, or a link starting with http://, if searched from youtube can use /1 or /1,2,3 or /1,1-6-2,34 for range start,stop and step can be left blank
		To add url either type url or url name
		
		add omitted use ls or search''' 
		pass
	def do_places(self,line):
		'''add favourite places to easily traverse too\n--view view save places
		\n--clear clears saved places\n--add name path, add places\nname, traverse to place'''
		if not os.path.exists(config):
			os.mkdir(config)
		if not os.path.exists(f'{config}/config'):
			os.mknod(f'{config}/config')
		if '--add' in line:
			line=line.replace('--add','').split(' ')
			name = line[1]
			line = line[2]
			if os.path.isdir(line):
				f=open(f'{config}/config','a')
				f.write(f'{name}|{line}\n')
				Font.warning(f'added place {name}|{line}')
			else:
				Font.warning(f'place {name}|{line} not found')
		elif '--view' in line:
			plc = {}
			pl=[x.rstrip() for x in open(f'{config}/config')]
			for i in pl:
				i=i.split('|',1)
				plc[i[0]] = i[1]
			for j,k in plc.items():
				print(f'{j}\t\t{k}')
		elif '--clear' in line:
			os.remove(f'{config}/config')
			os.mknod(f'{config}/config')
			Font.warning(f'cleared favourite places')
		else:
			plc = {}
			pl=[x.rstrip() for x in open(f'{config}/config')]
			for i in pl:
				i=i.split('|',1)
				plc[i[0]] = i[1]
			if line in plc.keys():
				os.chdir(plc[line])
				Font.path(f'{plc[line]}')
				
			elif line not in plc.keys():
				Font.warning(f'{line} doesnt exist in places')
	def do_del(self,line):
		'''delete items from playlist using\n \t\ta list 1,2,3,4\n \t\ta range start-stop-step\n'''
		#playlist.sort(),playlist_.sort()
		if all(i.isdigit() for i in line.split(',')): 
			line=line.split(',')
			line = [[playlist[int(i)],playlist_[int(i)]] for i in line]
			for i in line:
				name = i[1]
				a=playlist.index(i[0])
				b=playlist_.index(i[1])
				del(playlist[a])
				del(playlist_[b])
				Font.warning(f'deleted {name}')
		if '-' in line:
			length=len(line.split('-'))
			filerange=[]
			if length == 2:
				start,stop = tuple(line.split('-'))
				if start == ' ' or start =='':
					start=0
				if stop == ' ' or stop=='' or not stop.isdigit():
					stop = len(playlist)
				filerange=playlist_[int(start):int(stop)+1]
				del(playlist[int(start):int(stop)+1])
				del(playlist_[int(start):int(stop)+1])
			if length == 3:
				start,stop,step = tuple(line.split('-'))
				if start == ' ' or start =='':
					start=0
				if stop == ' ' or stop=='' or not stop.isdigit():
					stop = len(playlist)
				filerange=playlist_[int(start):int(stop)+1:int(step)]
				del(playlist[int(start):int(stop)+1:int(step)])
				del(playlist_[int(start):int(stop)+1:int(step)])
			for i in filerange:
				Font.warning(f'deleted {i}')
		'''
		for n,i in enumerate(line):
			i=int(i)
			print(f'removed {playlist[i]}')
			del(playlist[i])
			del(playlist_[i])'''
		#playlist.sort(reverse=True),playlist_.sort(reverse=True)
	def do_favourite(self,line):
		'''favourite playlist_number adds file to favourites'''
		if line.isdigit():
			line=int(line)
			
			if not os.path.exists(f'{config}/favourites.playlist'):
				os.system(f'touch {config}/favourites.playlist')
			p = open(f'{config}/favourites.playlist','a')
			p.write(f'{playlist_[line]}||{playlist[line]}\n')
			Font().info(f'Added {playlist_[line]} to favourites')

	def do_later(self,line):
		'''later playlist_number adds file to watch_later playlist'''
		if line.isdigit():
			line=int(line)
			
			if not os.path.exists(f'{config}/watch_later.playlist'):
				os.system(f'touch {config}/watch_later.playlist')
			p = open(f'{config}/watch_later.playlist','a')
			p.write(f'{playlist_[line]}||{playlist[line]}\n')
			Font().info(f'Added {playlist_[line]} to watch_later')
	def do_add_to(self,line):
		'''"add_to playlist track_number" to add to a playlist which exists\n
		"add_to playlist track_number create" to create a playlist and add_to it'''
		if not line.endswith('create'):
			_Playlist,n = line.split(" ")
			print(int(n))
			if not os.path.exists(f'{config}/{_Playlist}.playlist'):
				Font().info("Playlist Not Found")
			else:
				p=open(f'{config}/{_Playlist}.playlist','a')
				p.write(f'{playlist_[int(n)]}||{playlist[int(n)]}\n')
				Font().info(f"Added {playlist_[int(n)]} to {_Playlist}")		
		else:
			_Playlist,n,x = line.split(" ")
			if not os.path.exists(f'{config}/{_Playlist}.playlist'):
				os.system(f'touch {config}/{_Playlist}.playlist')
				Font().info(f"Playlist {_Playlist} created")
				p = open(f'{config}/{_Playlist}.playlist','a')
				p.write(f'{playlist_[int(n)]}||{playlist[int(n)]}\n')
				Font().info(f"Added {playlist_[int(n)]} to {_Playlist}")
			elif os.path.exists(f'{config}/{_Playlist}.playlist'):
				Font().info(f"{_Playlist} exists ABORTING")
			
	def default(self,line):
		'''can add file with d:dir, A:audio file, V:videofile,path with *,A|Vstart-stop&|step for range, or a link starting with http://, if searched from youtube can use /1 or /1,2,3 or /1,1-6-2,34 for range start,stop and step can be left blank
		To add url either type url or url name''' 
		line = line.split(',')
		for i in line:
			orig = i
			if i.startswith('http') and len(i.split(' ')) == 1:
				playlist.append(i)
				playlist_.append(i)
			if i.startswith('http') and len(i.split(' ')) > 1:
				playlist.append(i.split(' ')[0])
				playlist_.append(i.split(' ',1)[1])
			i=i.lower()
			if i.startswith('/'):
				if i.replace('/','').isdigit() and len(line) == 1 and all('-' not in x for x in line):
					index=int(i.replace('/',''))
					playlist.append(f'"{self.video[index][1]}"')
					playlist_.append(f'"{self.video[index][0]}"')
				
				elif i.startswith('/') and len(line) >1 and all('-' not in x for x in line):
					line[0]=int(i.replace('/',''))
					for tracks in line:
						index = int(tracks)
						playlist.append(f'"{self.video[index][1]}"')
						playlist_.append(f'"{self.video[index][0]}"')
				elif '-' in i and len(line) == 1:
					range_=i.replace('/','').split('-')
					if len(range_) == 3:
						start,stop,step = range_
						if start == '':
							start = 0
						else:
							start = int(start)
						if stop == '':
							stop = int(len(self.video))
						else:
							stop = int(stop)
						if step == '':
							step = 1
						else:
							step = int(step)
					elif len(range_) == 2:
						start,stop = range_
						if start == '':
							start = 0
						else:
							start = int(start)
						if stop == '':
							stop = int(len(self.video))
						else:
							stop = int(stop)
						step = 1
					else:
						start,stop,step = 0,len(self.video),1
					selection = self.video[start:stop:step]
					for i in selection:
						playlist.append(f'"{i[1]}"')
						playlist_.append(f'"{i[0]}"')
				elif any('-' in x for x in line) and len(line) > 1:
					line[0]=line[0].replace('/','')
					for i in line:
						if '-' not in i:
							
							playlist.append(f'"{self.video[int(i)][1]}"')
							playlist_.append(f'"{self.video[int(i)][0]}"')
							
						elif '-' in i:
							range_=i.split('-')
							if len(range_) == 3:
								start,stop,step = range_
								if start == '':
									start = 0
								else:
									start = int(start)
								if stop == '':
									stop = int(len(self.video))
								else:
									stop = int(stop)
								if step == '':
									step = 1
								else:
									step = int(step)
							elif len(range_) == 2:
								start,stop = range_
								if start == '':
									start = 0
								else:
									start = int(start)
								if stop == '':
									stop = int(len(self.video))
								else:
									stop = int(stop)
									step = 1
							else:
								start,stop,step = 0,len(self.video),1
							selection = self.video[start:stop:step]
							for i in selection:
								playlist.append(f'"{i[1]}"')
								playlist_.append(f'"{i[0]}"')
							
					
			if i.startswith('a'):
				if i.replace('a','').isdigit():
					index=int(i.replace('a',''))
					playlist.append(f'"{self.audio[index][1]}"')
					playlist_.append(f'"{self.audio[index][0]}"')
				if '-' in i:
					length=len(i.split('-'))
					if length == 2:
						start,stop = tuple(i.replace('a','').split('-'))
						if start == ' ' or start =='':
							start=0
						if stop == ' ' or stop=='' or not stop.isdigit():
							stop = len(self.audio)
						filerange=self.audio[int(start):int(stop)+1]
					if length == 3:
						start,stop,step = tuple(i.replace('a','').split('-'))
						if start == ' ' or start =='':
							start=0
						if stop == ' ' or stop=='' or not stop.isdigit():
							stop = len(self.audio)
						filerange=self.audio[int(start):int(stop)+1:int(step)]
				else:
					filerange=[]
					
				#for item in reversed(filerange):
				for item in filerange:
					playlist.append(f'"{item[1]}"')
					playlist_.append(f'"{item[0]}"')
			if i.startswith('v'):
				if i.replace('v','').isdigit():
					index=int(i.replace('v',''))
					playlist.append(f'"{self.video[index][1]}"')
					playlist_.append(f'"{self.video[index][0]}"')
				if '-' in i:
					length=len(i.split('-'))
					if length == 2:
						start,stop = tuple(i.replace('v','').split('-'))
						if start == ' ' or start =='':
							start=0
						if stop == ' ' or stop=='' or not stop.isdigit():
							stop = len(self.video)
						filerange=self.video[int(start):int(stop)+1]
					if length == 3:
						start,stop,step = tuple(i.replace('v','').split('-'))
						if start == ' ' or start =='':
							start=0
						if stop == ' ' or stop=='' or not stop.isdigit():
							stop = len(self.video)
						filerange=self.video[int(start):int(stop)+1:int(step)]
				else:
					filerange=[]
					
				#for item in reversed(filerange):
				for item in filerange:
					playlist.append(f'"{item[1]}"')
					playlist_.append(f'"{item[0]}"')
			if i.startswith('d:'):
				folder=i.replace('d:','')
				dummy=[[x[0].lower(),x[1]] for x in self.folders]
				for i in dummy:
					if i[0] == folder:
						content=files().list_abspath(i[1])
						self.audio=files().add_color(content[0],
						'magenta',i[1],'on_white','audio')
						self.video=files().add_color(content[3],
						'red',i[1],'on_white','video')
						for item in self.audio:
							playlist.append(f'"{item[1]}"')
							playlist_.append(f'"{item[0]}"')
						for item in self.video:
							playlist.append(f'"{item[1]}"')
							playlist_.append(f'"{item[0]}"')
						
			if '*' in i:		
				print(i)
				dummy=[x[0].lower() for x in self.video]
				dummy.extend([x[0].lower() for x in self.audio])
				s=Search.wildcard(i,dummy)
				for i in s:
					for m in self.audio:
						if i == m[0].lower():
							playlist.append(f'"{m[1]}"')
							playlist_.append(f'"{m[0]}"')
					for m in self.video:
						if i == m[0]:
							playlist.append(f'"{m[1]}"')
							playlist_.append(f'"{m[0]}"')
			if i in [x[0].lower() for x in self.audio]:
				for items in self.audio:
					name=items[0]
					data=items[1]
					if i == name.lower():
						playlist.append(f'"{data}"')
						playlist_.append(f'"{name}"')
			if i in [x[0].lower() for x in self.video]:
				for items in self.video:
					name=items[0]
					data=items[1]
					if i == name.lower():
						playlist.append(f'"{data}"')
						playlist_.append(f'"{name}"')
			#playlist.sort(reverse=True)
			#playlist_.sort(reverse=True)
			if i.isdigit():
				'''prints a number from the playlist'''
				Font().info(playlist_[int(i)])			
			if i.lower().startswith('link'):
				'''prints the link from a number in a playlist'''
				Font().info(playlist[int(i.split(' ')[1])])		
	
try:
	print(colored('TYPE SOME COMMANDS TO USE YOUR TERMINAL MEDIAPLAYER, TYPE HELP FOR OPTIONS ','red', 'on_cyan',attrs=['bold']))
	p1 = threading.Thread(target=event_loop().main_event_loop)
	p2 = threading.Thread(target=CmdParse().cmdloop)
	p1.start()
	p2.start()
except:
	pass
