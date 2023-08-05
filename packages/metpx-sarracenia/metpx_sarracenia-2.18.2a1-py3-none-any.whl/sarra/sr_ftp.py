#!/usr/bin/env python3
#
# This file is part of sarracenia.
# The sarracenia suite is Free and is proudly provided by the Government of Canada
# Copyright (C) Her Majesty The Queen in Right of Canada, Environment Canada, 2008-2015
#
# Questions or bugs report: dps-client@ec.gc.ca
# sarracenia repository: git://git.code.sf.net/p/metpx/git
# Documentation: http://metpx.sourceforge.net/#SarraDocumentation
#
# sr_ftp.py : python3 utility tools for ftp usage in sarracenia
#             Since python3.2 supports ftps (RFC 4217)
#             I tested it and works for all our ftps pull/sender as of today
#
# Code contributed by:
#  Michel Grenier - Shared Services Canada
#  Last Changed   : Nov 23 21:12:24 UTC 2017
#
########################################################################
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, 
#  but WITHOUT ANY WARRANTY; without even the implied warranty of 
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
#

import ftplib,os,sys,time

try :
         from sr_util            import *
except :
         from sarra.sr_util      import *

#============================================================
# ftp protocol in sarracenia supports/uses :
#
# connect
# close
#
# if a source    : get    (remote,local)
#                  ls     ()
#                  cd     (dir)
#                  delete (path)
#
# if a sender    : put    (local,remote)
#                  cd     (dir)
#                  mkdir  (dir)
#                  umask  ()
#                  chmod  (perm)
#                  rename (old,new)
#
# FTP : no remote file seek... so 'I' part impossible
#

class sr_ftp(sr_proto):
    def __init__(self, parent) :
        parent.logger.debug("sr_ftp __init__")
        sr_proto.__init__(self,parent)
        # ftp command times out after 20 secs
        # this setting is different from the computed iotime (sr_proto)
        self.init()
 
    # cd
    def cd(self, path):
        self.logger.debug("sr_ftp cd %s" % path)

        alarm_set(self.iotime)
        self.ftp.cwd(self.originalDir)
        self.ftp.cwd(path)
        self.pwd = path
        alarm_cancel()

    def cd_forced(self,perm,path) :
        self.logger.debug("sr_ftp cd_forced %d %s" % (perm,path))

        # try to go directly to path

        alarm_set(self.iotime)
        self.ftp.cwd(self.originalDir)
        try   :
                self.ftp.cwd(path)
                alarm_cancel()
                return
        except: pass
        alarm_cancel()

        # need to create subdir

        subdirs = path.split("/")
        if path[0:1] == "/" : subdirs[0] = "/" + subdirs[0]

        for d in subdirs :
            if d == ''   : continue
            # try to go directly to subdir
            try   :
                    alarm_set(self.iotime)
                    self.ftp.cwd(d)
                    alarm_cancel()
                    continue
            except: pass

            # create
            alarm_set(self.iotime)
            self.ftp.mkd(d)
            alarm_cancel()

            # chmod
            alarm_set(self.iotime)
            self.ftp.voidcmd('SITE CHMOD ' + "{0:o}".format(perm) + ' ' + d)
            alarm_cancel()

            # cd
            alarm_set(self.iotime)
            self.ftp.cwd(d)
            alarm_cancel()

    # check_is_connected

    def check_is_connected(self):
        self.logger.debug("sr_ftp check_is_connected")

        if self.ftp == None  : return False
        if not self.connected : return False

        if self.destination != self.parent.destination :
           self.close()
           return False

        self.batch = self.batch + 1
        if self.batch > self.parent.batch :
           self.close()
           return False

        return True

    # chmod
    def chmod(self,perm,path):
        self.logger.debug("sr_ftp chmod %s %s" % (str(perm),path))
        alarm_set(self.iotime)
        self.ftp.voidcmd('SITE CHMOD ' + "{0:o}".format(perm) + ' ' + path)
        alarm_cancel()

    # close
    def close(self):
        self.logger.debug("sr_ftp close")

        old_ftp = self.ftp

        self.init()

        try:
                alarm_set(self.iotime)
                old_ftp.quit()
        except: pass
        alarm_cancel()

    # connect...
    def connect(self):
        self.logger.debug("sr_ftp connect %s" % self.parent.destination)

        self.connected   = False
        self.destination = self.parent.destination

        if not self.credentials() : return False


        # timeout alarm 100 secs to connect
        alarm_set(3*self.iotime)
        try:
                expire  = -999
                if self.parent.timeout : expire = self.parent.timeout
                if self.port == '' or self.port == None : self.port = 21

                if not self.tls :
                   ftp = ftplib.FTP()
                   ftp.connect(self.host,self.port,timeout=expire)
                   ftp.login(self.user, self.password)
                else :
                   # ftplib supports FTPS with TLS 
                   ftp = ftplib.FTP_TLS(self.host,self.user,self.password,timeout=expire)
                   if self.prot_p : ftp.prot_p()
                   # needed only if prot_p then set back to prot_c
                   #else          : ftp.prot_c()

                ftp.set_pasv(self.passive)

                self.originalDir = '.'

                try   : self.originalDir = ftp.pwd()
                except:
                        (stype, svalue, tb) = sys.exc_info()
                        self.logger.warning("Unable to ftp.pwd (Type: %s, Value: %s)" % (stype ,svalue))

                self.pwd = self.originalDir

                self.connected = True

                self.ftp = ftp

                alarm_cancel()
                return True

        except:
            (stype, svalue, tb) = sys.exc_info()
            self.logger.error("Unable to connect to %s (user:%s). Type: %s, Value: %s" % (self.host,self.user, stype,svalue))

        alarm_cancel()
        return False

    # credentials...
    def credentials(self):
        self.logger.debug("sr_ftp credentials %s" % self.destination)

        try:
                ok, details = self.parent.credentials.get(self.destination)
                if details  : url = details.url

                self.host     = url.hostname
                self.port     = url.port
                self.user     = url.username
                self.password = url.password

                self.passive  = details.passive
                self.binary   = details.binary
                self.tls      = details.tls
                self.prot_p   = details.prot_p

                return True

        except:
                (stype, svalue, tb) = sys.exc_info()
                self.logger.error("Unable to get credentials for %s" % self.destination)
                self.logger.error("sr_ftp/credentials (Type: %s, Value: %s)" % (stype ,svalue))

        return False

    # delete
    def delete(self, path):
        self.logger.debug( "sr_ftp rm %s" % path)
        alarm_set(self.iotime)
        # if delete does not work (file not found) run pwd to see if connection is ok
        try   : self.ftp.delete(path)
        except: d = self.ftp.pwd()
        alarm_cancel()

    # get
    def get(self, remote_file, local_file, remote_offset=0, local_offset=0, length=0, filesize=None):
        self.logger.debug( "sr_ftp get %s %s %d" % (remote_file,local_file,local_offset))

        # open local file
        dst = self.local_write_open(local_file, local_offset)

        # initialize sumalgo
        if self.sumalgo : self.sumalgo.set_path(remote_file)

        # download
        self.write_chunk_init(dst)
        if self.binary : self.ftp.retrbinary('RETR ' + remote_file, self.write_chunk, self.bufsize )
        else           : self.ftp.retrlines ('RETR ' + remote_file, self.write_chunk )
        rw_length = self.write_chunk_end()

        # close
        self.local_write_close(dst)


    # getcwd
    def getcwd(self):
        alarm_set(self.iotime)
        pwd = self.ftp.pwd()
        alarm_cancel()
        return pwd

    # init
    def init(self):
        self.logger.debug("sr_ftp init")
        sr_proto.init(self)

        self.connected   = False 
        self.ftp         = None
        self.details     = None

        self.batch       = 0

    # ls
    def ls(self):
        self.logger.debug("sr_ftp ls")
        self.entries = {}
        alarm_set(self.iotime)
        self.ftp.retrlines('LIST',self.line_callback )
        alarm_cancel()
        self.logger.debug("sr_ftp ls = %s" % self.entries )
        return self.entries

    # line_callback: entries[filename] = 'stripped_file_description'
    def line_callback(self,iline):
        self.logger.debug("sr_ftp line_callback %s" % iline)

        alarm_cancel()

        oline  = iline
        oline  = oline.strip('\n')
        oline  = oline.strip()
        oline  = oline.replace('\t',' ')
        opart1 = oline.split(' ')
        opart2 = []

        for p in opart1 :
            if p == ''  : continue
            opart2.append(p)

        fil  = opart2[-1]
        line = ' '.join(opart2)

        self.entries[fil] = line

        alarm_set(self.iotime)

    # mkdir
    def mkdir(self, remote_dir):
        self.logger.debug("sr_ftp mkdir %s" % remote_dir)
        alarm_set(self.iotime)
        self.ftp.mkd(remote_dir)
        alarm_cancel()
        alarm_set(self.iotime)
        self.ftp.voidcmd('SITE CHMOD ' + "{0:o}".format(self.parent.chmod_dir) + ' ' + remote_dir)
        alarm_cancel()

    # put
    def put(self, local_file, remote_file, local_offset=0, remote_offset=0, length=0, filesize=None):
        self.logger.debug("sr_ftp put %s %s" % (local_file,remote_file))

        # open 
        src = self.local_read_open(local_file, local_offset)

        # upload
        self.write_chunk_init(None)
        if self.binary : self.ftp.storbinary("STOR " + remote_file, src, self.bufsize, self.write_chunk)
        else           : self.ftp.storlines ("STOR " + remote_file, src, self.write_chunk)
        rw_length = self.write_chunk_end()

        # close 
        self.local_read_close(src)

    # rename
    def rename(self,remote_old,remote_new) :
        self.logger.debug("sr_ftp rename %s %s" % (remote_old,remote_new))
        alarm_set(self.iotime)
        self.ftp.rename(remote_old,remote_new)
        alarm_cancel()

    # rmdir
    def rmdir(self, path):
        self.logger.debug("sr_ftp rmdir %s" % path)
        alarm_set(self.iotime)
        self.ftp.rmd(path)
        alarm_cancel()

    # umask
    def umask(self) :
        self.logger.debug("sr_ftp umask")
        alarm_set(self.iotime)
        self.ftp.voidcmd('SITE UMASK 777')
        alarm_cancel()


#============================================================
#
# wrapping of downloads/sends using sr_ftp in ftp_transport
#
#============================================================

class ftp_transport(sr_transport):
    def __init__(self) :
        self.ftp   = None
        self.cdir  = None

    def close(self) :
        self.logger.debug("ftp_transport close")

        try    : self.ftp.close()
        except : pass

        self.ftp  = None
        self.cdir = None

    def download( self, parent ):
        self.logger = parent.logger
        self.parent = parent
        self.logger.debug("ftp_transport download")

        msg         = parent.msg
        token       = msg.relpath.split('/')
        cdir        = '/'.join(token[:-1])
        remote_file = token[-1]
        urlstr      = msg.baseurl + '/' + msg.relpath
        new_lock    = ''

        try:    curdir = os.getcwd()
        except: curdir = None

        if curdir != parent.new_dir:
           os.chdir(parent.new_dir)

        try :
                parent.destination = msg.baseurl

                ftp = self.ftp
                if ftp == None or not ftp.check_is_connected() :
                   self.logger.debug("ftp_transport download connects")
                   ftp = sr_ftp(parent)
                   ok = ftp.connect()
                   if not ok : return False
                   self.ftp  = ftp
                   self.cdir = None

                # for generalization purpose
                if not hasattr(ftp,'seek') and msg.partflg == 'i':
                   self.logger.error("ftp, inplace part file not supported")
                   msg.report_publish(499,'ftp does not support partitioned file transfers')
                   return False
                
                if self.cdir != cdir :
                   self.logger.debug("ftp_transport download cd to %s" %cdir)
                   ftp.cd(cdir)
                   self.cdir  = cdir
    
                remote_offset = 0
                if  msg.partflg == 'i': remote_offset = msg.offset
    
                str_range = ''
                if msg.partflg == 'i' :
                   str_range = 'bytes=%d-%d'%(remote_offset,remote_offset+msg.length-1)
    
                #download file
    
                msg.logger.debug('Beginning fetch of %s %s into %s %d-%d' % 
                    (urlstr,str_range,parent.new_file,msg.local_offset,msg.local_offset+msg.length-1))
    
                # FIXME  locking for i parts in temporary file ... should stay lock
                # and file_reassemble... take into account the locking

                ftp.set_sumalgo(msg.sumalgo)

                if parent.inflight == None or msg.partflg == 'i' :
                   ftp.get(remote_file,parent.new_file,remote_offset,msg.local_offset,msg.length,msg.filesize)

                elif parent.inflight == '.' :
                   new_lock = '.' + parent.new_file
                   ftp.get(remote_file,new_lock,remote_offset,msg.local_offset,msg.length,msg.filesize)
                   if os.path.isfile(parent.new_file) : os.remove(parent.new_file)
                   os.rename(new_lock, parent.new_file)
                      
                elif parent.inflight[0] == '.' :
                   new_lock  = parent.new_file + parent.inflight
                   ftp.get(remote_file,new_lock,remote_offset,msg.local_offset,msg.length,msg.filesize)
                   if os.path.isfile(parent.new_file) : os.remove(parent.new_file)
                   os.rename(new_lock, parent.new_file)

                # fix permission 

                self.set_local_file_attributes(parent.new_file,msg)

                # fix message if no partflg (means file size unknown until now)

                if msg.partflg == None:
                   msg.set_parts(partflg='1',chunksize=ftp.fpos)
    
                msg.report_publish(201,'Downloaded')

                msg.onfly_checksum = ftp.checksum
    
                if parent.delete and hasattr(ftp,'delete') :
                   try   :
                           ftp.delete(remote_file)
                           msg.logger.debug ('file  deleted on remote site %s' % remote_file)
                   except: msg.logger.error('unable to delete remote file %s' % remote_file)
    
                return True
                
        except:
                #closing on problem
                try    : self.close()
                except : pass
    
                (stype, svalue, tb) = sys.exc_info()
                msg.logger.error("Download failed %s. Type: %s, Value: %s" % (urlstr, stype ,svalue))
                msg.report_publish(499,'ftp download failed')
                if os.path.isfile(new_lock) : os.remove(new_lock)
 
                return False

        #closing on problem
        try    : self.close()
        except : pass
    
        msg.report_publish(498,'ftp download failed')
    
        return False

    def send( self, parent ):
        self.logger = parent.logger
        self.parent = parent
        self.logger.debug("ftp_transport send")

        msg    = parent.msg

        # 'i' cannot be supported by ftp/ftps
        # we cannot offset in the remote file to inject data
        #
        # FIXME instead of dropping the message
        # the inplace part could be delivered as 
        # a separate partfile and message set to 'p'
        if  msg.partflg == 'i':
            self.logger.error("ftp cannot send partitioned files")
            msg.report_publish(499,'ftp delivery failed')
            return False
    
        local_file = parent.local_path
        new_dir = parent.new_dir
    
        try :
                ftp = self.ftp
                if ftp == None or not ftp.check_is_connected() :
                   self.logger.debug("ftp_transport send connects")
                   ftp = sr_ftp(parent)
                   ok  = ftp.connect()
                   if not ok : return False
                   self.ftp  = ftp
                   self.cdir = None
                
                if self.cdir != new_dir :
                   self.logger.debug("ftp_transport send cd to %s" % new_dir)
                   ftp.cd_forced(775,new_dir)
                   self.cdir  = new_dir

                #=================================
                # delete event
                #=================================

                if msg.sumflg == 'R' :
                   msg.logger.debug("message is to remove %s" % parent.new_file)
                   ftp.delete(parent.new_file)
                   msg.report_publish(205,'Reset Content : deleted')
                   return True

                #=================================
                # send event
                #=================================

                offset    = 0
                str_range = ''
    
                # deliver file
    
                if parent.inflight == None :
                   ftp.put(local_file, parent.new_file)
                elif parent.inflight == '.' :
                   new_lock = '.'  + parent.new_file
                   ftp.put(local_file, new_lock)
                   ftp.rename(new_lock, parent.new_file)
                elif parent.inflight[0] == '.' :
                   new_lock = parent.new_file + parent.inflight
                   ftp.put(local_file, new_lock)
                   ftp.rename(new_lock, parent.new_file)
                elif parent.inflight == 'umask' :
                   ftp.umask()
                   ftp.put(local_file, parent.new_file)
    
                # fix permission 

                self.set_remote_file_attributes(ftp,parent.new_file,msg)
    
                msg.logger.debug('Sent: %s %s into %s/%s %d-%d' % 
                    (parent.local_file,str_range,parent.new_dir,parent.new_file,offset,offset+msg.length-1))

                msg.report_publish(201,'Delivered')
    
                return True
                
        except:
                #closing on error
                try    : self.close()
                except : pass
    
                (stype, svalue, tb) = sys.exc_info()
                msg.logger.error("Delivery failed %s. Type: %s, Value: %s" % (parent.new_scrpath+parent.new_relpath, stype ,svalue))
                msg.report_publish(499,'ftp delivery failed')
    
                return False
    
        #closing on error
        try    : self.close()
        except : pass

        msg.report_publish(499,'ftp delivery failed')
    
        return False

# ===================================
# self_test
# ===================================

try    : 
         from sr_config         import *
         from sr_message        import *
         from sr_util           import *
except :
         from sarra.sr_config   import *
         from sarra.sr_message  import *
         from sarra.sr_util     import *

class test_logger:
      def silence(self,str):
          pass
      def __init__(self):
          self.debug   = print
          self.error   = print
          self.info    = print
          self.warning = print
          self.debug   = self.silence
          self.info    = self.silence


def self_test():

    logger = test_logger()


    # config setup
    cfg = sr_config()

    cfg.defaults()
    cfg.general()
    cfg.set_sumalgo('d')
    msg = sr_message(cfg)
    msg.filesize = None
    msg.onfly_checksum = False
    cfg.msg = msg
    #cfg.debug  = True
    my_ftp_cred = 'ftp://localhost'
    opt1 = "destination " + my_ftp_cred
    cfg.option( opt1.split()  )
    cfg.logger = logger
    cfg.timeout = 5.0
    # 1 bytes par 5 secs
    #cfg.kbytes_ps = 0.0001
    cfg.kbytes_ps = 0.01

    try:
           ftp = sr_ftp(cfg)
           ftp.connect()
           ftp.mkdir("tztz")
           ftp.chmod(0o775,"tztz")
           ftp.cd("tztz")
       
           f = open("aaa","wb")
           f.write(b"1\n")
           f.write(b"2\n")
           f.write(b"3\n")
           f.close()
       
           if hasattr(ftp,'put') :
              ftp.put("aaa", "bbb")
              ls = ftp.ls()
              logger.info("ls = %s" % ls )
       
              ftp.chmod(0o775,"bbb")
              ls = ftp.ls()
              logger.info("ls = %s" % ls )
       
              ftp.rename("bbb", "ccc")
              ls = ftp.ls()
              logger.info("ls = %s" % ls )
       
           if hasattr(ftp,'seek') :
              ftp.get("ccc", "bbb",0,0,6)
              f = open("bbb","rb")
              data = f.read()
              f.close()
       
              if data != b"1\n2\n3\n" :
                 logger.error("sr_ftp1 TEST FAILED")
                 sys.exit(1)

              os.unlink("bbb")

           msg.start_timer()
           msg.topic   = "v02.post.test"
           msg.notice  = "notice"
           msg.baseurl = my_ftp_cred
           msg.relpath = "tztz/ccc"
           msg.partflg = '1'
           msg.offset  = 0
           msg.length  = 0

           msg.local_file   = "bbb"
           msg.local_offset = 0
           msg.sumalgo      = None

           cfg.new_file     = "bbb"
           cfg.new_dir      = "."

           cfg.msg     = msg
           cfg.batch   = 5
           cfg.inflight    = None
       

           if hasattr(ftp,'get') :
              dldr = ftp_transport()
              dldr.download(cfg)
              logger.debug("checksum = %s" % msg.onfly_checksum)
              dldr.download(cfg)
              dldr.download(cfg)
              cfg.logger.info("lock .")
              cfg.inflight    = '.'
              dldr.download(cfg)
              dldr.download(cfg)
              msg.sumalgo = cfg.sumalgo
              dldr.download(cfg)
              logger.debug("checksum = %s" % msg.onfly_checksum)
              cfg.logger.info("lock .tmp")
              cfg.inflight    = '.tmp'
              dldr.download(cfg)
              dldr.download(cfg)
              dldr.close()
              dldr.close()
              dldr.close()
    
           if hasattr(ftp,'put') :
              dldr = ftp_transport()
              cfg.local_file    = "bbb"
              cfg.local_path    = "./bbb"
              cfg.new_dir       = "tztz"
              cfg.new_file      = "ddd"
              cfg.remote_file   = "ddd"
              cfg.remote_path   = "tztz/ddd"
              cfg.remote_urlstr = my_ftp_cred + "/tztz/ddd"
              cfg.remote_dir    = "tztz"
              cfg.chmod         = 0o775
              cfg.inflight      = None
              dldr.send(cfg)
              if hasattr(ftp,'delete') : dldr.ftp.delete("ddd")
              if hasattr(ftp,'delete') : dldr.ftp.delete("zzz_unexistant")
              cfg.inflight        = '.'
              dldr.send(cfg)
              if hasattr(ftp,'delete') : dldr.ftp.delete("ddd")
              cfg.inflight        = '.tmp'
              dldr.send(cfg)
              dldr.send(cfg)
              dldr.send(cfg)
              dldr.send(cfg)
              dldr.send(cfg)
              dldr.send(cfg)
              dldr.close()
              dldr.close()
              dldr.close()

              ftp = sr_ftp(cfg)
              ftp.connect()
              ftp.cd("tztz")
              ftp.ls()
              ftp.delete("ccc")
              ftp.delete("ddd")
              logger.info("%s" % ftp.originalDir)
              ftp.cd("")
              logger.info("%s" % ftp.getcwd())
              ftp.rmdir("tztz")
              ftp.close()

           if hasattr(ftp,'seek') :
              ftp = sr_ftp(cfg)
              ftp.connect()
              ftp.put("aaa","bbb",0,0,2)
              ftp.put("aaa","bbb",2,4,2)
              ftp.put("aaa","bbb",4,2,2)
              ftp.get("bbb","bbb",2,2,2)
              ftp.delete("bbb")
              f = open("bbb","rb")
              data = f.read()
              f.close()
       
              if data != b"1\n3\n3\n" :
                 logger.error("sr_ftp TEST FAILED ")
                 sys.exit(1)
       
              ftp.close()

           #opt1 = "destination ftp://mgtest"
           #cfg.option( opt1.split()  )
           #ftp.connect()
           #ftp.ls()
           #ftp.close()

    except:
           (stype, svalue, tb) = sys.exc_info()
           logger.error("sr_ftp/test (Type: %s, Value: %s)" % (stype ,svalue))
           logger.error("sr_ftp TEST FAILED")
           sys.exit(2)

    os.unlink('aaa')
    os.unlink('bbb')

    print("sr_ftp TEST PASSED")
    sys.exit(0)

# ===================================
# MAIN
# ===================================

def main():

    self_test()
    sys.exit(0)

# =========================================
# direct invocation : self testing
# =========================================

if __name__=="__main__":
   main()
